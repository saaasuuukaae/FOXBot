import os
import disnake
from disnake.ext.commands import Bot, Cog
from _config import config
import dotenv

bot = Bot(command_prefix=config.command_prefix)
bot.help_command = None


# Function to load environment variables from .env file
def load_env(file_path: str):
	dotenv.load_dotenv(
		file_path
	)


def main():
	load_env(config.dotenv_file_path)
	bot.run(os.environ.get("TOKEN"))


if __name__ == '__main__':
	main()
