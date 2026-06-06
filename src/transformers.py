import pandas as pd
from src.interfaces import IDataTransformer

class DefectTransformer(IDataTransformer):
    def transform(self, data: pd.DataFrame, config: dict = None) -> pd.DataFrame:
        df = data.copy()
        if config is None or "rates" not in config:
            raise ValueError("Config must contain 'rates' key with transformation details.")
        
        for rate_info in config["rates"]:
            new_column = rate_info["new_column"]
            numerator = rate_info["numerator"]
            denominator = rate_info["denominator"]

            if numerator not in data.columns or denominator not in data.columns:
                raise ValueError(f"Columns '{numerator}' and '{denominator}' must exist in the data.")
            
            # Avoid division by zero
            df[new_column] = df.apply(lambda row: row[numerator] / row[denominator] if row[denominator] != 0 else 0, axis=1)
        
        return df

class DeleteTransformer(IDataTransformer):
    def transform(self, data: pd.DataFrame, config: dict = None) -> pd.DataFrame:
        df = data.copy()
        if config is None or "columns_to_delete" not in config:
            # TODO: LOG
            return df
        
        columns_to_delete = config["columns_to_delete"]
        
        return df.drop(columns=columns_to_delete, errors='ignore')
