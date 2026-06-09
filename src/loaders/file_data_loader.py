import copy
import pandas as pd
from src.interfaces import IDataLoader, PipelineContext

class FileDataLoader(IDataLoader):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def execute(self, context: PipelineContext) -> PipelineContext:
        result = copy.deepcopy(context)
        result.data = pd.read_csv(self.file_path)
        return result

