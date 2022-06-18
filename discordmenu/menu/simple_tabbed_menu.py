from typing import Optional, Dict

from discord import Message

from discordmenu.embed.emoji import EmojiRef
from discordmenu.embed.menu import EmbedMenu
from discordmenu.embed.transitions import EmbedTransitions, EmbedTransition
from discordmenu.embed.wrapper import EmbedWrapper
from discordmenu.menu.base import PMenuable
from discordmenu.menu.view.simple_tabbed_view import SimpleTabbedViewState, SimpleTabbedView


class SimpleTabbedMenu(PMenuable[SimpleTabbedViewState]):
    MENU_TYPE = SimpleTabbedViewState.MENU_TYPE

    @staticmethod
    def menu() -> EmbedMenu:
        return EmbedMenu(SimpleTabbedMenuTransitions.transitions(), SimpleTabbedMenu.embed)

    @staticmethod
    async def respond_to_1(message: Optional[Message], ims, **data) -> EmbedWrapper:
        view_state = await SimpleTabbedViewState.deserialize(ims)
        view_state.message = "This is message 1."
        return SimpleTabbedMenu.embed(view_state)

    @staticmethod
    async def respond_to_2(message: Optional[Message], ims, **data) -> EmbedWrapper:
        view_state = await SimpleTabbedViewState.deserialize(ims)
        view_state.message = "This is message 2."
        return SimpleTabbedMenu.embed(view_state)

    @staticmethod
    async def respond_to_3(message: Optional[Message], ims, **data) -> EmbedWrapper:
        view_state = await SimpleTabbedViewState.deserialize(ims)
        view_state.message = "This is message 3."
        return SimpleTabbedMenu.embed(view_state)

    @staticmethod
    def embed(state: SimpleTabbedViewState) -> Optional[EmbedWrapper]:
        if state is None:
            return None
        return EmbedWrapper(SimpleTabbedView(state), SimpleTabbedMenuTransitions.emoji_names())


class SimpleTabbedMenuTransitions(EmbedTransitions):
    ONE = '1\N{COMBINING ENCLOSING KEYCAP}'
    TWO = '2\N{COMBINING ENCLOSING KEYCAP}'
    THREE = '3\N{COMBINING ENCLOSING KEYCAP}'

    DATA: Dict[EmojiRef, EmbedTransition] = {
        ONE: EmbedTransition(ONE, SimpleTabbedMenu.respond_to_1),
        TWO: EmbedTransition(TWO, SimpleTabbedMenu.respond_to_2),
        THREE: EmbedTransition(THREE, SimpleTabbedMenu.respond_to_3),
    }
