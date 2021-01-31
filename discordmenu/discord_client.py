import asyncio
from typing import Dict, List, Optional

from discord import Embed, Emoji, Forbidden, Message
from discordmenu.embed.control import EmbedControl
from discordmenu.emoji_cache import emoji_cache


async def update_message(message: Message, updated_messaged_contents, guild_message: bool,
                         emoji_diff: Dict[str, List[Emoji]] = None):
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


async def remove_reaction(message: Message, emoji, user_id):
    if not message.guild:
        # bots don't have permission to delete reactions in DM. So check if theres a guild associated before attempting.
        return

    member = message.guild.get_member(user_id)

    try:
        await message.remove_reaction(emoji, member)
    except Forbidden:
        pass


async def send_embed_control(ctx, embed_control: "EmbedControl"):
    new_embed = embed_control.embed_views[0].to_embed()
    message = await ctx.send(embed=new_embed)

    emoji_to_add = [emoji_cache.get_by_name(e) for e in embed_control.emoji_buttons]
    add = [message.add_reaction(e) for e in emoji_to_add]
    await asyncio.gather(*add)


async def update_embed_control(message: Message, next_embed_control: Optional["EmbedControl"], emoji_diff: Dict):
    guild_message = bool(message.guild)

    if not next_embed_control:
        await message.delete()

    updated_message_contents = next_embed_control.embed_views[0].to_embed()
    await message.edit(embed=updated_message_contents)

    if emoji_diff:
        add = [message.add_reaction(e) for e in emoji_diff.get('add', [])]
        await asyncio.gather(*add)

        if guild_message:
            remove = [message.clear_reaction(e) for e in emoji_diff.get('remove', [])]
            await asyncio.gather(*remove)


def diff_emojis(message: Message, next_embed_control: Optional["EmbedControl"]):
    current_emojis = [e.emoji for e in message.reactions]
    next_emojis = next_embed_control.emoji_buttons

    return {
        'add': [e for e in next_emojis if e not in current_emojis],
        'remove': [e for e in current_emojis if e not in next_emojis],
    }
