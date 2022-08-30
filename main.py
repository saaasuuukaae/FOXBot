import os
import disnake
from disnake.ext.commands import Bot, Cog
from _config import config
import dotenv
from fox import *

bot = Bot(intents=disnake.Intents.all())
bot.help_command = None


@bot.slash_command(
	name="ping",

)
async def ping(inter: disnake.ApplicationCommandInteraction):
	await inter.send("pong")

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user}")
	print(f"{len(bot.guilds)} guilds")
	print(f"{len(bot.users)} users")

# Function to load environment variables from .env file
def load_env(file_path: str):
	dotenv.load_dotenv(
		file_path
	)


# Function that loads all cogs
def load_cogs():
	for file in os.listdir(config.cogs_dir_path):
		if file.endswith(".py"):
			bot.load_extension(f"cogs.{file[:-3]}")
			print(f"Loaded extension: {file[:-3]}")


def test():
	manager = JsonManager(
		os.path.join(config.base_dir, 'data.json')
	)

	root = manager.root
	print(root.id)
	print(root.root_channels)
	print(root.root_users)

def main():
	load_env(config.dotenv_file_path)
	load_cogs()
	test()
	bot.run(os.environ.get("TOKEN"))


if __name__ == '__main__':
	main()
