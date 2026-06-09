import copy
import pandas as pd
from typing import List, Dict, Any
from src.interfaces import IDataTransformer, PipelineContext

class DeleteTransformer(IDataTransformer):
    def __init__(self, config: Dict[str, Any]):
        if config is None or 'columns_to_delete' not in config:
            raise ValueError("Config must contain 'rates' key with transformation details.")

        self.columns_to_delete = config['columns_to_delete']

    def execute(self, context: PipelineContext) -> PipelineContext:
        result = copy.deepcopy(context)
        result.data = result.data.drop(columns=self.columns_to_delete, errors='ignore')
        return result
