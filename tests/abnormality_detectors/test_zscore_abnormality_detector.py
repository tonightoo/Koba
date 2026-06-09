import unittest
import pandas as pd
from src.interfaces import IPipelineStage, PipelineContext
from src.abnormality_detectors.zscore_abnormality_detector import ZScoreAbnormalityDetector

class TestZScoreAbnormalityDetector(unittest.TestCase):
    def setUp(self):
        config = {
            'target_columns': ['defect_rate'],
            'threshold': 2.0
        }
        self.detector: IPipelineStage = ZScoreAbnormalityDetector(config)
        self.context: PipelineContext = PipelineContext(pd.DataFrame())

   
    def test_detect_no_abnormality(self):
        self.context = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3", "Lot4", "Lot5"],
            'defect_rate': [10, 20, 30, 40, 50]  
        }))

        result_context = self.detector.execute(self.context)
        zscore_result = result_context.analysis_results["zscore_result"]
        has_zscore_abnormality = zscore_result["has_zscore_abnormality"]
        self.assertFalse(has_zscore_abnormality)
        #self.assertNotIn('zscore_abnormality_column_names', result_context.analysis_results)
        self.assertIn('defect_rate_zscore', zscore_result['data'])
        self.assertIn('defect_rate_is_abnormal', zscore_result['data']) 

    def test_detect_with_abnormalities(self):
        self.context = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3", "Lot4", "Lot5", "Lot6", "Lot7"],
            'defect_rate': [10, 12, 15, 13, 11, 14, 200]  
        }))
        result_context = self.detector.execute(self.context)

        zscore_result = result_context.analysis_results["zscore_result"]
        has_zscore_abnormality = zscore_result['has_zscore_abnormality']
        is_lot7_abnormal = zscore_result['data'].loc[
                                zscore_result['data']['LotNo'] == 'Lot7', 'defect_rate_is_abnormal'
                            ].values[0]
        is_lot1_abnormal = zscore_result['data'].loc[
                                zscore_result['data']['LotNo'] == 'Lot1', 'defect_rate_is_abnormal'
                            ].values[0]
        lot7_zscore = zscore_result['data'].loc[
                        zscore_result['data']['LotNo'] == 'Lot7', 'defect_rate_zscore'
                    ].values[0] >= 2.0

        self.assertTrue(has_zscore_abnormality)
        self.assertTrue(is_lot7_abnormal)
        self.assertFalse(is_lot1_abnormal)
        self.assertTrue(lot7_zscore)
        #self.assertEqual(set(result_context.analysis_results['zscore_abnormality_column_names']), set(['defect_rate']))
        #self.assertTrue(result_context.anlysis_result.loc[6, 'defect_rate_is_abnormal'])
        #self.assertFalse(result_context.anlysis_result.loc[0, 'defect_rate_is_abnormal'])
        #self.assertTrue(result_context.anlysis_result.loc[6, 'defect_rate_zscore'] >= 2.0)