#!/usr/bin/env python3
"""Safe scoped positive-prompt injection to existing ComfyUI UI-workflow JSON.
Does NOT create reference image sockets, change samplers/models, run inference or install nodes.
"""
from __future__ import annotations
import argparse, copy, json
from pathlib import Path
from validate_task import load_task, TaskError


def inject(wf: dict, task: dict, *, node_id: int | None = None, node_title: str | None = None) -> dict:
    if (node_id is None)==(node_title is None):
        raise ValueError('Pass exactly one node_id or node_title')
    if task['mode'].startswith('video_'):
        raise ValueError('Video handoff tasks are not ComfyUI image prompts')
    obj=copy.deepcopy(wf)
    hits=[n for n in obj.get('nodes',[]) if (n.get('id')==node_id if node_id is not None else n.get('title')==node_title)]
    if len(hits)!=1:
        raise ValueError(f'Expected exactly one target prompt node, found {len(hits)}')
    n=hits[0]
    if n.get('type')!='PrimitiveStringMultiline':
        raise ValueError('Injection target must be PrimitiveStringMultiline and already wired to the correct encoder')
    vals=n.get('widgets_values')
    if not isinstance(vals,list) or not vals or not isinstance(vals[0],str):
        raise ValueError('Prompt node widgets_values[0] is not text')
    if not n.get('outputs') or not n['outputs'][0].get('links'):
        raise ValueError('Prompt node is not wired. Refusing to inject a disconnected widget.')
    n['widgets_values'][0]=task['positive_prompt']
    return obj


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument('--workflow',required=True)
    p.add_argument('--task',required=True)
    sel=p.add_mutually_exclusive_group(required=True)
    sel.add_argument('--node-id',type=int)
    sel.add_argument('--node-title')
    p.add_argument('--output',required=True)
    p.add_argument('--force',action='store_true')
    a=p.parse_args()
    out=Path(a.output)
    if out.exists() and not a.force: raise SystemExit('Output already exists. Add --force to explicitly overwrite: '+str(out))
    src=json.loads(Path(a.workflow).read_text(encoding='utf-8'))
    task=load_task(a.task)
    upd=inject(src,task,node_id=a.node_id,node_title=a.node_title)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(upd,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'PASS: {out} — only authorized prompt widget modified. Run audit_comfyui.py.')

if __name__=='__main__':main()
