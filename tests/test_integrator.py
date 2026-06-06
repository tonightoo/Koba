import unittest
import pandas as pd
from src.interfaces import IDataIntegrator
from src.integrator import KeyIntegrator



class TestKeyIntegrator(unittest.TestCase):
    def setUp(self):
        self.integrator = KeyIntegrator(key_column="LotNo")

    def test_integrate(self):
        data1 = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30]
        })

        data2 = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value2': [100, 200, 300]
        })

        integrated_data = self.integrator.integrate([data1, data2])

        expected_data = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30],
            'value2': [100, 200, 300]
        })

        pd.testing.assert_frame_equal(integrated_data, expected_data)
    
    def test_integrate_with_complicated_keys(self):
        data1 = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3", "Lot4"],
            'value1': [10, 20, 30, 40]
        })

        data2 = pd.DataFrame({
            'LotNo': ["Lot3", "Lot2", "Lot1"],
            'value2': [100, 200, 300]
        })

        integrated_data = self.integrator.integrate([data1, data2])

        expected_data = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3", "Lot4"],
            'value1': [10, 20, 30, 40],
            'value2': [300, 200, 100, None]
        })

        pd.testing.assert_frame_equal(integrated_data, expected_data)

    def test_integrate_empty_list(self):
        integrated_data = self.integrator.integrate([])
        expected_data = pd.DataFrame()
        pd.testing.assert_frame_equal(integrated_data, expected_data)
    
    def test_integrate_single_dataframe(self):
        data = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30]
        })

        integrated_data = self.integrator.integrate([data])
        pd.testing.assert_frame_equal(integrated_data, data)

    def test_integrate_non_overlapping_keys(self):
        data1 = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30]
        })

        data2 = pd.DataFrame({
            'LotNo': ["Lot4", "Lot5", "Lot6"],
            'value2': [100, 200, 300]
        })

        integrated_data = self.integrator.integrate([data1, data2])

        expected_data = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3", "Lot4", "Lot5", "Lot6"],
            'value1': [10, 20, 30, None, None, None],
            'value2': [None, None, None, 100, 200, 300]
        })

        pd.testing.assert_frame_equal(integrated_data, expected_data)

    def test_integrate_different_key_names(self):
        data1 = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30]
        })

        data2 = pd.DataFrame({
            'LotID': ["Lot1", "Lot2", "Lot3"],
            'value2': [100, 200, 300]
        })

        with self.assertRaises(KeyError):
            self.integrator.integrate([data1, data2])

    def test_integrate_different_key_types(self):
        data1 = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30]
        })

        data2 = pd.DataFrame({
            'LotNo': [1, 2, 3],  # 数値型のキー
            'value2': [100, 200, 300]
        })

        with self.assertRaises(ValueError):
            self.integrator.integrate([data1, data2])

    def test_integrate_with_missing_keys(self):
        data1 = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30]
        })

        data2 = pd.DataFrame({
            'LotNo': ["Lot2", "Lot3", "Lot4"],
            'value2': [200, 300, 400]
        })

        integrated_data = self.integrator.integrate([data1, data2])

        expected_data = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3", "Lot4"],
            'value1': [10, 20, 30, None],
            'value2': [None, 200, 300, 400]
        })

        pd.testing.assert_frame_equal(integrated_data, expected_data)

    def test_integrate_with_duplicate_keys(self):
        data1 = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot2"],
            'value1': [10, 20, 30]
        })

        data2 = pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value2': [100, 200, 300]
        })

        with self.assertRaises(ValueError):
            self.integrator.integrate([data1, data2])