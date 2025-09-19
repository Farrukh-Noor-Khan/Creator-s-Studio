# core/utils.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_env_var(key):
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Missing env var: {key}")
    return value