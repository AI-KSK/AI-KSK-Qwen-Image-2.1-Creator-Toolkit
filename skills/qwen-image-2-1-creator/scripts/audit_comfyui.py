#!/usr/bin/env python3
"""Strict structural audit: only widgets_values[0] on explicitly authorized prompt titles may change."""
from __future__ import annotations
import argparse, json, copy
from pathlib import Path


def audit(original:dict, updated:dict, allowed_titles:set[str]) -> dict:
    old=copy.deepcopy(original)
    new=copy.deepcopy(updated)
    old_nodes={n['id']:n for n in old.get('nodes',[])}
    new_nodes={n['id']:n for n in new.get('nodes',[])}
    if set(old_nodes)!=set(new_nodes): raise ValueError('Nodes added or removed')
    if old.get('links')!=new.get('links'): raise ValueError('Links changed')
    changed=[]
    for node_id in sorted(old_nodes):
        a=old_nodes[node_id]; b=new_nodes[node_id]
        if a==b: continue
        if a.get('type')!='PrimitiveStringMultiline' or a.get('title') not in allowed_titles:
            raise ValueError(f'Unauthorized node change: id={node_id}, title={a.get("title")}')
        x=a['widgets_values']; y=b['widgets_values']
        if x[:1]==y[:1]: raise ValueError(f'Changed node not explained: {node_id}')
        bb=copy.deepcopy(b); bb['widgets_values'][0]=x[0]
        if bb!=a: raise ValueError(f'Other properties changed on node {node_id}')
        changed.append({'id':node_id,'title':a['title']})
    # remove nodes+links then compare remaining structure
    old.pop('nodes'); new.pop('nodes'); old.pop('links');new.pop('links')
    if old!=new: raise ValueError('Workflow-level metadata changed')
    if not changed: raise ValueError('No authorized prompt changes found')
    return {'status':'PASS','modified':changed,'node_count':len(old_nodes),'link_count':len(original['links']),'runtime_tested':False}


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument('--original',required=True)
    p.add_argument('--updated',required=True)
    p.add_argument('--allowed-titles',required=True,help='Comma-separated exact prompt titles')
    a=p.parse_args()
    old=json.loads(Path(a.original).read_text('utf-8'))
    new=json.loads(Path(a.updated).read_text('utf-8'))
    result=audit(old,new,{x.strip() for x in a.allowed_titles.split(',') if x.strip()})
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
