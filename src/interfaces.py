from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Any


class PipelineContext:
    def __init__(self, data: pd.DataFrame):
        self.data: pd.DataFrame = data.copy()

        self.analysis_results: Dict[str, Any] = {}

# interface for all process
class IPipelineStage(ABC):
    @abstractmethod
    def execute(self, context: PipelineContext) -> PipelineContext:
        pass

class IPipelineJoiner(ABC):
    @abstractmethod
    def execute(self, left_context: PipelineContext, right_context: PipelineContext) -> PipelineContext:
        pass

# interface for data loading
class IDataLoader(IPipelineStage, ABC):
    """
    Interface for data loading.
    """
    pass

# interface for data transformation
class IDataTransformer(IPipelineStage, ABC):
    """
    Interface for data transformation.
    """
    pass

# interface for data integration
class IDataIntegrator(IPipelineJoiner, ABC):
    """
    Interface for data integration.
    """
    pass 

# interface for abnoramlity detection
# e.g., calculate z-score 
class IAbnormalityDetector(IPipelineStage, ABC):
    """
    Interface for abnormality detection.
    """
    pass

class IFactorAnalyzer(IPipelineStage, ABC):
    """
    Interface for factor analysis.
    """
    pass
