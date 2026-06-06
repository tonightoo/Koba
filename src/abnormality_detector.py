import pandas as pd
from typing import List
from src.interfaces import IAbnormalityDetector, AbnormalityResult

class ZScoreAbnormalityDetector(IAbnormalityDetector):
    def __init__(self, threshold):
        self.threshold = threshold

    def detect(self, data: pd.DataFrame, target_columns: List[str]) -> AbnormalityResult:
        df = data.copy()
        abnormal_items = []

        for col in target_columns:
            if col not in df.columns:
                continue

            avg = df[col].mean()
            std = df[col].std(ddof=0)

            if std == 0:
                continue

            z_scores = (df[col] - avg).abs() / std
            is_abnormal_series = z_scores > self.threshold

            df[f"{col}_zscore"] = z_scores
            df[f"{col}_is_abnormal"] = is_abnormal_series

            if is_abnormal_series.any():
                abnormal_items.append(col)

        is_detected = len(abnormal_items) > 0

        return AbnormalityResult(
            is_detected=is_detected,
            abnormal_items=abnormal_items,
            details=df
        )








