#!/usr/bin/env python3
"""Validate task manifests for Qwen-Image-2.1 image generation and external video handoffs.
Pure standard-library validation: does NOT run PE model, inspect image pixels, or infer content.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

IMAGE_MODES = {'t2i', 'single_edit', 'multi_edit', 'local_edit', 'transparent',
               'outpaint', 'typography', 'identity', 'storyboard', 'benchmark'}
VIDEO_MODES = {'video_t2v', 'video_i2v', 'video_storyboard'}
ALL_MODES = IMAGE_MODES | VIDEO_MODES
KNOWN_BACKENDS = {'Wan2.2', 'MiniMax H3', 'Wan2.1', 'other_external_video_model'}
RATIO_PATTERN = re.compile(r'^[1-9][0-9]*:[1-9][0-9]*$')

class TaskError(ValueError):
    pass


def load_task(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    return validate_task(data)


def validate_task(t: dict) -> dict:
    if not isinstance(t, dict):
        raise TaskError('Task must be one JSON object')
    mode = t.get('mode')
    if mode not in ALL_MODES:
        raise TaskError(f'Unsupported mode: {mode!r}')
    if not isinstance(t.get('id'), str) or not t['id'].strip():
        raise TaskError('Non-empty id is required')
    images = t.get('input_images', [])
    if not isinstance(images, list) or not all(isinstance(x, str) and x.strip() for x in images):
        raise TaskError('input_images must be a list of non-empty strings')
    n = len(images)
    if n > 10:
        raise TaskError('Qwen Image 2.1 supports at most 10 reference images')
    if mode in {'t2i', 'video_t2v'} and n:
        raise TaskError(f'{mode} must not carry input images')
    if mode in {'single_edit', 'local_edit', 'outpaint'} and n != 1:
        raise TaskError(f'{mode} requires exactly one reference image')
    if mode == 'multi_edit' and not 2 <= n <= 10:
        raise TaskError('multi_edit requires 2-10 reference images')
    if mode in {'video_i2v', 'video_storyboard'} and n < 1:
        raise TaskError(f'{mode} requires one or more input/keyframe image paths')
    if mode in {'identity'} and n < 1:
        raise TaskError('identity requires at least one identity reference')

    prompt = t.get('positive_prompt', '')
    if not isinstance(prompt, str) or len(prompt.strip()) < 20:
        raise TaskError('positive_prompt must contain a useful concrete prompt (20+ characters)')
    text_elements = t.get('rendered_text', [])
    if not isinstance(text_elements, list) or not all(isinstance(x, str) and x for x in text_elements):
        raise TaskError('rendered_text must be list of non-empty exact strings')
    for literal in text_elements:
        if '"'+literal+'"' not in prompt:
            raise TaskError(f'Rendered literal text missing from double quotes: {literal!r}')

    ratio = t.get('wh_ratio', '')
    follow = t.get('ratio_follow', '')
    if not isinstance(ratio, str) or not isinstance(follow, str):
        raise TaskError('wh_ratio and ratio_follow must be strings')
    if ratio and not RATIO_PATTERN.fullmatch(ratio):
        raise TaskError('wh_ratio must be e.g. 16:9 or empty string')
    if ratio and follow:
        raise TaskError('wh_ratio and ratio_follow are mutually exclusive')
    if follow and follow not in [f'<image{i}>' for i in range(1, n+1)]:
        raise TaskError('ratio_follow must reference an actual input image')
    if mode in {'t2i', 'video_t2v'} and follow:
        raise TaskError('Cannot follow image ratio without an image')
    if mode in {'multi_edit'}:
        for i in range(1, n+1):
            if f'<image{i}>' not in prompt:
                raise TaskError(f'Multi-image editing must state role of <image{i}>')
    if mode == 'single_edit' and '<image1>' in prompt:
        raise TaskError('Single-image PE-I2I directive should refer naturally to the image, not <image1>')
    if mode == 'outpaint' and not ratio:
        raise TaskError('outpaint must explicitly request new wh_ratio')
    if mode == 'local_edit' and not (t.get('mask_path') or t.get('visual_annotation')):
        raise TaskError('local_edit requires mask_path or documented visual_annotation')

    if mode in VIDEO_MODES:
        v = t.get('video', {})
        if not isinstance(v, dict) or v.get('backend') not in KNOWN_BACKENDS:
            raise TaskError('External video handoff needs recognized video.backend')
        shots = v.get('shots', [])
        if not isinstance(shots, list) or len(shots) < 1:
            raise TaskError('video.shots must be non-empty')
        for i, shot in enumerate(shots,1):
            if not isinstance(shot,dict) or not isinstance(shot.get('motion_prompt'),str) or len(shot['motion_prompt'])<10:
                raise TaskError(f'video.shots[{i}] missing motion_prompt')
            if not isinstance(shot.get('duration_s'),(int,float)) or shot['duration_s']<=0:
                raise TaskError(f'video.shots[{i}] needs positive duration_s')
    return t


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--task', required=True)
    ap.add_argument('--check-file-existence', action='store_true')
    args=ap.parse_args()
    t=load_task(args.task)
    if args.check_file_existence:
        missing=[]
        for img in t.get('input_images', []):
            p=Path(img)
            if not p.is_absolute(): p=Path(args.task).resolve().parent / p
            if not p.is_file(): missing.append(str(p))
        if missing: raise SystemExit('Missing input images: '+', '.join(missing))
    print(json.dumps({'status':'PASS','id':t['id'],'mode':t['mode'],
                      'reference_images':len(t.get('input_images',[])),
                      'native_video_generation':False,'runtime_tested':False},ensure_ascii=False))

if __name__=='__main__':
    main()
