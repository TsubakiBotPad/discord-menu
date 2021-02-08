import asyncio
from typing import Callable, List, Optional, Coroutine, Dict

from discord import Message, RawReactionActionEvent
from discordmenu.discord_client import remove_reaction, update_embed_control, send_embed_control, \
    diff_emojis_raw
from discordmenu.embed.control import EmbedControl
from discordmenu.embed.emoji import DEFAULT_EMBED_MENU_EMOJI_CONFIG, EmbedMenuEmojiConfig
from discordmenu.embed.view_state import ViewState
from discordmenu.emoji.emoji import discord_emoji_to_emoji_name
from discordmenu.emoji.emoji_cache import emoji_cache
from discordmenu.reaction_filter import ReactionFilter

_IntraMessageState = Dict
NextEmbedControlFunc = Callable[[Optional[Message], Dict, _IntraMessageState], Coroutine[None, None, EmbedControl]]


class EmbedMenu:
    def __init__(self,
                 reaction_filters: List[ReactionFilter],
                 transitions: Dict[str, NextEmbedControlFunc],
                 initial_pane: Callable,
                 emoji_config: EmbedMenuEmojiConfig = DEFAULT_EMBED_MENU_EMOJI_CONFIG,
                 unsupported_transition_announce_timeout: int = 10
                 ):
        self.emoji_config = emoji_config
        self.transitions = transitions
        self.reaction_filters = reaction_filters
        self.initial_pane = initial_pane
        self.unsupported_transition_announce_timeout = unsupported_transition_announce_timeout

    async def create(self, ctx, state: ViewState):
        embed_control: EmbedControl = self.initial_pane(state)
        e_buttons = embed_control.emoji_buttons

        # Only add the close button if it doesn't exist, in case user has overridden it.
        e_buttons.append(
            self.emoji_config.delete_message) if self.emoji_config.delete_message not in e_buttons else None
        await send_embed_control(ctx, embed_control)

    async def transition(self, message, ims, emoji_clicked, member, **data):
        transition_func = self.transitions.get(emoji_clicked)
        if not transition_func:
            if emoji_clicked == discord_emoji_to_emoji_name(self.emoji_config.delete_message):
                await message.delete()
            return

        new_control = await transition_func(message, ims, **data)

        if new_control is not None:
            current_emojis = [e.emoji for e in message.reactions]

            next_emojis = new_control.emoji_buttons + [emoji_cache.get_emoji(self.emoji_config.delete_message)]

            emoji_diff = diff_emojis_raw(current_emojis, next_emojis)
            await update_embed_control(message, new_control, emoji_diff)
        elif self.emoji_config.unsupported_transition is not None:
            # allow the reporting of an unsupported transition to be nulled by config
            await message.add_reaction(self.emoji_config.unsupported_transition)
            asyncio.create_task(self.remove_unsupported_action_response(message))

        if message.guild:
            await remove_reaction(message, emoji_clicked, member.id)

    async def remove_unsupported_action_response(self, message):
        await asyncio.sleep(self.unsupported_transition_announce_timeout)
        await message.clear_reaction(self.emoji_config.unsupported_transition)

    async def should_respond_raw(self, message, event: RawReactionActionEvent):
        for reaction_filter in self.reaction_filters:
            allow = await reaction_filter.allow_reaction_raw(message, event)
            if not allow:
                return False
        return True

    async def should_respond(self, message, reaction, member):
        for reaction_filter in self.reaction_filters:
            allow = await reaction_filter.allow_reaction(message, reaction, member)
            if not allow:
                return False
        return True
