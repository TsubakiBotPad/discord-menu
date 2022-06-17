import logging

import discord

from discordmenu.embed.transitions import EmbedTransitions
from discordmenu.menu.listener.menu_listener import MenuListener
from discordmenu.menu.listener.menu_map import MenuMap, MenuMapEntry
from discordmenu.menu.simple_tabbed_menu import SimpleTabbedMenu, SimpleTabbedMenuTransitions
from discordmenu.menu.simple_text_menu import SimpleTextMenu
from discordmenu.menu.view.simple_tabbed_view import SimpleTabbedViewState
from discordmenu.menu.view.simple_text_view import SimpleTextViewState
from redbot.core import commands

logger = logging.getLogger('test-bot')

menu_map = MenuMap()
menu_map[SimpleTextMenu.MENU_TYPE] = MenuMapEntry(SimpleTextMenu, EmbedTransitions)
menu_map[SimpleTabbedMenu.MENU_TYPE] = MenuMapEntry(SimpleTabbedMenu, SimpleTabbedMenuTransitions)


class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.listener = MenuListener(self.bot, menu_map)

    @commands.command(aliases=['t'])
    async def simplemenu(self, ctx, *, member: discord.Member = None):
        vs = SimpleTextViewState("Hello World!")
        await SimpleTextMenu.menu().create(ctx, vs)

    @commands.Cog.listener('on_raw_reaction_add')
    @commands.Cog.listener('on_raw_reaction_remove')
    async def on_raw_reaction_update(self, payload: discord.RawReactionActionEvent):
        await self.listener.on_raw_reaction_update(payload)

    @commands.command(aliases=['t2'])
    async def simpletabbedmenu(self, ctx, *, member: discord.Member = None):
        vs = SimpleTabbedViewState("Initial message.")
        all_emoji = SimpleTabbedMenuTransitions().all_emoji_names()
        print("STMT all_emoji", all_emoji)

        await SimpleTabbedMenu.menu().create(ctx, vs)
