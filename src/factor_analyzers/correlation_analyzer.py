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

        if self.target_column not in result_context.data:
            raise ValueError(f"target_column '{self.target_column}' not found in data")
        
        target_features = self.feature_columns
        if not target_features:
            target_features = [col for col in result_context.data if col != self.target_column]

        result_rows = []

        for col in result_context.data.columns:
            if col == self.target_column:
                continue

            corr_val = result_context.data[self.target_column].corr(result_context.data[col], method='pearson')

            if pd.isna(corr_val):
                is_high = False
            else:
                is_high = abs(corr_val) >= self.threshold

            records.append({
                'target_column': self.target_column,
                'compare_column': col,
                'correlation_value': corr_val if not pd.isna(corr_val) else None,
                'is_high_correlation': is_high
            })

        result = {}
        result['data'] = pd.DataFrame(records)
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