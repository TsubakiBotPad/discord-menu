from typing import Callable, List, Optional, Coroutine, Dict

from discord import Message, RawReactionActionEvent
from discordmenu.discord_client import remove_reaction, diff_emojis, update_embed_control, send_embed_control
from discordmenu.embed.control import EmbedControl
from discordmenu.embed.view_state import ViewState
from discordmenu.reaction_filter import ReactionFilter

_IntraMessageState = Dict
NextEmbedControlFunc = Callable[[Optional[Message], Dict, _IntraMessageState], Coroutine[None, None, EmbedControl]]


class EmbedMenu:
    def __init__(self,
                 reaction_filters: List[ReactionFilter],
                 transitions: Dict[str, NextEmbedControlFunc],
                 initial_pane: Callable):
        self.transitions = transitions
        self.reaction_filters = reaction_filters
        self.initial_pane = initial_pane

    async def create(self, ctx, state: ViewState):
        await send_embed_control(ctx, self.initial_pane(state))

    async def transition(self, message, ims, emoji_clicked, **data):
        transition_func = self.transitions.get(emoji_clicked)
        if not transition_func:
            return

        new_control = await transition_func(message, ims, **data)
        emoji_diff = diff_emojis(message, new_control)
        await update_embed_control(message, new_control, emoji_diff)

        if message.guild:
            await remove_reaction(message, emoji_clicked, ims['original_author_id'])

    async def should_respond(self, message, event: RawReactionActionEvent):
        for reaction_filter in self.reaction_filters:
            allow = await reaction_filter.allow_reaction_raw(message, event)
            if not allow:
                return False
        return True
