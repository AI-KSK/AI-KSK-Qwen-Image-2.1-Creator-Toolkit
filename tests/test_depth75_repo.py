import csv
import pathlib
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_depth75 import check_all

class Depth75PackageTests(unittest.TestCase):
    def test_workflows(self):
        reports=check_all()
        self.assertEqual(len(reports),3)
        for r in reports:
            self.assertEqual(r['status'],'PASS')
            self.assertFalse(r['runtime_tested'])

    def test_matrix_csv(self):
        with (ROOT/'data'/'depth75_matrix.csv').open(encoding='utf-8',newline='') as f:
            data=list(csv.DictReader(f))
        self.assertEqual(len(data),75)
        self.assertEqual(len(set(x['label'] for x in data)),75)
        self.assertEqual({x['start_percent'] for x in data},{'0.00','0.25','0.50'})
        self.assertEqual({x['end_percent'] for x in data},{'0.60','0.70','0.80','0.90','1.00'})
        self.assertEqual({x['weight'] for x in data},{'0.20','0.40','0.60','0.80','1.00'})

if __name__=='__main__':unittest.main()
