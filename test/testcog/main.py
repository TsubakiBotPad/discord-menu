import logging

import discord
from discordmenu.menu.listener.menu_listener import MenuListener
from discordmenu.menu.listener.menu_map import MenuMap, MenuMapEntry
from discordmenu.menu.simple_text_menu import SimpleTextMenu
from discordmenu.menu.view.simple_text_view import SimpleTextViewState
from redbot.core import commands

logger = logging.getLogger('test-bot')

menu_map = MenuMap()
menu_map[SimpleTextMenu.MENU_TYPE] = MenuMapEntry(SimpleTextMenu)


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
