import os
from typing import List
from pydantic import BaseModel, ValidationError
from plct_ai_data_unifier.utils import read_json, read_yaml

class RepoObject(BaseModel):
    url: str

class ConfigModel(BaseModel):
    repos: List[RepoObject] = []


def load_config(path: str) -> ConfigModel:
    ext = os.path.splitext(path)[1].lower()
    if ext in (".yaml", ".yml"):
        raw = read_yaml(path)
    elif ext == ".json":
        raw = read_json(path)
    else:
        # Prefer YAML for human-edited files, but keep JSON compatibility.
        try:
            raw = read_yaml(path)
        except Exception:
            raw = read_json(path)
    try:
        cfg = ConfigModel.model_validate(raw)
    except ValidationError as exc:
        raise
    return cfg


def is_git_repo(path: str) -> bool:
    return os.path.exists(path) and os.path.isdir(path) and os.path.exists(os.path.join(path, ".git"))