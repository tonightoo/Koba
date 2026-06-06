from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Any

# interface for data loading
class IDataLoader(ABC):
    """
    Interface for data loading.
    """
    @abstractmethod
    def load(self) -> pd.DataFrame:
        pass

# interface for data transformation
class IDataTransformer(ABC):
    """
    Interface for data transformation.
    """
    @abstractmethod
    def transform(self, data: pd.DataFrame, config: dict = None) -> pd.DataFrame:
        """
        config example:
        {
            "rates": [
                {
                    "new_column": "defect1_rate",
                    "numerator": "defect1_count",
                    "denominator": "total_chips"
                },
                {
                    "new_column": "defect2_rate",
                    "numerator": "defect2_count",
                    "denominator": "total_chips"
                }
            ]
        }

        """
        pass


# interface for data integration
class IDataIntegrator(ABC):
    """
    Interface for data integration.
    """
    @abstractmethod
    def integrate(self, data_list: List[pd.DataFrame]) -> pd.DataFrame:
        pass

# class for abnormality detection result
class AbnormalityResult:
    """
    Class to represent the result of abnormality detection.
    """
    def __init__(self, is_detected: bool, abnormal_items: List[str], details: pd.DataFrame):
        self.is_detected = is_detected
        self.abnormal_items = abnormal_items
        self.details = details

# interface for abnoramlity detection
# e.g., calculate z-score 
class IAbnormalityDetector(ABC):
    """
    Interface for abnormality detection.
    """
    @abstractmethod
    def detect(self, data: pd.DataFrame, target_columns: List[str]) -> AbnormalityResult:
        pass


class AnalysisResult:
    """
    Class to represent the result of analysis.
    """
    def __init__(self, analyzer_name: str, summary: Dict[str, Any], raw_output: Any):
        self.analyzer_name = analyzer_name
        self.summary = summary
        self.raw_output = raw_output


class IFactorAnalyzer(ABC):
    """
    Interface for factor analysis.
    """
    @abstractmethod
    def analyze(self, data: pd.DataFrame, target: str, features: List[str]) -> AnalysisResult:
        pass

