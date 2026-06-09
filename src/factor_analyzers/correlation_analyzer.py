import copy
import pandas as pd
from typing import List, Dict, Any
from src.interfaces import IFactorAnalyzer, PipelineContext

class CorrelationAnalyzer(IFactorAnalyzer):
    def __init__(self, config: Dict[str, Any]):
        if config is None:
            raise ValueError("[CorrectionAnalyzer] there's no config")

        self.threshold = config['threshold']
        self.target_column = config['target_column']
        self.feature_columns = config['feature_columns'] or []
        self.data_types = config['data_types'] or {}

        if not self.target_column:
            raise ValueError("[CorrelationFactorAnalyzer] target_column is needed in config")

    def execute(self, context: PipelineContext) -> PipelineContext:
        result_context = copy.deepcopy(context)
        df = result_context.data

        if self.target_column not in df:
            raise ValueError(f"target_column '{self.target_column}' not found in data")
        
        target_features = self.feature_columns
        if not target_features:
            target_features = [col for col in df if col != self.target_column]

        result_rows = []

        for col in df.columns:
            if col == self.target_column:
                continue

            data_type = self._determine_data_type(df[col], col)

            if data_type == 'nominal':
                print(f"{col} is nominal and removed from correlation")
                continue
            elif data_type == 'ordinal':
                if (df[col].dtype == 'object' or
                    pd.api.types.is_string_dtype(df[col])):
                    working_series = df[col].astype('category').cat.codes
                else:
                    working_series = df[col]

                method_name = 'spearman'
                corr_val = df[self.target_column].corr(working_series, method = method_name)
            else:
                method_name = 'pearson'
                corr_val = df[self.target_column].corr(df[col], method = method_name)

            if pd.isna(corr_val):
                is_high = False
            else:
                is_high = abs(corr_val) >= self.threshold

            result_rows.append({
                'target_column': self.target_column,
                'compare_column': col,
                'data_type': data_type,
                'method': method_name,
                'correlation_value': corr_val if not pd.isna(corr_val) else None,
                'is_high_correlation': is_high
            })

        result = {}
        result['data'] = pd.DataFrame(result_rows)
        result['has_high_correlation'] = result['data']['is_high_correlation'].any()
        result_context.analysis_results['correlation_result'] = result

        return result_context

    def _determine_data_type(self, series: pd.Series, col_name: str) -> str:
        if col_name in self.data_types:
            return self.data_types[col_name]

        if (pd.api.types.is_object_dtype(series) or
             pd.api.types.is_string_dtype(series)):
             return "nominal"
            
        if pd.api.types.is_float_dtype(series):
            return "continuous"
            
        unique_count = series.nunique()
        if unique_count < 10:
            return "ordinal"
            
        return "continuous"