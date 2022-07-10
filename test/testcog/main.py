import logging

import discord
from redbot.core import commands

from discordmenu.embed.transitions import EmbedTransitions
from discordmenu.menu.closable_menu import ClosableMenuViewState
from discordmenu.menu.listener.menu_listener import MenuListener
from discordmenu.menu.listener.menu_map import MenuMap, MenuMapEntry
from discordmenu.menu.scrollable_menu import ScrollableMenu, ScrollableMenuTransitions
from discordmenu.menu.scrollable_menu import ScrollableViewState, ScrollableViews
from discordmenu.menu.simple_tabbed_text_menu import SimpleTabbedTextMenu, SimpleTabbedTextMenuTransitions, \
    SimpleTabbedTextViewState
from discordmenu.menu.simple_text_menu import SimpleTextMenu, SimpleTextViewState
from discordmenu.menu.tabbed_menu import TabbedMenu, TabbedMenuTransitions
from .examples.closable_menu import ClosableMenus, ClosableView1Props, ClosableView2Props
from .examples.rich_text_menu import RichTextViewState, RichTextMenu, RichTextMenuTransitions
from .examples.scrollable_menu import ScrollableView0, ScrollableView1, ScrollableView2
from .examples.tabbed_menu import CustomTabbedViewState

logger = logging.getLogger('test-bot')

menu_map = MenuMap()
menu_map[SimpleTextMenu.MENU_TYPE] = MenuMapEntry(SimpleTextMenu, EmbedTransitions)
menu_map[SimpleTabbedTextMenu.MENU_TYPE] = MenuMapEntry(SimpleTabbedTextMenu, SimpleTabbedTextMenuTransitions)
menu_map[RichTextMenu.MENU_TYPE] = MenuMapEntry(RichTextMenu, RichTextMenuTransitions)
menu_map[ClosableMenus.MENU_TYPE] = MenuMapEntry(ClosableMenus, EmbedTransitions)
menu_map[ScrollableMenu.MENU_TYPE] = MenuMapEntry(ScrollableMenu, ScrollableMenuTransitions)
menu_map[TabbedMenu.MENU_TYPE] = MenuMapEntry(TabbedMenu, TabbedMenuTransitions)


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
    async def SimpleTabbedTextmenu(self, ctx):
        vs = SimpleTabbedTextViewState(
            ["Message 1", "Message 2", "Message 3", "Message 4", "Message 5"], 0)
        await SimpleTabbedTextMenu.menu().create(ctx, vs)

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

    @commands.command(aliases=['t5'])
    async def scrollablemenu(self, ctx):
        ScrollableViews.set('scrollable_menu_example', [ScrollableView0, ScrollableView1, ScrollableView2])
        vs = ScrollableViewState(ctx.message.author.id, '', 'scrollable_menu_example', -1, 0, 3)
        await ScrollableMenu.menu().create(ctx, vs)

    @commands.command(aliases=['t6'])
    async def tabbedmenu(self, ctx):
        vs = CustomTabbedViewState()
        await TabbedMenu.menu().create(ctx, vs)
