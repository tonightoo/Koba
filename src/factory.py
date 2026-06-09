import importlib
from typing import Dict, Any
from src.interfaces import IPipelineStage

def create_stage_instance(module_path: str, class_name: str, config_dict: Dict[str, Any]) -> IPipelineStage:
    if not module_path or not class_name:
        raise ValueError(f"[Factory] module_path({module_path}) or class_name({class_name}) is missing")
    try:
        module = importlib.import_module(module_path)
        stage_class = getattr(module, class_name)

        return stage_class(config=config_dict)
    
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(f"module {module_path} not found") from e
    except AttributeError as e:
        raise AttributeError(f"{class_name} not found in {module_path}")


