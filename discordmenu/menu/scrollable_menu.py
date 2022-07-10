from typing import Any, Dict, Callable, Union, List
from typing import Optional

from discord import Message

from discordmenu.embed.emoji import EmojiRef
from discordmenu.embed.menu import EmbedMenu
from discordmenu.embed.transitions import EmbedTransitions, EmbedTransition
from discordmenu.embed.view import EmbedView
from discordmenu.embed.view_state import ViewState
from discordmenu.embed.wrapper import EmbedWrapper
from discordmenu.menu.base import PMenuable


class ScrollableViewState(ViewState):
    MENU_TYPE = "ScrollableMenu"

    def __init__(self, original_author_id: int, raw_query: str, menu_id: str, prev_pane_num: int, current_pane_num: int,
                 num_pages: int, extra_state=None):
        super().__init__(original_author_id, ScrollableViewState.MENU_TYPE, raw_query, extra_state=extra_state)
        self.menu_id = menu_id
        self.prev_pane_num = prev_pane_num,
        self.current_pane_num = current_pane_num
        self.num_pages = num_pages

    def serialize(self) -> Dict[str, Any]:
        ret = super().serialize()
        ret.update({
            'menu_id': self.menu_id,
            'prev_pane_num': self.prev_pane_num,
            'current_pane_num': self.current_pane_num,
            'num_pages': self.num_pages,
        })
        return ret

    @classmethod
    async def deserialize(cls, ims: dict) -> "ScrollableViewState":
        return cls(ims.get('original_author_id'), ims.get('raw_query'), ims.get('menu_id'), ims.get('prev_pane_num'),
                   ims.get('current_pane_num'), ims.get('num_pages'), extra_state=ims)


class ScrollableViews:
    DATA: Dict[str, List[Callable[[ScrollableViewState], EmbedView]]] = {}

    @classmethod
    def set(cls, menu_id: str, views: Union[List[Callable], Callable]) -> None:
        if type(views) is list:
            cls.DATA[menu_id] = views
        else:
            cls.DATA[menu_id] = [views]

    @classmethod
    def view(cls, menu_id: str, idx: int) -> Callable[[ScrollableViewState], EmbedView]:
        return cls.DATA[menu_id][idx]

    @classmethod
    def view_count(cls, menu_id: str):
        return len(cls.DATA[menu_id])


class ScrollableMenu(PMenuable[ScrollableViewState]):
    MENU_TYPE = ScrollableViewState.MENU_TYPE

    @staticmethod
    def menu() -> EmbedMenu:
        return EmbedMenu(ScrollableMenuTransitions.transitions(), ScrollableMenu.embed)

    @staticmethod
    async def respond_to_left(message: Optional[Message], ims, **data) -> EmbedWrapper:
        state = await ScrollableViewState.deserialize(ims)

        next_pane_num = (state.current_pane_num - 1) % state.num_pages
        state.prev_pane_num = state.current_pane_num
        state.current_pane_num = next_pane_num

        return ScrollableMenu.embed(state)

    @staticmethod
    async def respond_to_right(message: Optional[Message], ims, **data) -> EmbedWrapper:
        state = await ScrollableViewState.deserialize(ims)

        next_pane_num = (state.current_pane_num + 1) % state.num_pages
        state.prev_pane_num = state.current_pane_num
        state.current_pane_num = next_pane_num

        return ScrollableMenu.embed(state)

    @staticmethod
    def embed(state: ScrollableViewState) -> Optional[EmbedWrapper]:
        if state is None:
            return None
        emojis = ScrollableMenuTransitions.emoji_names()
        menu_id = state.menu_id
        view = ScrollableViews.view(menu_id, state.current_pane_num)(state)
        n = ScrollableViews.view_count(menu_id)
        return EmbedWrapper(view, emojis[:n])


class ScrollableMenuTransitions(EmbedTransitions):
    left_arrow = '\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}'
    right_arrow = '\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}'

    DATA: Dict[EmojiRef, EmbedTransition] = {
        left_arrow: EmbedTransition(left_arrow, ScrollableMenu.respond_to_left),
        right_arrow: EmbedTransition(right_arrow, ScrollableMenu.respond_to_right),
    }
