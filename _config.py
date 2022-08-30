import os.path
from pathlib import Path

__all__ = ["BASE_DIR", "config"]
BASE_DIR = Path(__file__).resolve().parent


class Config:
	base_dir = BASE_DIR
	dotenv_file_path = os.path.join(BASE_DIR, '.env')
	cogs_dir_path = os.path.join(BASE_DIR, 'cogs')

	embed_color = 0x00ff00
	embed_footer: str = "Powered by FOX"


config = Config()
