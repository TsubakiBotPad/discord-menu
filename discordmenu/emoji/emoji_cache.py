from typing import List

from discord import Emoji as Emoji
from discord.ext.commands import Bot


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


class EmojiCache:
    def __init__(self, guild_ids: List[int]):
        self.guild_ids = guild_ids
        self.custom_emojis: List[Emoji] = []

    def set_guild_ids(self, guild_ids: List[int]):
        self.guild_ids = guild_ids

    def refresh_from_discord_bot(self, bot: Bot):
        self.custom_emojis = [e for g in bot.guilds if g.id in self.guild_ids for e in g.emojis]

    def refresh_from_emojis(self, emojis: List[Emoji]):
        self.custom_emojis = emojis

    def get_by_name(self, name):
        res = [e for e in self.custom_emojis if e.name == name]
        return res[0] if len(res) > 0 else name

    def get_emoji(self, name):
        for e in self.custom_emojis:
            if e.name == name:
                return str(e)

        # special case when a unicode character is specified
        if len(name) == 1 and not is_ascii(name):
            return name

        return ":{}:".format(name)


emoji_cache = EmojiCache([])
