import asyncio
from typing import Dict, List, Optional, Union, Sequence

from discord import Embed, Emoji, Forbidden, Message
from discord import NotFound, AutoShardedClient
from discord.ext.commands import Context

from discordmenu.embed.wrapper import EmbedWrapper
from discordmenu.embed.view import EmbedView
from discordmenu.emoji.emoji_cache import emoji_cache


async def update_message(message: Message, updated_messaged_contents, guild_message: bool,
                         emoji_diff: Optional[Dict[str, List[Union[str, Emoji]]]] = None) -> None:
    if isinstance(updated_messaged_contents, Embed):
        await message.edit(embed=updated_messaged_contents)
    else:
        await message.edit(content=updated_messaged_contents)
    if emoji_diff:
        add = [message.add_reaction(e) for e in emoji_diff.get('add', [])]
        await asyncio.gather(*add)

        if guild_message:
            remove = [message.clear_reaction(e) for e in emoji_diff.get('remove', [])]
            await asyncio.gather(*remove)


async def remove_reaction(message: Message, emoji: str, user_id: int) -> None:
    if not message.guild:
        # bots don't have permission to delete reactions in DM. So check if theres a guild associated before attempting.
        return

    member = message.guild.get_member(user_id)

    try:
        # support custom emojis
        await message.remove_reaction(emoji_cache.get_raw_emoji(emoji), member)
    except Forbidden:
        pass


async def send_embed(ctx: Context, embed_wrapper: EmbedWrapper, message: Optional[Message] = None) -> Message:
    if not issubclass(type(embed_wrapper.embed_view), EmbedView):
        raise TypeError("Check return type of your View, an EmbedView is not being returned")
    new_embed = embed_wrapper.embed_view.to_embed()
    if message is None:
        message = await ctx.send(embed=new_embed)
    else:
        await message.edit(embed=new_embed)

    emoji_to_add = [emoji_cache.get_by_name(e) for e in embed_wrapper.emoji_buttons]
    add = [message.add_reaction(e) for e in emoji_to_add]
    try:
        await asyncio.gather(*add)
    except NotFound:
        # if messsage is deleted early
        pass
    return message


async def update_embed(message: Message, next_embed: EmbedWrapper,
                       emoji_diff: Dict[str, List[Union[Emoji, str]]]) -> None:
    guild_message = bool(message.guild)

    if not next_embed:
        await message.delete()

    updated_message_contents = next_embed.embed_view.to_embed()
    await message.edit(embed=updated_message_contents)

    if emoji_diff:
        add = [message.add_reaction(e) for e in emoji_diff.get('add', [])]
        try:
            await asyncio.gather(*add)
        except NotFound:
            # if messsage is deleted early
            pass

        if guild_message:
            remove = [message.clear_reaction(e) for e in emoji_diff.get('remove', [])]
            try:
                await asyncio.gather(*remove)
            except NotFound:
                # if messsage is deleted early
                pass


def diff_emojis(message: Message, next_embed: EmbedWrapper) -> Dict[str, List[Union[str, Emoji]]]:
    current_emojis = [e.emoji for e in message.reactions]
    next_emojis = next_embed.emoji_buttons
    return diff_emojis_raw(current_emojis, next_emojis)


def diff_emojis_raw(current_emojis: List[Union[str, Emoji]], next_emojis: List[Union[str, Emoji]]) \
        -> Dict[str, List[Union[str, Emoji]]]:
    add = sorted(
        set(e for e in next_emojis if e and not emoji_matches(e, current_emojis)),
        key=lambda x: next_emojis.index(x))
    remove = list(set(e for e in current_emojis if e and not emoji_matches(e, next_emojis)))
    return {
        'add': [emoji_cache.get_by_name(e) for e in add],
        'remove': remove,
    }


def emoji_matches(emoji: Union[str, Emoji, Sequence[Union[str, Emoji]]],
                  emoji_to_match: List[Union[str, Emoji]]) -> bool:
    if isinstance(emoji, tuple) or isinstance(emoji, list):
        # handle case of fallback emojis
        return any(emoji_matches(e, emoji_to_match) for e in emoji)
    # handle case of custom emojis as well as normal unicode emojis
    if isinstance(emoji, Emoji):
        emoji = emoji.name
    emoji_to_match = [e.name if isinstance(e, Emoji) else e for e in emoji_to_match]
    return emoji in emoji_to_match
