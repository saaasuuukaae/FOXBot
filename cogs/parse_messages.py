import os

import disnake

from disnake.ext.commands import Bot, Cog, slash_command

from _config import config
from fox import JsonManager


class OnlyRootUsersCommand(disnake.ext.commands.CommandError):
	pass


class ParseMessages(Cog):
	def __init__(self, bot: Bot):
		self.bot = bot
		self.toggle_parser.add_check(self.check)
		self.toggle_embeds.add_check(self.check)

	@staticmethod
	async def is_valid_message(
			message: disnake.Message, manager: JsonManager
	) -> bool:
		if not manager.enabled:
			return False

		if message.author.bot:
			return False

		if not message.guild.id == manager.root.id:
			return False

		if message.channel.id not in manager.root.root_channels:
			return False

		if message.author.id not in manager.root.root_users:
			return False

		return True

	async def process(
			self, message: disnake.Message, manager: JsonManager,
			embed=False
	):

		embed_message = disnake.Embed(
			title="Message",
			description=message.content,
			color=config.embed_color,
		)

		icon = self.bot.user.avatar
		if icon is None:
			icon_url = ""
		else:
			icon_url = icon.url

		embed_message.set_footer(
			icon_url=icon_url,
			text=config.embed_footer
		)

		for _ in manager.guilds:
			guild = self.bot.get_guild(_.id)

			if guild is None:
				print("Unable to get guild with ID={}".format(_.id))
				continue
			for c in _.channels:

				channel = guild.get_channel(c)
				if channel is None:
					print(
						"Unable to get channel with ID={}\nguild.id={}".
						format(c, guild.id)
					)
					continue

				try:
					if embed:
						await channel.send(embeds=[embed_message])
					else:
						await channel.send(message.content)
				except Exception as exc:
					print("An error occurred: {}\n"
					      "When tried to send message to channel {} in "
					      "the guild = {}".format(exc, channel.id, guild.id))

	@Cog.listener(
		name='on_message',
	)
	async def on_message(self, message: disnake.Message):
		manager = JsonManager(
			os.path.join(config.base_dir, 'data.json')
		)
		validity = await self.is_valid_message(message, manager)

		if not validity:
			return

		await self.process(
			message=message,
			manager=manager,
			embed=manager.send_embed,
		)

	@slash_command(
		name='toggle'
	)
	async def toggle_parser(
			self, inter:
			disnake.ApplicationCommandInteraction
	):
		manager = JsonManager(
			os.path.join(config.base_dir, 'data.json')
		)

		manager.enabled = not manager.enabled

		await inter.send(
			f"Parser is now {'enabled' if manager.enabled else 'disabled'}"
		)

	@slash_command(
		name="toggle-embeds"
	)
	async def toggle_embeds(
			self, inter:
			disnake.ApplicationCommandInteraction
	):
		manager = JsonManager(
			os.path.join(config.base_dir, 'data.json')
		)

		manager.send_embed = not manager.send_embed

		await inter.send(
			f"Embeds are now "
			f"{'enabled' if manager.send_embed else 'disabled'}"
		)

	@toggle_embeds.error
	@toggle_parser.error
	async def error_handler(
			self, inter: disnake.ApplicationCommandInteraction, error:
			Exception
	):
		if isinstance(error, OnlyRootUsersCommand):
			await inter.send("You are not allowed to use this command")
		else:
			await inter.send(
				"An error has occurred when processing your request")

	def check(self, inter: disnake.ApplicationCommandInteraction):
		manager = JsonManager(
			os.path.join(config.base_dir, 'data.json')
		)
		if inter.user.id in manager.root.root_users:
			return True
		else:
			raise OnlyRootUsersCommand("This command is only for root users")


def setup(bot: Bot):
	bot.add_cog(ParseMessages(bot))
	print("Added cog: ParseMessages")
