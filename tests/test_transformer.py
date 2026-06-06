import unittest
import pandas as pd
from src.interfaces import IDataTransformer
from src.loaders import DummyDataLoader
from src.transformers import DefectTransformer
from src.transformers import DeleteTransformer


class TestDefectTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = DefectTransformer()
        self.loader = DummyDataLoader()

    def test_transform_defects(self):
        data = self.loader.load()
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

        transformed_data = self.transformer.transform(data, config)

        expected_data = {
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
        }

        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(transformed_data, expected_df)

    def test_transform_defects_with_zero_denominator(self):
        data = self.loader.load()
        data.loc[0, 'total_chips'] = 0  # Set total_chips to zero for the first row

        config = {
            "rates": [
                {
                    "new_column": "defect1_rate",
                    "numerator": "defect1_count",
                    "denominator": "total_chips"
                }
            ]
        }

        transformed_data = self.transformer.transform(data, config)

        expected_defect1_rate = [0, 15/1000, 12/1000, 250/1000]  # First row should be 0 due to division by zero handling
        self.assertListEqual(transformed_data['defect1_rate'].tolist(), expected_defect1_rate)

    def test_transform_defects_with_missing_columns(self):
        data = self.loader.load()
        config = {
            "rates": [
                {
                    "new_column": "defect1_rate",
                    "numerator": "defect1_count",
                    "denominator": "missing_column"
                }
            ]
        }

        with self.assertRaises(ValueError):
            self.transformer.transform(data, config)

    def test_transform_defects_with_invalid_config(self):
        data = self.loader.load()
        config = {
            "invalid_key": []
        }

        with self.assertRaises(ValueError):
            self.transformer.transform(data, config)

    def test_transform_defects_with_none_config(self):
        data = self.loader.load()

        with self.assertRaises(ValueError):
            self.transformer.transform(data, None)

    def test_transform_defects_with_empty_rates(self):
        data = self.loader.load()
        config = {
            "rates": []
        }

        transformed_data = self.transformer.transform(data, config)
        pd.testing.assert_frame_equal(transformed_data, data)

    def test_transform_defects_with_nonexistent_numerator(self):
        data = self.loader.load()
        config = {
            "rates": [
                {
                    "new_column": "defect1_rate",
                    "numerator": "nonexistent_count",
                    "denominator": "total_chips"
                }
            ]
        }

        with self.assertRaises(ValueError):
            self.transformer.transform(data, config)



class TestDeleteTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = DeleteTransformer()
        self.loader = DummyDataLoader()

    def test_transform_delete(self):
        data = self.loader.load()
        config = {
            "columns_to_delete": ["factor2", "factor5", "factor8"]
        }

        transformed_data = self.transformer.transform(data, config)

        expected_data = {
            'LotNo':       ["Lot1", "Lot2", "Lot3", "Lot4"],
            'total_chips': [1000,   1000,   1000,   1000],
            'defect1_count': [10,     15,     12,     250],
            'defect2_count': [5,      30,      6,      7],
            'defect3_count': [2,      1,      3,      2],
            'factor1':      [180.0,  182.0,  179.0,  230.0],
            'factor3':      [5.0,    5.2,    4.8,    5.1],
            'factor4':      [10.0,   35.0,   10.2,   9.8],
            'factor6':      [20.0,   22.0,   21.0,   20.5],
            'factor7':      [25.1,   26.3,   24.8,   25.5],
            'factor9':      [120.0,  121.0,  119.0,  120.5],
        }

        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(transformed_data, expected_df)

    def test_transform_delete_with_nonexistent_columns(self):
        data = self.loader.load()
        config = {
            "columns_to_delete": ["nonexistent_column"]
        }

        transformed_data = self.transformer.transform(data, config)
        pd.testing.assert_frame_equal(transformed_data, data)




