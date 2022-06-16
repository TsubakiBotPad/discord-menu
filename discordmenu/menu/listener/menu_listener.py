import logging
from copy import deepcopy
from typing import Optional

import discord

from discordmenu.embed.emoji import DEFAULT_EMOJI_LIST
from discordmenu.intra_message_state import IntraMessageState
from discordmenu.menu.listener.bot_protocol import BotSupportsMenus
from discordmenu.menu.listener.errors import DiscordRatelimitFilter, MissingImsMenuType, InvalidImsMenuType, \
    CogNotLoaded
from discordmenu.menu.listener.menu_map import MenuMap
from discordmenu.menu.listener.reaction_filter_list import ReactionFilterList
from discordmenu.reaction_filter import ValidEmojiReactionFilter, BotAuthoredMessageReactionFilter, \
    MessageOwnerReactionFilter, NotPosterEmojiReactionFilter

logger = logging.getLogger('discordmenu.menu_listener')
logger.addFilter(DiscordRatelimitFilter())


class MenuListener:
    def __init__(self, discord_bot: BotSupportsMenus, menu_map: Optional[MenuMap] = None,
                 reaction_filters: Optional[ReactionFilterList] = None):
        super().__init__()
        self.bot = discord_bot
        self.menu_map: MenuMap = menu_map if menu_map else MenuMap()
        self.reaction_filters: ReactionFilterList = reaction_filters if reaction_filters else ReactionFilterList()

    @staticmethod
    def _emoji_was_removed_in_public_channel(channel, payload: discord.RawReactionActionEvent):
        return payload.event_type == "REACTION_REMOVE" and not isinstance(channel, discord.DMChannel)

    async def _fetch_message(self, channel, payload):
        message = discord.utils.get(self.bot.cached_messages, id=payload.message_id)
        if message is None:
            message = await channel.fetch_message(payload.message_id)
        return message

    def _message_is_not_authored_by_bot(self, message):
        return message.author != self.bot.user

    def _get_emoji_clicked(self, payload: discord.RawReactionActionEvent) -> Optional[str]:
        emoji_obj = payload.emoji
        if isinstance(emoji_obj, str):
            emoji_clicked = emoji_obj
        else:
            emoji_clicked = emoji_obj.name

        # determine if this is potentially a valid reaction prior to doing any network call:
        # this is true if it's a default emoji or in any of our global panes emoji lists
        if emoji_clicked in DEFAULT_EMOJI_LIST:
            return emoji_clicked
        for menu_type, menu_entry in self.menu_map.items():
            if emoji_clicked in menu_entry.transition.all_emoji_names():
                return emoji_clicked
        return None

    def _event_is_not_relevant(self, payload: discord.RawReactionActionEvent):
        emoji_clicked = self._get_emoji_clicked(payload)
        if emoji_clicked is None:
            return True, None

        channel = self.bot.get_channel(payload.channel_id)

        if self._emoji_was_removed_in_public_channel(channel, payload):
            return True, None

        message = await self._fetch_message(channel, payload)

        if self._message_is_not_authored_by_bot(message):
            return True, None

        reaction = discord.utils.find((lambda r:
                                       r.emoji == payload.emoji.name
                                       if payload.emoji.is_unicode_emoji()
                                       else r.emoji == payload.emoji),
                                      message.reactions)
        if reaction is None:
            return True, None

        member = payload.member or self.bot.get_user(payload.user_id)

        ims = message.embeds and IntraMessageState.extract_data(message.embeds[0])
        if not ims:
            return True, None

        return False, (emoji_clicked, channel, message, reaction, member, ims)

    async def on_raw_reaction_update(self, payload: discord.RawReactionActionEvent):
        """
        This function responds to Discord's RawReactionActionEvent to update menus.

        For Discord Red, apply this function to a listener decorated with:
        @commands.Cog.listener('on_raw_reaction_add')
        @commands.Cog.listener('on_raw_reaction_remove')
        """
        event_is_not_relevant, obj_tuple = self._event_is_not_relevant(payload)
        if event_is_not_relevant:
            return

        emoji_clicked, channel, message, reaction, member, ims = obj_tuple
        cog_name, menu, panes = self.get_menu_attributes(ims)
        reaction_filters = self.get_reaction_filters(ims)
        if not (await menu.should_respond(message, reaction, reaction_filters, member)):
            return

        try:
            data = await self.get_menu_context(ims)
        except CogNotLoaded:
            return

        data.update({
            'reaction': emoji_clicked
        })

        await menu.transition(message, deepcopy(ims), emoji_clicked, member, **data)
        await self.listener_respond_with_child(deepcopy(ims), message, emoji_clicked, member)

    async def listener_respond_with_child(self, menu_1_ims, message_1, emoji_clicked, member):
        failsafe = 0

        while menu_1_ims.get('child_message_id'):
            if failsafe == 10:
                break
            failsafe += 1
            _, _, panes_class_1 = self.get_menu_attributes(menu_1_ims)
            child_data_func = panes_class_1.get_child_data_func(emoji_clicked)
            try:
                data = await self.get_menu_context(menu_1_ims)
            except CogNotLoaded:
                return
            emoji_simulated_clicked_2, extra_ims = None, {}
            if child_data_func is not None:
                emoji_simulated_clicked_2, extra_ims = await child_data_func(menu_1_ims, emoji_clicked, **data)
            if emoji_simulated_clicked_2 is not None:
                fctx = await self.bot.get_context(message_1)
                try:
                    message_2 = await fctx.fetch_message(int(menu_1_ims['child_message_id']))
                    menu_2_ims = message_2.embeds and IntraMessageState.extract_data(message_2.embeds[0])
                    menu_2_ims.update(extra_ims)
                    _, menu_2, _ = self.get_menu_attributes(menu_2_ims)
                    await menu_2.transition(message_2, menu_2_ims, emoji_simulated_clicked_2, member, **data)
                except discord.errors.NotFound:
                    break
                menu_1_ims = menu_2_ims
                message_1 = message_2

    def get_reaction_filters(self, ims: dict):
        """
        User should override this if they want to change the existing filters
        """
        cog_name, menu, panes = self.get_menu_attributes(ims)
        reaction_filters = [
            ValidEmojiReactionFilter(panes.all_emoji_names()),
            NotPosterEmojiReactionFilter(),
            BotAuthoredMessageReactionFilter(self.bot.user.id),
            MessageOwnerReactionFilter(ims['original_author_id'])
        ]
        additional_filters = self.get_additional_reaction_filters(ims)
        return reaction_filters + additional_filters

    def get_additional_reaction_filters(self, ims: dict):
        """
        User should override this if they want to add additional filters on top of the base set
        """
        return []

    async def get_menu_context(self, ims):
        menu_entry = self.get_menu_attributes(ims)

        # Get base data from cog assuming it has a function called get_menu_context.
        # This is for a cog to pass data from the cog to the menu if it's needed during a menu transition.
        cog_name = menu_entry.cog_name
        cog = self.bot.get_cog(cog_name)
        if cog is None:
            raise CogNotLoaded(f"Cog {cog_name} is unloaded.")
        if hasattr(cog, "get_menu_context"):
            return await cog.get_menu_context(ims)
        return {}

    def get_menu_attributes(self, ims):
        menu_type = ims.get('menu_type')
        if menu_type is None:
            raise MissingImsMenuType("Missing IMS menu type")
        if menu_type not in self.menu_map:
            raise InvalidImsMenuType(f"Invalid IMS menu type: {menu_type}")
        return self.menu_map[menu_type]
