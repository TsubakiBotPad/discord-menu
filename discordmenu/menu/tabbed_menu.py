from typing import Any, Dict, Coroutine, Callable, Union, List
from typing import Optional

from discord import Message

from discordmenu.embed.emoji import EmojiRef
from discordmenu.embed.menu import EmbedMenu
from discordmenu.embed.transitions import EmbedTransitions, EmbedTransition
from discordmenu.embed.view import EmbedView
from discordmenu.embed.view_state import ViewState
from discordmenu.embed.wrapper import EmbedWrapper
from discordmenu.intra_message_state import _IntraMessageState
from discordmenu.menu.base import PMenuable


class TabbedViewState(ViewState):
    MENU_TYPE = "TabbedMenu"

    def __init__(self, original_author_id: int, raw_query: str, menu_id: str, current_index: int, extra_state=None):
        super().__init__(original_author_id, TabbedViewState.MENU_TYPE, raw_query, extra_state=extra_state)
        self.menu_id = menu_id
        self.current_index = current_index

    def serialize(self) -> Dict[str, Any]:
        ret = super().serialize()
        ret.update({
            'menu_id': self.menu_id,
            'current_index': self.current_index,
        })
        return ret

    @classmethod
    async def deserialize(cls, ims: dict) -> "TabbedViewState":
        return cls(ims.get('original_author_id'), ims.get('raw_query'), ims.get('menu_id'), ims.get('current_index'),
                   extra_state=ims)


class TabbedViews:
    DATA: Dict[str, List[Callable[[TabbedViewState], EmbedView]]] = {}

    @classmethod
    def set(cls, menu_id: str, views: Union[List[Callable], Callable]) -> None:
        if type(views) is list:
            cls.DATA[menu_id] = views
        else:
            cls.DATA[menu_id] = [views]

    @classmethod
    def view(cls, menu_id: str, idx: int) -> Callable[[TabbedViewState], EmbedView]:
        return cls.DATA[menu_id][idx]

    @classmethod
    def view_count(cls, menu_id: str):
        return len(cls.DATA[menu_id])


class TabbedMenu(PMenuable[TabbedViewState]):
    MENU_TYPE = TabbedViewState.MENU_TYPE

    @staticmethod
    def menu() -> EmbedMenu:
        return EmbedMenu(TabbedMenuTransitions.transitions(), TabbedMenu.embed)

    @staticmethod
    def respond_to_n_emoji(n: int) -> \
            Optional[Callable[[Optional[Message], _IntraMessageState, Any], Coroutine[None, None, EmbedWrapper]]]:
        async def respond_to_n_inner(message: Optional[Message], ims, **data) -> EmbedWrapper:
            view_state = await TabbedViewState.deserialize(ims)
            view_state.current_index = n - 1
            return TabbedMenu.embed(view_state)

        return respond_to_n_inner

    @staticmethod
    def embed(state: TabbedViewState) -> Optional[EmbedWrapper]:
        if state is None:
            return None
        emojis = TabbedMenuTransitions.emoji_names()
        menu_id = state.menu_id
        view = TabbedViews.view(menu_id, state.current_index)(state)
        n = TabbedViews.view_count(menu_id)
        return EmbedWrapper(view, emojis[:n])


def keycap(n: int):
    if n < 0 or n > 9:
        raise ValueError("n must be between 0 and 9")
    return '{}\N{COMBINING ENCLOSING KEYCAP}'.format(n)


class TabbedMenuTransitions(EmbedTransitions):
    DATA: Dict[EmojiRef, EmbedTransition] = {
        keycap(1): EmbedTransition(keycap(1), TabbedMenu.respond_to_n_emoji(1)),
        keycap(2): EmbedTransition(keycap(2), TabbedMenu.respond_to_n_emoji(2)),
        keycap(3): EmbedTransition(keycap(3), TabbedMenu.respond_to_n_emoji(3)),
        keycap(4): EmbedTransition(keycap(4), TabbedMenu.respond_to_n_emoji(4)),
        keycap(5): EmbedTransition(keycap(5), TabbedMenu.respond_to_n_emoji(5)),
        keycap(6): EmbedTransition(keycap(6), TabbedMenu.respond_to_n_emoji(6)),
        keycap(7): EmbedTransition(keycap(7), TabbedMenu.respond_to_n_emoji(7)),
        keycap(8): EmbedTransition(keycap(8), TabbedMenu.respond_to_n_emoji(8)),
        keycap(9): EmbedTransition(keycap(9), TabbedMenu.respond_to_n_emoji(9)),
    }
