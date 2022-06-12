from typing import Union, Iterable

from discord import Message

from discordmenu.embed.emoji import EmojiRef, MultiEmojiRef
from discordmenu.embed.view import EmbedView
from discordmenu.emoji.emoji_cache import emoji_cache


class EmbedWrapper:
    def __init__(self, embed_view: EmbedView,
                 emoji_buttons: Iterable[Union[EmojiRef, MultiEmojiRef]] = None):
        self.embed_view = embed_view
        self.emoji_buttons = [emoji_cache.get_name_by_name(e) for e in emoji_buttons or []]

    @staticmethod
    def from_message(message: Message) -> "EmbedWrapper":
        emojis = [r.emoji for r in message.reactions]
        embed_view = EmbedView.from_message(message.embeds[0])
        return EmbedWrapper(embed_view, emojis)
