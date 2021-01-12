import inspect
from typing import Callable, Optional, List, Union
from typing import Dict

from discord import Message, Embed, Emoji, RawReactionActionEvent

from discordmenu.embed.components import EmbedMain, EmbedAuthor, EmbedFooter, EmbedThumbnail, EmbedBodyImage, \
    EmbedField
from discordmenu.intra_message_state import IntraMessageState
from discordmenu.reaction_filter import ReactionFilter


class EmbedView:
    def __init__(self,
                 embed_main: EmbedMain,
                 embed_author: EmbedAuthor = None,
                 embed_thumbnail: EmbedThumbnail = None,
                 embed_body_image: EmbedBodyImage = None,
                 embed_fields: List[EmbedField] = None,
                 embed_footer: EmbedFooter = None
                 ):
        self.embed_author = embed_author
        self.embed_body_image = embed_body_image
        self.embed_thumbnail = embed_thumbnail
        self.embed_main = embed_main
        self.embed_fields = embed_fields or []
        self.embed_footer = embed_footer

    def to_embed(self) -> Embed:
        embed = Embed(**self.embed_main)
        embed.set_thumbnail(**self.embed_thumbnail) if self.embed_thumbnail else None
        embed.set_image(**self.embed_body_image) if self.embed_body_image else None
        embed.set_author(**self.embed_author) if self.embed_author else None
        embed.set_footer(**self.embed_footer) if self.embed_footer else None

        for field in self.embed_fields:
            embed.add_field(**field)

        return embed

    @staticmethod
    def from_message(existing_embed: Embed) -> "EmbedView":
        main = EmbedMain(existing_embed.title, existing_embed.url, existing_embed.colour, existing_embed.description)

        e_author = existing_embed.author
        author = EmbedAuthor(e_author.name, e_author.url, e_author.icon_url)

        thumbnail = EmbedThumbnail(existing_embed.thumbnail.url)
        body_image = EmbedBodyImage(existing_embed.image.url)

        e_footer = existing_embed.footer
        footer = EmbedFooter(e_footer.text, e_footer.icon_url)

        fields = [EmbedField(e.name, e.value, e.inline) for e in existing_embed.fields]
        return EmbedView(main, author, thumbnail, body_image, fields, footer)


class EmbedControl:
    def __init__(self, embed_views: List[EmbedView], emoji_buttons: List[Union[Emoji, str]] = None):
        self.embed_views = embed_views
        self.emoji_buttons = emoji_buttons or []

    @staticmethod
    def from_message(message: Message) -> "EmbedControl":
        emojis = [r.emoji for r in message.reactions]
        embed_views = [EmbedView.from_message(e) for e in message.embeds]
        return EmbedControl(embed_views, emojis)


_IntraMessageState = Dict
NextEmbedControlFunc = Callable[[EmbedControl, _IntraMessageState], EmbedControl]


async def _get_next_embed_control(func, embed_control: EmbedControl, state: Dict) -> Optional[EmbedControl]:
    updated_message = None
    if inspect.iscoroutinefunction(func):
        updated_message = await func(embed_control, **state)
    elif inspect.isfunction(func):
        updated_message = func(embed_control, **state)
    return updated_message


class EmbedMenu:
    def __init__(self,
                 reaction_filters: List[ReactionFilter],
                 panes: Dict[str, NextEmbedControlFunc]):
        self.panes = panes
        self.reaction_filters = reaction_filters

    def get_embed_control(self, emoji_name, prev_embed_control: EmbedControl = None, state: _IntraMessageState = None):
        return self.panes.get(emoji_name)(prev_embed_control, **state)

    async def next_embed_control(self, message: Message, emoji_name_received: str) -> Optional[EmbedControl]:
        ims = IntraMessageState.extract_data(message.embeds[0])

        embed_control = EmbedControl.from_message(message)
        func = self.panes.get(emoji_name_received)
        if not func:
            return embed_control

        return await _get_next_embed_control(func, embed_control, ims)

    def diff_emojis(self, message: Message, next_embed_control: Optional[EmbedControl]):
        current_emojis = [e.emoji for e in message.reactions]
        next_emojis = next_embed_control.emoji_buttons

        return {
            'add': [e for e in next_emojis if e not in current_emojis],
            'remove': [e for e in current_emojis if e not in next_emojis],
        }

    async def should_respond(self, message, event: RawReactionActionEvent):
        for reaction_filter in self.reaction_filters:
            allow = await reaction_filter.allow_reaction_raw(message, event)
            if not allow:
                return False
        return True
