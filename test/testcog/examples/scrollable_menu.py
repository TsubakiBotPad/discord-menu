from typing import Optional, Dict

from discord import Message

from discordmenu.embed.base import Box
from discordmenu.embed.components import EmbedMain, EmbedField
from discordmenu.embed.emoji import EmojiRef
from discordmenu.embed.menu import EmbedMenu
from discordmenu.embed.text import Text
from discordmenu.embed.transitions import EmbedTransitions, EmbedTransition
from discordmenu.embed.view import EmbedView
from discordmenu.embed.view_state import ViewState
from discordmenu.embed.wrapper import EmbedWrapper
from discordmenu.menu.base import PMenuableCM
from discordmenu.menu.footer import embed_footer_with_state


class ScrollableMenuViewState(ViewState):
    MENU_TYPE = 'ScrollableMenu'

    def __init__(self, original_author_id: int, menu_type: str, raw_query: str, current_pane_num: int,
                 prev_pane_num: int, total_pages: int):
        super().__init__(original_author_id, menu_type, raw_query)
        self.total_pages = total_pages
        self.prev_pane_num = prev_pane_num
        self.current_pane_num = current_pane_num

    def serialize(self):
        ret = super().serialize()
        ret.update({
            'total_pages': self.total_pages,
            'prev_pane_num': self.prev_pane_num,
            'current_pane_num': self.current_pane_num,
        })
        return ret

    @classmethod
    async def deserialize(cls, ims: dict) -> "ScrollableMenuViewState":
        original_author_id = ims['original_author_id']
        menu_type = ims['menu_type']
        raw_query = ims['raw_query']
        current_pane_num = ims['current_pane_num']
        prev_pane_num = ims['prev_pane_num']
        total_pages = ims['total_pages']
        return ScrollableMenuViewState(original_author_id, menu_type, raw_query, current_pane_num, prev_pane_num,
                                       total_pages)


class ScrollableView0(EmbedView):
    def __init__(self, state: ScrollableMenuViewState):
        super().__init__(
            EmbedMain(),
            embed_footer=embed_footer_with_state(state),
            embed_fields=[
                EmbedField(
                    'Scrollable View Type 0',
                    Box(
                        Text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis bibendum mi, ultricies '
                             'hendrerit est. Pellentesque eget molestie magna, vitae pulvinar arcu.'),
                        Text('Navigated from pane {}'.format(state.prev_pane_num))
                    )
                ),
            ]
        )


class ScrollableView1(EmbedView):
    def __init__(self, state: ScrollableMenuViewState):
        super().__init__(
            EmbedMain(),
            embed_footer=embed_footer_with_state(state),
            embed_fields=[
                EmbedField(
                    'Scrollable View Type 1',
                    Box(
                        Text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis bibendum mi, ultricies '
                             'hendrerit est. Pellentesque eget molestie magna, vitae pulvinar arcu.'),
                        Text('Navigated from pane {}'.format(state.prev_pane_num))
                    )
                ),
            ]
        )


class ScrollableView2(EmbedView):
    def __init__(self, state: ScrollableMenuViewState):
        super().__init__(
            EmbedMain(),
            embed_footer=embed_footer_with_state(state),
            embed_fields=[
                EmbedField(
                    'Scrollable View Type 2',
                    Box(
                        Text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis bibendum mi, ultricies '
                             'hendrerit est. Pellentesque eget molestie magna, vitae pulvinar arcu.'),
                        Text('Navigated from pane {}'.format(state.prev_pane_num))
                    )
                ),
            ]
        )


class ScrollableMenu(PMenuableCM[ScrollableMenuViewState]):
    MENU_TYPE = ScrollableMenuViewState.MENU_TYPE
    pane_num_to_view_constructor = {
        0: ScrollableView0,
        1: ScrollableView1,
        2: ScrollableView2,
    }

    @classmethod
    def menu(cls):
        return EmbedMenu(ScrollableMenuTransitions.transitions(), ScrollableMenu.embed)

    @classmethod
    def embed(cls, state: ScrollableMenuViewState):
        return EmbedWrapper(ScrollableView1(state), ScrollableMenuTransitions.emoji_names())

    @classmethod
    async def respond_with_left(cls, message: Optional[Message], ims, **data) -> EmbedWrapper:
        state = await ScrollableMenuViewState.deserialize(ims)

        current_pane_num: int = state.current_pane_num
        state.prev_pane_num = current_pane_num
        next_pane_num = (current_pane_num - 1) % state.total_pages
        state.current_pane_num = next_pane_num

        return ScrollableMenu.get_embed_view_by_pane_num(next_pane_num, state)

    @classmethod
    async def respond_with_right(cls, message: Optional[Message], ims, **data) -> EmbedWrapper:
        state = await ScrollableMenuViewState.deserialize(ims)

        current_pane_num: int = state.current_pane_num
        state.prev_pane_num = current_pane_num
        next_pane_num = (current_pane_num + 1) % state.total_pages
        state.current_pane_num = next_pane_num

        return ScrollableMenu.get_embed_view_by_pane_num(next_pane_num, state)

    @classmethod
    def get_embed_view_by_pane_num(cls, pane_num: int, state: ScrollableMenuViewState) -> EmbedWrapper:
        view_constructor = cls.pane_num_to_view_constructor[pane_num]
        view = view_constructor(state)
        return EmbedWrapper(view, ScrollableMenuTransitions.emoji_names())


class ScrollableMenuTransitions(EmbedTransitions):
    LEFT = '\N{BLACK LEFT-POINTING TRIANGLE}'
    RIGHT = '\N{BLACK RIGHT-POINTING TRIANGLE}'

    DATA: Dict[EmojiRef, EmbedTransition] = {
        LEFT: EmbedTransition(LEFT, ScrollableMenu.respond_with_left),
        RIGHT: EmbedTransition(RIGHT, ScrollableMenu.respond_with_right),
    }
