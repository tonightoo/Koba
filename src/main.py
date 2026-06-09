import json
import os
import copy
from typing import List, Dict, Any
import pandas as pd

from src.interfaces import PipelineContext
from src.factory import create_stage_instance

def load_pipeline_config(config_path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"File not found: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_pipeline(pipelien_configs: List[Dict[str, Any]]) -> Dict[str, PipelineContext]:
    context_cache = {}
    initial_context = PipelineContext(pd.DataFrame())
    context_cache['0'] = initial_context

    print('start pipeline process')

    for stage_info in pipelien_configs:
        stage_id = stage_info.get('id')
        parent_id = stage_info.get('depends_on')
        module_path = stage_info.get('module')
        class_name = stage_info.get('class')
        config_dict = stage_info.get('config') or {}

        if parent_id is None:
            base_context = copy.deepcopy(initial_context)
        else:
            if parent_id not in context_cache:
                raise ValueError(f'error: {parent_id} not found')
            base_context = copy.deepcopy(context_cache[parent_id])
        
        stage_instance = create_stage_instance(module_path, class_name, config_dict)

        result_context = stage_instance.execute(base_context)

        context_cache[stage_id] = result_context

    print('finish pipeline process')
    return context_cache