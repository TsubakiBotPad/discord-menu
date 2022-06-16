from typing import Protocol, Sequence, Union

import discord
from discord.ext.commands import AutoShardedBot


class BotSupportsMenus(Protocol):
    def cached_messages(self) -> Sequence[discord.Message]:
        ...

    @property
    def user(self) -> discord.User:
        ...

    def get_user(self, user_id: str) -> discord.User:
        ...

    def get_menu_context(self, ims: dict) -> dict:
        ...

    def get_channel(self, channel_id: str) -> Union[discord.TextChannel, discord.DMChannel]:
        ...

    def get_context(self, message: discord.Message) -> discord.ext.commands.Context:
        ...

    def get_cog(self, cog_name: str) -> discord.ext.commands.Cog:
        ...
