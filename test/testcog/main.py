import logging

import discord
from redbot.core import commands

from discordmenu.embed.transitions import EmbedTransitions
from discordmenu.menu.closable_menu import ClosableMenuViewState
from discordmenu.menu.listener.menu_listener import MenuListener
from discordmenu.menu.listener.menu_map import MenuMap, MenuMapEntry
from discordmenu.menu.simple_tabbed_menu import SimpleTabbedMenu, SimpleTabbedMenuTransitions
from discordmenu.menu.simple_text_menu import SimpleTextMenu
from discordmenu.menu.view.simple_tabbed_view import SimpleTabbedViewState
from discordmenu.menu.view.simple_text_view import SimpleTextViewState
from .examples.closable_menu import ClosableMenus, ClosableView1Props, ClosableView2Props
from .examples.rich_text_menu import RichTextViewState, RichTextMenu, RichTextMenuTransitions

logger = logging.getLogger('test-bot')

menu_map = MenuMap()
menu_map[SimpleTextMenu.MENU_TYPE] = MenuMapEntry(SimpleTextMenu, EmbedTransitions)
menu_map[SimpleTabbedMenu.MENU_TYPE] = MenuMapEntry(SimpleTabbedMenu, SimpleTabbedMenuTransitions)
menu_map[RichTextMenu.MENU_TYPE] = MenuMapEntry(RichTextMenu, RichTextMenuTransitions)
menu_map[ClosableMenus.MENU_TYPE] = MenuMapEntry(ClosableMenus, EmbedTransitions)


class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.listener = MenuListener(self.bot, menu_map)

    @commands.Cog.listener('on_raw_reaction_add')
    @commands.Cog.listener('on_raw_reaction_remove')
    async def on_raw_reaction_update(self, payload: discord.RawReactionActionEvent):
        await self.listener.on_raw_reaction_update(payload)

    @commands.command(aliases=['t'])
    async def simplemenu(self, ctx):
        vs = SimpleTextViewState("Hello World!")
        await SimpleTextMenu.menu().create(ctx, vs)

    @commands.command(aliases=['t2'])
    async def simpletabbedmenu(self, ctx):
        vs = SimpleTabbedViewState("Initial message.")
        await SimpleTabbedMenu.menu().create(ctx, vs)

    @commands.command(aliases=['t3'])
    async def richtextmenu(self, ctx):
        await RichTextMenu.menu().create(ctx, RichTextViewState())

    @commands.command(aliases=['t4'])
    async def closablemenu(self, ctx, *, query: str = None):
        original_author_id = ctx.message.author.id
        if query == 'type1':
            props = ClosableView1Props("type 1 message.")
            vs = ClosableMenuViewState(original_author_id, ClosableMenus.MENU_TYPE, query, ClosableView1Props.VIEW_TYPE,
                                       props)
            await ClosableMenus.menu().create(ctx, vs)
        elif query == 'type2':
            props = ClosableView2Props("type 2 message.")
            vs = ClosableMenuViewState(original_author_id, ClosableMenus.MENU_TYPE, query, ClosableView2Props.VIEW_TYPE,
                                       props)
            await ClosableMenus.menu().create(ctx, vs)
