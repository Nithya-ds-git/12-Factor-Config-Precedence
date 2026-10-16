import os
from typing import List, Optional

import yaml
from dotenv import dotenv_values
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DEFAULTS = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

ALIASES = {"num_workers": "workers"}


def normalize_key(key):
    key = key.strip().lower()
    return ALIASES.get(key, key)


def coerce(key, value):
    if key in ("port", "workers"):
        return int(value)
    if key == "debug":
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in ("true", "1", "yes", "on")
    return str(value)


def load_yaml(env_name):
    path = os.path.join(BASE_DIR, f"config.{env_name}.yaml")
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    return {normalize_key(k): v for k, v in data.items()}


def load_dotenv_layer():
    out = {}
    for k, v in dotenv_values(os.path.join(BASE_DIR, ".env")).items():
        if k.upper().startswith("APP_"):
            k = k[4:]
        out[normalize_key(k)] = v
    return out


def load_os_env():
    out = {}
    for k, v in os.environ.items():
        if k.startswith("APP_"):
            out[normalize_key(k[4:])] = v
    return out


@app.get("/effective-config")
def effective_config(set: Optional[List[str]] = Query(default=None)):
    env_name = os.environ.get("APP_ENV", "development")

    config = dict(DEFAULTS)              # 1. defaults
    config.update(load_yaml(env_name))   # 2. YAML
    config.update(load_dotenv_layer())   # 3. .env
    config.update(load_os_env())         # 4. OS env

    for item in set or []:               # 5. CLI overrides
        if "=" in item:
            k, v = item.split("=", 1)
            config[normalize_key(k)] = v

    result = {k: coerce(k, v) for k, v in config.items()}
    result["api_key"] = "****"
    return result
