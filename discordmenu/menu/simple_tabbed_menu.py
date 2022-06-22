from typing import Any, Dict, List
from typing import Optional

from discord import Message

from discordmenu.embed.components import EmbedMain
from discordmenu.embed.emoji import EmojiRef
from discordmenu.embed.menu import EmbedMenu
from discordmenu.embed.transitions import EmbedTransitions, EmbedTransition
from discordmenu.embed.view import EmbedView
from discordmenu.embed.view_state import ViewState
from discordmenu.embed.wrapper import EmbedWrapper
from discordmenu.menu.base import PMenuable
from discordmenu.menu.footer import embed_footer_with_state


class SimpleTabbedViewState(ViewState):
    MENU_TYPE = "SimpleTabbedMenu"

    def __init__(self, messages: List[str], current_index: int, extra_state=None):
        super().__init__(0, SimpleTabbedViewState.MENU_TYPE, "", extra_state=extra_state)
        self.current_index = current_index
        self.messages = messages

    def serialize(self) -> Dict[str, Any]:
        ret = super().serialize()
        ret.update({
            'messages': self.messages,
            'current_index': self.current_index,
        })
        return ret

    @classmethod
    async def deserialize(cls, ims: dict) -> "SimpleTabbedViewState":
        return cls(ims.get('messages'), ims.get('current_index'), extra_state=ims)


class SimpleTabbedView(EmbedView):
    def __init__(self, state: SimpleTabbedViewState):
        super().__init__(
            EmbedMain(description=state.messages[state.current_index]),
            embed_footer=embed_footer_with_state(state)
        )


class SimpleTabbedMenu(PMenuable[SimpleTabbedViewState]):
    MENU_TYPE = SimpleTabbedViewState.MENU_TYPE

    @staticmethod
    def menu() -> EmbedMenu:
        return EmbedMenu(SimpleTabbedMenuTransitions.transitions(), SimpleTabbedMenu.embed)

    @staticmethod
    async def respond_to_1(message: Optional[Message], ims, **data) -> EmbedWrapper:
        view_state = await SimpleTabbedViewState.deserialize(ims)
        view_state.current_index = 0
        return SimpleTabbedMenu.embed(view_state)

    @staticmethod
    async def respond_to_2(message: Optional[Message], ims, **data) -> EmbedWrapper:
        view_state = await SimpleTabbedViewState.deserialize(ims)
        view_state.current_index = 1
        return SimpleTabbedMenu.embed(view_state)

    @staticmethod
    async def respond_to_3(message: Optional[Message], ims, **data) -> EmbedWrapper:
        view_state = await SimpleTabbedViewState.deserialize(ims)
        view_state.current_index = 2
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
