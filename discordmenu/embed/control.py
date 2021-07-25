from typing import List, Union

from discord import Message, Emoji

from discordmenu.embed.view import EmbedView
from discordmenu.emoji.emoji_cache import emoji_cache


class EmbedControl:
    def __init__(self, embed_views: List[EmbedView], emoji_buttons: List[Union[Emoji, str]] = None):
        self.embed_views = embed_views
        self.emoji_buttons = [emoji_cache.get_name_by_name(e) for e in emoji_buttons] or []

    @staticmethod
    def from_message(message: Message) -> "EmbedControl":
        emojis = [r.emoji for r in message.reactions]
        embed_views = [EmbedView.from_message(e) for e in message.embeds]
        return EmbedControl(embed_views, emojis)
