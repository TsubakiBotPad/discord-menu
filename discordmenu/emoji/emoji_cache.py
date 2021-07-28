from typing import List, Union, Sequence

from discord import Emoji as Emoji
from discord.ext.commands import Bot


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


class EmojiCache:
    def __init__(self, guild_ids: List[int]):
        self.guild_ids = guild_ids
        self.custom_emojis: List[Emoji] = []

    def set_guild_ids(self, guild_ids: List[int]) -> None:
        self.guild_ids = guild_ids

    def refresh_from_discord_bot(self, bot: Bot) -> None:
        self.custom_emojis = [e for g in bot.guilds if g.id in self.guild_ids for e in g.emojis]

    def refresh_from_emojis(self, emojis: List[Emoji]) -> None:
        self.custom_emojis = emojis

    def get_by_name(self, names: Union[str, Sequence[str]]) -> Union[Emoji, str]:
        return self._get_value_by_name(names, self._emoji)

    def get_name_by_name(self, names: Union[str, Sequence[str]]) -> Union[Emoji, str]:
        return self._get_value_by_name(names, self._emoji_name)

    def _get_value_by_name(self, names: Union[str, Sequence[str]], f) -> Union[Emoji, str]:
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
    def _emoji(e: Emoji) -> Emoji:
        return e

    @staticmethod
    def _emoji_name(e: Emoji) -> str:
        return e.name

    def get_emoji(self, name: str) -> str:
        """Use for getting an emoji name to print in text"""
        for e in self.custom_emojis:
            if e.name == name:
                return str(e)

        # special case when a unicode character is specified
        if len(name) == 1 and not is_ascii(name):
            return name

        return ":{}:".format(name)

    def get_raw_emoji(self, name: str) -> str:
        """Same as get_emoji but no colons - use for getting a reaction name"""
        for e in self.custom_emojis:
            if e.name == name:
                return str(e)

        # special case when a unicode character is specified
        if len(name) == 1 and not is_ascii(name):
            return name

        return str(name)


emoji_cache = EmojiCache([])
