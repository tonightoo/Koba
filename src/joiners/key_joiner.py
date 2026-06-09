import pandas as pd
from src.interfaces import IDataIntegrator, PipelineContext
from typing import List, Dict, Any

class KeyJoiner(IDataIntegrator):
    def __init__(self, config: Dict[str, Any]):
        self.key_column = config['key_column_name']


    def execute(self, left_context: PipelineContext, right_context: PipelineContext) -> PipelineContext:
        if not left_context:
            return right_context
        if not right_context:
            return left_context

        result_context: PipelineContext = PipelineContext(pd.DataFrame())
        result_context.data = pd.merge(left_context.data, right_context.data, on=self.key_column, how='outer', validate='one_to_one')
        return result_context

