import unittest
import pandas as pd
from src.interfaces import IAbnormalityDetector, AbnormalityResult
from src.abnormality_detector import ZScoreAbnormalityDetector

class TestZScoreAbnormalityDetector(unittest.TestCase):
    def setUp(self):
        self.detector = ZScoreAbnormalityDetector(threshold = 2)

   
    def test_detect_no_abnormality(self):
        data = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3", "Lot4", "Lot5"],
            'defect_rate': [10, 20, 30, 40, 50]  
        })
        result = self.detector.detect(data, ['defect_rate'])
        self.assertFalse(result.is_detected)
        self.assertEqual(result.abnormal_items, [])
        self.assertIn('defect_rate_zscore', result.details.columns)
        self.assertIn('defect_rate_is_abnormal', result.details.columns)

    def test_detect_with_abnormalities(self):
        data = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3", "Lot4", "Lot5", "Lot6", "Lot7"],
            'defect_rate': [10, 12, 15, 13, 11, 14, 200]  
        })
        result = self.detector.detect(data, ['defect_rate']) 
        self.assertTrue(result.is_detected)
        self.assertEqual(set(result.abnormal_items), set(['defect_rate']))
        self.assertTrue(result.details.loc[6, 'defect_rate_is_abnormal'])
        self.assertFalse(result.details.loc[0, 'defect_rate_is_abnormal'])
        self.assertTrue(result.details.loc[6, 'defect_rate_zscore'] >= 2.0)