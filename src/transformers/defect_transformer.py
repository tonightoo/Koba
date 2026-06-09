import copy
import pandas as pd
from typing import List, Dict, Any
from src.interfaces import IDataTransformer, PipelineContext

class DefectTransformer(IDataTransformer):
    def __init__(self, config: Dict[str, Any]):
        if config is None or 'rates' not in config:
            raise ValueError("Config must contain 'rates' key with transformation details.")

        self.config = config
        for rate_info in self.config['rates']:
            if (not isinstance(rate_info['new_column'], str) or 
                not isinstance(rate_info['numerator'], str) or 
                not isinstance(rate_info['denominator'], str)
            ):
                raise ValueError("'new_column', 'numerator' and 'denominator' should be string type.")
        

    def execute(self, context: PipelineContext) -> PipelineContext:
        result = copy.deepcopy(context)

        for rate_info in self.config['rates']:
            new_column = rate_info['new_column']
            numerator = rate_info['numerator']
            denominator = rate_info['denominator']

            if numerator not in result.data.columns or denominator not in result.data.columns:
                raise ValueError(f"Columns '{numerator}' and '{denominator}' must exist in the data.")
            
            # Avoid division by zero
            result.data[new_column] = result.data.apply(lambda row: row[numerator] / row[denominator] if row[denominator] != 0 else 0, axis=1)
        
        return result

