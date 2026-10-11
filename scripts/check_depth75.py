#!/usr/bin/env python3
"""Offline validation for GitHub-shipped Qwen Image 2.1 Depth-75 UI workflows.

No ComfyUI, model files, internet, or GPU required. This is a static check only.
"""
from __future__ import annotations
import argparse
import collections
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILES={
    'small':'workflows/depth75/01_first_row_5_previews.json',
    'full':'workflows/depth75/02_all_75_previews.json',
    'manual':'workflows/depth75/03_manual_depth_first_row_5.json',
}
STARTS=(0.0,0.25,0.5)
ENDS=(0.6,0.7,0.8,0.9,1.0)
WEIGHTS=(0.2,0.4,0.6,0.8,1.0)

def check_one(path, *, expected_active):
    wf=json.loads(Path(path).read_text(encoding='utf-8'))
    nodes=wf['nodes'];links=wf['links']
    ids=[n['id'] for n in nodes]; linkids=[v[0] for v in links]
    assert len(nodes)==316,(path,'node count',len(nodes))
    assert len(links) in (836,837),(path,'link count',len(links))
    assert len(set(ids))==len(ids),(path,'duplicate node ids')
    assert len(set(linkids))==len(linkids),(path,'duplicate link ids')
    idx={n['id']:n for n in nodes}
    edges={x[0]:x for x in links}
    for lid,src,sidx,dst,didx,typ in links:
        assert src in idx and dst in idx,(path,'bad node reference',lid)
        s=idx[src];d=idx[dst]
        assert 0<=sidx<len(s.get('outputs',[])),(path,'bad output slot',lid)
        assert 0<=didx<len(d.get('inputs',[])),(path,'bad input slot',lid)
        assert s['outputs'][sidx]['type']==typ==d['inputs'][didx]['type'],(path,'type mismatch',lid)
        assert lid in (s['outputs'][sidx].get('links') or []),(path,'source missing reverse link',lid)
        assert lid==d['inputs'][didx].get('link'),(path,'dest missing reverse link',lid)
    for node in nodes:
        for o in node.get('outputs',[]):
            for lid in o.get('links') or []: assert lid in edges,(path,'dangling output',node['id'],lid)
        for ii in node.get('inputs',[]):
            if ii.get('link') is not None: assert ii['link'] in edges,(path,'dangling input',node['id'])
    c=collections.Counter(n['type'] for n in nodes)
    assert c['QwenImage21UnionApply']==75 and c['KSampler']==76,(path,c)
    assert c['PreviewImage']==78 and c['VAEDecode']==76,(path,c)
    assert c['QwenImage21UnionLoader']==1
    assert c['QwenImage21UnionLatentFromImage']==1
    assert c['TextEncodeQwenImage21']==1
    assert c['LoadImage']==(2 if c['DepthAnythingV2Preprocessor']==0 else 1)
    assert c['DepthAnythingV2Preprocessor'] in (0,1)
    controls=[n for n in nodes if n['type']=='QwenImage21UnionApply']
    seen=set()
    for n in controls:
        v=n['widgets_values']
        assert len(v)==4 and v[0]=='Depth',(path,n['id'],v)
        tag=(round(float(v[2]),2),round(float(v[3]),2),round(float(v[1]),2))
        assert 0<=tag[0]<=tag[1]<=1 and 0<=tag[2]<=2
        assert tag not in seen,(path,'duplicate cell',tag)
        seen.add(tag)
        # Each Union output goes to exactly one sampler MODEL input.
        output_links=n['outputs'][0]['links']
        assert len(output_links)==1
        outlink=edges[output_links[0]]
        assert idx[outlink[3]]['type']=='KSampler'
        # Each control node shares same checkpoint / VAE / ControlNet / depth map sources.
        for inp in ['model','union_patch','vae','control_image']:
            item=next(x for x in n['inputs'] if x['name']==inp)
            assert item['link'] is not None,(path,n['id'],inp)
    expected={(a,b,c) for a in STARTS for b in ENDS for c in WEIGHTS}
    assert seen==expected,(path,'matrix mismatch')
    for n in nodes:
        if n['type']=='KSampler':
            v=n.get('widgets_values',[])
            assert len(v)==7,(path,'widget layout',n['id'],v)
            assert v[0]==9527 and v[1]=='fixed' and v[2]==25
            assert v[3]==3.5 and v[4]=='euler' and v[5]=='simple' and v[6]==1.0,(path,n['id'],v)
    actives=[n for n in nodes if n['type']=='KSampler' and n.get('mode',0)==0]
    assert len(actives)==expected_active,(path,'active samplers',len(actives),expected_active)
    # 76 distinct sampler→decode→preview chains, all connected; previews labeled by 75 controls.
    seen_previews=set()
    for n in [n for n in nodes if n['type']=='KSampler']:
        outlink=edges[n['outputs'][0]['links'][0]]
        decoder=idx[outlink[3]]
        assert decoder['type']=='VAEDecode'
        assert any(x['name']=='vae' and x.get('link') for x in decoder['inputs'])
        did=edges[decoder['outputs'][0]['links'][0]][3]
        assert idx[did]['type']=='PreviewImage'
        assert did not in seen_previews
        seen_previews.add(did)
    return {'status':'PASS','file':str(path),'nodes':len(nodes),'links':len(links),
            'matrix':len(controls),'samplers':c['KSampler'],'active_samplers':len(actives),
            'preview_paths':len(seen_previews),'runtime_tested':False}

def check_all():
    return [check_one(ROOT/FILES[k],expected_active=(76 if k=='full' else 6)) for k in FILES]

def main():
    parser=argparse.ArgumentParser(description='Validate Qwen Image 2.1 Depth75 UI workflow static structure.')
    parser.add_argument('--json',help='Check one workflow JSON instead of repository defaults')
    args=parser.parse_args()
    if args.json:
        path=Path(args.json)
        active=sum(n['type']=='KSampler' and n.get('mode',0)==0 for n in json.loads(path.read_text('utf-8'))['nodes'])
        result=[check_one(path,expected_active=active)]
    else: result=check_all()
    for r in result:print(json.dumps(r,ensure_ascii=False))

if __name__=='__main__':main()
