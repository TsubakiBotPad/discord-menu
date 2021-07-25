from typing import List, Union, Tuple

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

    def get_by_name(self, names: Union[str, Tuple[str], List[str]]):
        return self._get_value_by_name(names, self._emoji)

    def get_name_by_name(self, names: Union[str, Tuple[str], List[str]]):
        return self._get_value_by_name(names, self._emoji_name)

    def _get_value_by_name(self, names: Union[str, Tuple[str], List[str]], f):
        # names will be a tuple if looking up immediately from an emoji list
        # but it becomes a list when deserialized from an ims
        if isinstance(names, str):
            res = [f(e) for e in self.custom_emojis if e.name == names]
            return res[0] if len(res) > 0 else names
        else:
            # return the first success, if there is one
            # otherwise just return the last thing, which is presumed to be a default emoji
            # a list of length 0 is invalid input
            if len(names) == 0:
                raise KeyError
            for name in names:
                res = [e.name for e in self.custom_emojis if e.name == name]
                if len(res) > 0:
                    return res[0]
            return self.get_by_name(names[-1])

    @staticmethod
    def _emoji(e: Emoji):
        return e

    @staticmethod
    def _emoji_name(e: Emoji):
        return e.name

    def get_emoji(self, name):
        for e in self.custom_emojis:
            if e.name == name:
                return str(e)

        # special case when a unicode character is specified
        if len(name) == 1 and not is_ascii(name):
            return name

        return ":{}:".format(name)


emoji_cache = EmojiCache([])
