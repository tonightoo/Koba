import copy
import pandas as pd
from typing import List
from src.interfaces import IAbnormalityDetector, PipelineContext

class ZScoreAbnormalityDetector(IAbnormalityDetector):
    def __init__(self, config: Dict[str, Any]):
        self.threshold = config['threshold']
        self.target_columns = config['target_columns']

    def execute(self, context: PipelineContext) -> PipelineContext:
        result_context = copy.deepcopy(context)
        abnormal_items = []
        result = {}
        result_data = pd.DataFrame({})
        result_data["LotNo"] = context.data["LotNo"]

        for col in self.target_columns:
            if col not in context.data.columns:
                continue

            avg = context.data[col].mean()
            std = context.data[col].std(ddof=0)

            if std == 0:
                continue

            z_scores = (context.data[col] - avg).abs() / std
            is_abnormal_series = z_scores > self.threshold

            result_data[f"{col}_zscore"] = z_scores
            result_data[f"{col}_is_abnormal"] = is_abnormal_series
            #result_context.data[f"{col}_zscore"] = z_scores
            #result_context.data[f"{col}_is_abnormal"] = is_abnormal_series
            if is_abnormal_series.any():
                abnormal_items.append(col)

        is_detected = len(abnormal_items) > 0
        result['has_zscore_abnormality'] = is_detected
        result['data'] = result_data
        result_context.analysis_results['zscore_result'] = result

        return result_context
