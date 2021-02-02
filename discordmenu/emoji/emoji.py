from typing import Union

from discord import Emoji


def discord_emoji_to_emoji_name(emoji_obj: Union[str, Emoji]):
    return emoji_obj if isinstance(emoji_obj, str) else emoji_obj.name

