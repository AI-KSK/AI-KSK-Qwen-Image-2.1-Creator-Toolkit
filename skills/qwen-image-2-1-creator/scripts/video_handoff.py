#!/usr/bin/env python3
"""Create an external video-model handoff manifest. Does not synthesize video."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from validate_task import load_task, VIDEO_MODES


def handoff(t:dict)->dict:
    if t['mode'] not in VIDEO_MODES: raise ValueError('Only video_* tasks allowed')
    shots=[]
    for j,s in enumerate(t['video']['shots'],start=1):
        shots.append({'shot':j,'source_image':s.get('source_image'),
                      'motion_prompt':s['motion_prompt'],
                      'duration_s':s['duration_s'],'camera':s.get('camera','user-defined'),
                      'continuity_lock':s.get('continuity_lock','preserve identity and visual direction'),
                      'status':'waiting_for_external_video_model'})
    return {'task_id':t['id'],'workflow':'Qwen-image design/frames -> external video model',
            'backend':t['video']['backend'],'external_inference_required':True,
            'native_qwen_image_video':False,'source_images':t.get('input_images',[]),
            'storyboard_visual_prompt':t['positive_prompt'],'shots':shots,
            'runtime_verified':False}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--task',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--force',action='store_true')
    a=ap.parse_args();t=load_task(a.task)
    o=Path(a.output)
    if o.exists() and not a.force:raise SystemExit('Refusing overwrite: '+str(o))
    o.parent.mkdir(parents=True,exist_ok=True)
    o.write_text(json.dumps(handoff(t),ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS: external-video HANDOFF ONLY (not rendered): '+str(o))
if __name__=='__main__':main()
