import pandas as pd
from src.interfaces import IDataIntegrator

class KeyIntegrator(IDataIntegrator):
    def __init__(self, key_column: str):
        self.key_column = key_column

    def integrate(self, data_list: list[pd.DataFrame]) -> pd.DataFrame:
        if not data_list:
            return pd.DataFrame()

        integrated_data = data_list[0]
        for data in data_list[1:]:
            integrated_data = pd.merge(integrated_data, data, on=self.key_column, how='outer', validate='one_to_one')

        return integrated_data
