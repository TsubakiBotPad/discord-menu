from typing import Iterable, Optional, List, Union

from discord import Reaction, Message, Member, RawReactionActionEvent, Emoji

from discordmenu.embed.emoji import DEFAULT_EMBED_MENU_EMOJI_CONFIG, EmbedMenuEmojiConfig
from discordmenu.emoji.emoji import discord_emoji_to_emoji_name


class ReactionFilter:
    def __init__(self, reaction_filter: Optional["ReactionFilter"] = None):
        self.inner_filter = reaction_filter

    async def allow_reaction(self, message: Message, reaction: Reaction, member: Member) -> bool:
        parent = await self._allow_reaction(message, reaction, member)
        if parent:
            return True

        return await self.inner_filter.allow_reaction(message, reaction, member) if self.inner_filter else False

    async def allow_reaction_raw(self, message: Message, reaction: RawReactionActionEvent) -> bool:
        parent = await self._allow_reaction_raw(message, reaction)
        if parent:
            return True

        return await self.inner_filter.allow_reaction_raw(message, reaction) if self.inner_filter else False

    async def _allow_reaction(self, message: Message, reaction: Reaction, member: Member) -> bool:
        return True

    async def _allow_reaction_raw(self, message: Message, reaction: RawReactionActionEvent) -> bool:
        return True


class ValidEmojiReactionFilter(ReactionFilter):
    def __init__(self, valid_emoji_names: Iterable[Union[str, Emoji]],
                 default_emoji_override: Optional[EmbedMenuEmojiConfig] = None,
                 filters: Optional[ReactionFilter] = None):
        super().__init__(filters)
        default_emojis = default_emoji_override or DEFAULT_EMBED_MENU_EMOJI_CONFIG
        emoji_set = set(default_emojis.to_list())
        emoji_set.update(valid_emoji_names)
        self.valid_emoji_names = list(emoji_set)

    async def _allow_reaction(self, message: Message, reaction: Reaction, member: Member) -> bool:
        valid_emoji_reaction = discord_emoji_to_emoji_name(reaction.emoji) in self.valid_emoji_names
        return valid_emoji_reaction

    async def _allow_reaction_raw(self, message: Message, reaction: RawReactionActionEvent) -> bool:
        valid_emoji_reaction = discord_emoji_to_emoji_name(reaction.emoji) in self.valid_emoji_names
        return valid_emoji_reaction


class BotAuthoredMessageReactionFilter(ReactionFilter):
    """
    This prevents the bot from reacting to messages it didn't post.
    """

    def __init__(self, bot_id: int, filters: Optional[ReactionFilter] = None):
        super().__init__(filters)
        self.bot_id = bot_id

    async def _allow_reaction(self, message: Message, reaction: Reaction, member: Member):
        return message.author.id == self.bot_id

    async def _allow_reaction_raw(self, message: Message, reaction: RawReactionActionEvent):
        return message.author.id == self.bot_id


class NotPosterEmojiReactionFilter(ReactionFilter):
    """
    This prevents the bot from reacting to its own emojis in DM.
    """

    async def _allow_reaction(self, message: Message, reaction: Reaction, member: Member):
        return message.author.id != member.id

    async def _allow_reaction_raw(self, message: Message, reaction: RawReactionActionEvent) -> bool:
        if not reaction.guild_id:
            return message.author.id != reaction.user_id
        return True


class MessageOwnerReactionFilter(ReactionFilter):
    def __init__(self, original_author_id: int, filters: Optional[ReactionFilter] = None):
        super().__init__(filters)
        self.original_author_id = original_author_id

    async def _allow_reaction(self, message: Message, reaction: Reaction, member: Member) -> bool:
        return member.id == self.original_author_id

    async def _allow_reaction_raw(self, message: Message, reaction: RawReactionActionEvent) -> bool:
        if reaction.guild_id:
            return reaction.member.id == self.original_author_id
        return True


class FriendReactionFilter(ReactionFilter):
    def __init__(self, original_author_id: int, friends_ids: List[int], filters: Optional[ReactionFilter] = None):
        super().__init__(filters)
        self.original_author_id = original_author_id
        self.friend_ids = friends_ids

    async def _allow_reaction(self, message: Message, reaction: Reaction, member: Member) -> bool:
        # return await friend_ids(self.original_author_id, member.id)
        return member.id in self.friend_ids

    async def _allow_reaction_raw(self, message: Message, reaction: RawReactionActionEvent) -> bool:
        # return self.friend_ids(self.original_author_id, reaction.member.id)
        return reaction.member.id in self.friend_ids
