import copy
import json
import pathlib
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_task import load_task, validate_task, TaskError
from inject_comfyui import inject
from audit_comfyui import audit
from video_handoff import handoff


class FullSkillTests(unittest.TestCase):
    def test_all_thirteen_routes_valid(self):
        files=sorted((ROOT/'examples').glob('*.json'))
        self.assertEqual(len(files),16)
        for f in files:
            with self.subTest(example=f.name):
                self.assertIn('positive_prompt',load_task(f))

    def test_multi_reference_limit(self):
        t=load_task(ROOT/'examples'/'multi_edit.json')
        t['input_images']=[f'x{i}.png' for i in range(11)]
        with self.assertRaises(TaskError):validate_task(t)

    def test_multi_tags_required(self):
        t=load_task(ROOT/'examples'/'multi_edit.json')
        t['positive_prompt']=t['positive_prompt'].replace('<image2>','第二张图')
        with self.assertRaises(TaskError):validate_task(t)

    def test_t2i_rejects_images(self):
        t=load_task(ROOT/'examples'/'t2i_poster.json')
        t['input_images']=['source.png']
        with self.assertRaises(TaskError):validate_task(t)

    def test_literal_text_lock(self):
        t=load_task(ROOT/'examples'/'t2i_poster.json')
        t['positive_prompt']=t['positive_prompt'].replace('"AUTUMN 2026"','"AUTUMN 2025"')
        with self.assertRaises(TaskError):validate_task(t)

    def test_conflicting_ratio(self):
        t=load_task(ROOT/'examples'/'outpaint.json')
        t['ratio_follow']='<image1>'
        with self.assertRaises(TaskError):validate_task(t)

    def test_local_edit_needs_mask(self):
        t=load_task(ROOT/'examples'/'local_edit.json')
        t.pop('mask_path')
        with self.assertRaises(TaskError):validate_task(t)

    def test_video_only_external(self):
        t=load_task(ROOT/'examples'/'video_storyboard.json')
        h=handoff(t)
        self.assertTrue(h['external_inference_required'])
        self.assertFalse(h['runtime_verified'])
        self.assertEqual(len(h['shots']),2)

    def test_video_bad_backend_rejected(self):
        t=load_task(ROOT/'examples'/'video_t2v.json')
        t['video']['backend']='Qwen Image 2.1'
        with self.assertRaises(TaskError):validate_task(t)

    def test_safe_inject_and_audit(self):
        wf=json.loads((ROOT/'assets'/'reference_11groups.json').read_text('utf-8'))
        t=load_task(ROOT/'examples'/'t2i_poster.json')
        nw=inject(wf,t,node_title='T2I-01｜正向提示词')
        rep=audit(wf,nw,{'T2I-01｜正向提示词'})
        self.assertEqual(rep['status'],'PASS')
        self.assertEqual(len(wf['nodes']),len(nw['nodes']))
        self.assertEqual(len(wf['links']),len(nw['links']))
        self.assertNotEqual(wf['nodes'][0]['widgets_values'][0],nw['nodes'][0]['widgets_values'][0])

    def test_non_target_mutation_caught(self):
        wf=json.loads((ROOT/'assets'/'reference_11groups.json').read_text('utf-8'))
        t=load_task(ROOT/'examples'/'t2i_poster.json')
        nw=inject(wf,t,node_title='T2I-01｜正向提示词')
        sampler=next(x for x in nw['nodes'] if x['type']=='KSamplerAdvanced')
        sampler['widgets_values'][3]=999
        with self.assertRaises(ValueError):audit(wf,nw,{'T2I-01｜正向提示词'})

    def test_unwired_prompt_rejected(self):
        wf=json.loads((ROOT/'assets'/'reference_11groups.json').read_text('utf-8'))
        t=load_task(ROOT/'examples'/'t2i_poster.json')
        unused=next(x for x in wf['nodes'] if x['type']=='PrimitiveStringMultiline' and not x['outputs'][0]['links']) if any(x['type']=='PrimitiveStringMultiline' and not x['outputs'][0]['links'] for x in wf['nodes']) else None
        if unused is None:
            # simulate one known target disconnected
            target=next(x for x in wf['nodes'] if x.get('title')=='T2I-01｜正向提示词')
            target['outputs'][0]['links']=[]
            unused=target
        with self.assertRaises(ValueError):inject(wf,t,node_id=unused['id'])


if __name__=='__main__':unittest.main()
