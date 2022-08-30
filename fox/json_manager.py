from typing import Optional
import json

from fox.exceptions import JsonManagerError


class RootGuild:

	def __init__(self, data: dict):
		self.id = data.get("id", None)
		self.root_channels = data.get("root_channels", None)
		self.root_users = data.get("root_users", None)

	def __repr__(self):
		return f"<RootGuild id={self.id}>"


class Guild:

	def __init__(
			self,
			guild: dict
	):
		self.id: int = guild.get('id', None)
		self.channels: list[int] = guild.get('channels', None)

	def __repr__(self):
		return f"<Guild id={self.id}>"


class JsonManager:

	def __init__(
			self,
			file_path: str,
	):
		self.file_path = file_path
		self.dictionary: dict = {}

		self.root: Optional[RootGuild] = None
		self.guilds: list[Guild] = []

		self.process()

	def process(self):
		# Reading file
		with open(self.file_path, "r") as file:
			dictionary = json.load(
				file,
			)

			# Getting root guild
			root = dictionary.get("root_guild", None)

			if root is None:
				raise JsonManagerError("Root guild not found")

			self.root = RootGuild(root)

			# Getting guilds
			guilds = dictionary.get("guilds", None)

			if guilds is None:
				raise JsonManagerError("Guilds not found")

			for guild in guilds:
				self.guilds.append(Guild(guild))

			self.dictionary = dictionary

			return 0  # Success

	def save(self):
		with open(self.file_path, "w") as file:
			json.dump(
				self.dictionary,
				file,
				indent=4,
				sort_keys=True,
			)

	@property
	def enabled(self):
		return self.dictionary.get('enabled')

	@enabled.setter
	def enabled(self, value: bool):
		self.dictionary['enabled'] = value
		self.save()

	@property
	def send_embed(self):
		return self.dictionary.get('send_embed')

	@send_embed.setter
	def send_embed(self, value: bool):
		self.dictionary['send_embed'] = value
		self.save()
