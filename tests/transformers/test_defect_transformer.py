import unittest
import pandas as pd
from src.interfaces import IPipelineStage, PipelineContext
from src.loaders.dummy_data_loader import DummyDataLoader
from src.transformers.defect_transformer import DefectTransformer


class TestDefectTransformer(unittest.TestCase):
    def setUp(self):
        self.loader: IPipelineStage = DummyDataLoader()
        self.context: PipelineContext = PipelineContext(pd.DataFrame())

    def test_transform_defects(self):
        config = {
            "rates": [
                {
                    "new_column": "defect1_rate",
                    "numerator": "defect1_count",
                    "denominator": "total_chips"
                },
                {
                    "new_column": "defect2_rate",
                    "numerator": "defect2_count",
                    "denominator": "total_chips"
                }
            ]
        }

        self.transformer: IPipelineStage = DefectTransformer(config)
        self.context = self.loader.execute(self.context)

        transformed_context = self.transformer.execute(self.context)

        expected_data = pd.DataFrame({
            'LotNo':       ["Lot1", "Lot2", "Lot3", "Lot4"],
            'total_chips': [1000,   1000,   1000,   1000],
            'defect1_count': [10,     15,     12,     250],
            'defect2_count': [5,      30,      6,      7],
            'defect3_count': [2,      1,      3,      2],
            'factor1':      [180.0,  182.0,  179.0,  230.0],
            'factor2':      [60.0,   61.0,   59.0,   60.0],
            'factor3':      [5.0,    5.2,    4.8,    5.1],
            'factor4':      [10.0,   35.0,   10.2,   9.8],
            'factor5':      [0.50,   0.51,   0.49,   0.50],
            'factor6':      [20.0,   22.0,   21.0,   20.5],
            'factor7':      [25.1,   26.3,   24.8,   25.5],
            'factor8':      [50.0,   52.0,   48.0,   51.0],
            'factor9':      [120.0,  121.0,  119.0,  120.5],
            'defect1_rate': [10/1000,15/1000,12/1000,250/1000],
            'defect2_rate': [5/1000 ,30/1000 ,6/1000 ,7/1000 ]
        })

        expected_context = PipelineContext(expected_data)
        pd.testing.assert_frame_equal(transformed_context.data, expected_context.data)

    def test_transform_defects_with_zero_denominator(self):
        config = {
            "rates": [
                {
                    "new_column": "defect1_rate",
                    "numerator": "defect1_count",
                    "denominator": "total_chips"
                }
            ]
        }
        self.transformer = DefectTransformer(config)

        self.context = self.loader.execute(self.context)
        self.context.data.loc[0, 'total_chips'] = 0  # Set total_chips to zero for the first row


        transformed_context = self.transformer.execute(self.context)

        expected_defect1_rate = [0, 15/1000, 12/1000, 250/1000]  # First row should be 0 due to division by zero handling
        self.assertListEqual(transformed_context.data['defect1_rate'].tolist(), expected_defect1_rate)

    def test_transform_defects_with_missing_columns(self):
        self.context = self.loader.execute(self.context)
        config = {
            "rates": [
                {
                    "new_column": "defect1_rate",
                    "numerator": "defect1_count",
                    "denominator": "missing_column"
                }
            ]
        }
        self.transformer = DefectTransformer(config)

        with self.assertRaises(ValueError):
            self.transformer.execute(self.context)

    def test_transform_defects_with_invalid_config(self):
        config = {
            "invalid_key": []
        }
        with self.assertRaises(ValueError):
            self.transformer = DefectTransformer(config)

    def test_transform_defects_with_none_config(self):
        self.context = self.loader.execute(self.context)

        with self.assertRaises(ValueError):
            self.transformer = DefectTransformer(None)

    def test_transform_defects_with_empty_rates(self):
        config = {
            "rates": []
        }
        self.transformer = DefectTransformer(config)

        self.context = self.loader.execute(self.context)
        transformed_context = self.transformer.execute(self.context)
        pd.testing.assert_frame_equal(transformed_context.data, self.context.data)

    def test_transform_defects_with_nonexistent_numerator(self):
        config = {
            "rates": [
                {
                    "new_column": "defect1_rate",
                    "numerator": "nonexistent_count",
                    "denominator": "total_chips"
                }
            ]
        }
        self.transformer = DefectTransformer(config)

        self.context = self.loader.execute(self.context)
        with self.assertRaises(ValueError):
            self.transformer.execute(self.context)


