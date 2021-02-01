import abc
from collections.abc import Iterable
from typing import Optional

from discord import Reaction, Message, Member, RawReactionActionEvent
from discordmenu.embed.emoji import DEFAULT_EMBED_MENU_EMOJI_CONFIG, EmbedMenuEmojiConfig


class ReactionFilter:
    def __init__(self, reaction_filter: Optional["ReactionFilter"] = None):
        self.inner_filter: ReactionFilter = reaction_filter

    async def allow_reaction(self, message: Message, reaction: Reaction, member: Member):
        parent = await self._allow_reaction(message, reaction, member)
        if not parent:
            return False

        return await self.inner_filter.allow_reaction(message, reaction, member) if self.inner_filter else True

    async def allow_reaction_raw(self, message: Message, reaction: RawReactionActionEvent):
        parent = await self._allow_reaction_raw(message, reaction)
        if not parent:
            return False

        return await self.inner_filter.allow_reaction_raw(message, reaction) if self.inner_filter else True

    async def _allow_reaction(self, message: Message, reaction: Reaction, member: Member):
        return True

    async def _allow_reaction_raw(self, message: Message, reaction: RawReactionActionEvent):
        return True


class ValidEmojiReactionFilter(ReactionFilter):
    def __init__(self, valid_emoji_names: Iterable, default_emoji_override: EmbedMenuEmojiConfig = None,
                 filters: Optional[ReactionFilter] = None):
        super().__init__(filters)
        default_emojis = default_emoji_override or DEFAULT_EMBED_MENU_EMOJI_CONFIG
        emoji_set = set(default_emojis.to_list())
        emoji_set.update(valid_emoji_names)
        self.valid_emoji_names = list(emoji_set)

    async def _allow_reaction(self, message: Message, reaction: Reaction, member: Member):
        valid_emoji_reaction = str(reaction.emoji.name) in self.valid_emoji_names
        return valid_emoji_reaction

    async def _allow_reaction_raw(self, message: Message, reaction: RawReactionActionEvent):
        valid_emoji_reaction = str(reaction.emoji.name) in self.valid_emoji_names
        return valid_emoji_reaction


class NotPosterEmojiReactionFilter(ReactionFilter):
    """
    This prevents the bot from reacting to its own emojis in DM.
    """

    async def _allow_reaction(self, message: Message, reaction: Reaction, member: Member):
        return message.author.id != member.id

    async def _allow_reaction_raw(self, message: Message, reaction: RawReactionActionEvent):
        if not reaction.guild_id:
            return message.author.id != reaction.user_id
        return True


class MessageOwnerReactionFilter(ReactionFilter):
    def __init__(self, original_author_id: int, filters: Optional[ReactionFilter] = None):
        super().__init__(filters)
        self.original_author_id = original_author_id

    @abc.abstractmethod
    async def _allow_reaction_raw(self, message: Message, reaction: RawReactionActionEvent):
        if reaction.guild_id:
            return reaction.member.id == self.original_author_id
        return True
