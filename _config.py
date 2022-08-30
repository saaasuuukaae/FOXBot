import os.path
from pathlib import Path

__all__ = ["BASE_DIR", "config"]
BASE_DIR = Path(__file__).resolve().parent


class Config:
	dotenv_file_path = os.path.join(BASE_DIR, '.env')


config = Config()
