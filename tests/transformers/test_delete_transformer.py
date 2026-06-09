import unittest
import pandas as pd
from src.interfaces import IPipelineStage, PipelineContext
from src.loaders.dummy_data_loader import DummyDataLoader
from src.transformers.delete_transformer import DeleteTransformer

class TestDeleteTransformer(unittest.TestCase):
    def setUp(self):
        self.loader: IPipelineStage = DummyDataLoader()
        self.context: PipelineContext = PipelineContext(pd.DataFrame())

    def test_transform_delete(self):
        config = {
            "columns_to_delete": ["factor2", "factor5", "factor8"]
        }
        self.transformer = DeleteTransformer(config)

        self.context = self.loader.execute(self.context)
        transformed_context = self.transformer.execute(self.context)

        expected_data = pd.DataFrame({
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
        })

        expected_context = PipelineContext(expected_data)
        pd.testing.assert_frame_equal(transformed_context.data, expected_context.data)

    def test_transform_delete_with_nonexistent_columns(self):
        config = {
            "columns_to_delete": ["nonexistent_column"]
        }
        self.transformer = DeleteTransformer(config)

        self.context = self.loader.execute(self.context)
        transformed_context = self.transformer.execute(self.context)
        pd.testing.assert_frame_equal(transformed_context.data, self.context.data)




