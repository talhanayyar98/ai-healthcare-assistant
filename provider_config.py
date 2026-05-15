import os

from dotenv import load_dotenv

load_dotenv()


def get_provider(env_name: str, default: str) -> str:
    return os.getenv(env_name, default).strip().lower()
