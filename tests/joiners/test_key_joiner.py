import unittest
import pandas as pd
from src.interfaces import IPipelineJoiner, PipelineContext
from src.joiners.key_joiner import KeyJoiner



class TestKeyIntegrator(unittest.TestCase):
    def setUp(self):
        config = {
            "key_column_name": "LotNo"
        }
        self.integrator: IPipelineJoiner = KeyJoiner(config)
        self.context1: PipelineContext = PipelineContext(pd.DataFrame())
        self.context2: PipelineContext = PipelineContext(pd.DataFrame())

    def test_integrate(self):
        self.context1 = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30]
        }))

        self.context2 = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value2': [100, 200, 300]
        }))


        integrated_context = self.integrator.execute(self.context1, self.context2)

        expected_context = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30],
            'value2': [100, 200, 300]
        }))

        pd.testing.assert_frame_equal(integrated_context.data, expected_context.data)
    
    def test_integrate_with_complicated_keys(self):
        self.context1 = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3", "Lot4"],
            'value1': [10, 20, 30, 40]
        }))

        self.context2 = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot3", "Lot2", "Lot1"],
            'value2': [100, 200, 300]
        }))

        integrated_context = self.integrator.execute(self.context1, self.context2)

        expected_context = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3", "Lot4"],
            'value1': [10, 20, 30, 40],
            'value2': [300, 200, 100, None]
        }))

        pd.testing.assert_frame_equal(integrated_context.data, expected_context.data)

    def test_integrate_empty_list(self):
        self.context1 = PipelineContext(pd.DataFrame([]))
        self.context2 = PipelineContext(pd.DataFrame([]))

        with self.assertRaises(KeyError):
            self.integrator.execute(self.context1, self.context2)
        #expected_context = PipelineContext(pd.DataFrame([]))
        #pd.testing.assert_frame_equal(integrated_context.data, expected_context.data)
    
    def test_integrate_single_dataframe(self):
        self.context1 = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30]
        }))
        self.context2 = PipelineContext(pd.DataFrame([]))

        with self.assertRaises(KeyError):
             self.integrator.execute(self.context1, self.context2)
        ##pd.testing.assert_frame_equal(integrated_context.data, self.context1.data)

    def test_integrate_non_overlapping_keys(self):
        self.context1 = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30]
        }))

        self.context2 = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot4", "Lot5", "Lot6"],
            'value2': [100, 200, 300]
        }))

        integrated_context = self.integrator.execute(self.context1, self.context2)

        expected_conetext = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3", "Lot4", "Lot5", "Lot6"],
            'value1': [10, 20, 30, None, None, None],
            'value2': [None, None, None, 100, 200, 300]
        }))

        pd.testing.assert_frame_equal(integrated_context.data, expected_conetext.data)

    def test_integrate_different_key_names(self):
        self.context1 = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30]
        }))

        self.context2 = PipelineContext(pd.DataFrame({
            'LotID': ["Lot1", "Lot2", "Lot3"],
            'value2': [100, 200, 300]
        }))

        with self.assertRaises(KeyError):
            self.integrator.execute(self.context1, self.context2)

    def test_integrate_different_key_types(self):
        self.context1 = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30]
        }))

        self.context2 = PipelineContext(pd.DataFrame({
            'LotNo': [1, 2, 3],  # 数値型のキー
            'value2': [100, 200, 300]
        }))

        self.context1 = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value1': [10, 20, 30]
        }))

        with self.assertRaises(ValueError):
            self.integrator.execute(self.context1, self.context2)

    def test_integrate_with_missing_keys(self):
        
        self.context2 = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot2", "Lot3", "Lot4"],
            'value2': [200, 300, 400]
        }))

        with self.assertRaises(KeyError):
            self.integrator.execute(self.context1, self.context2)

        #expected_context = PipelineContext(pd.DataFrame({
        #    'LotNo': ["Lot1", "Lot2", "Lot3", "Lot4"],
        #    'value1': [10, 20, 30, None],
        #    'value2': [None, 200, 300, 400]
        #}))

        #pd.testing.assert_frame_equal(integrated_context.data, expected_context.data)

    def test_integrate_with_duplicate_keys(self):
        self.context1 = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot2"],
            'value1': [10, 20, 30]
        }))

        self.context2 = PipelineContext(pd.DataFrame({
            'LotNo': ["Lot1", "Lot2", "Lot3"],
            'value2': [100, 200, 300]
        }))

        with self.assertRaises(ValueError):
            self.integrator.execute(self.context1, self.context2)