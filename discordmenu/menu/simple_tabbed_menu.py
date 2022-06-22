from typing import Any, Dict, List, Coroutine, Callable
from typing import Optional

from discord import Message

from discordmenu.embed.components import EmbedMain
from discordmenu.embed.emoji import EmojiRef
from discordmenu.embed.menu import EmbedMenu
from discordmenu.embed.transitions import EmbedTransitions, EmbedTransition
from discordmenu.embed.view import EmbedView
from discordmenu.embed.view_state import ViewState
from discordmenu.embed.wrapper import EmbedWrapper
from discordmenu.intra_message_state import _IntraMessageState
from discordmenu.menu.base import PMenuable
from discordmenu.menu.footer import embed_footer_with_state


class SimpleTabbedViewState(ViewState):
    MENU_TYPE = "SimpleTabbedMenu"

    def __init__(self, messages: List[str], current_index: int, extra_state=None):
        super().__init__(0, SimpleTabbedViewState.MENU_TYPE, "", extra_state=extra_state)
        self.current_index = current_index
        self.messages = messages

        reaction_count = len(SimpleTabbedMenuTransitions.DATA)
        if len(messages) > reaction_count:
            raise ValueError("SimpleTabbedMenu only supports up to {} tabs. Write a custom menu or extend "
                             "SimpleTabbedMenuTransitions.DATA for more.".format(reaction_count))

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
    def respond_to_n_emoji(n: int) -> \
            Optional[Callable[[Optional[Message], _IntraMessageState, Any], Coroutine[None, None, EmbedWrapper]]]:
        async def respond_to_n_inner(message: Optional[Message], ims, **data) -> EmbedWrapper:
            view_state = await SimpleTabbedViewState.deserialize(ims)
            view_state.current_index = n - 1
            return SimpleTabbedMenu.embed(view_state)

        return respond_to_n_inner

    @staticmethod
    def embed(state: SimpleTabbedViewState) -> Optional[EmbedWrapper]:
        if state is None:
            return None
        emojis = SimpleTabbedMenuTransitions.emoji_names()
        n = len(state.messages)
        return EmbedWrapper(SimpleTabbedView(state), emojis[:n])


def keycap(n: int):
    if n < 0 or n > 9:
        raise ValueError("n must be between 0 and 9")
    return '{}\N{COMBINING ENCLOSING KEYCAP}'.format(n)


class SimpleTabbedMenuTransitions(EmbedTransitions):
    DATA: Dict[EmojiRef, EmbedTransition] = {
        keycap(1): EmbedTransition(keycap(1), SimpleTabbedMenu.respond_to_n_emoji(1)),
        keycap(2): EmbedTransition(keycap(2), SimpleTabbedMenu.respond_to_n_emoji(2)),
        keycap(3): EmbedTransition(keycap(3), SimpleTabbedMenu.respond_to_n_emoji(3)),
        keycap(4): EmbedTransition(keycap(4), SimpleTabbedMenu.respond_to_n_emoji(4)),
        keycap(5): EmbedTransition(keycap(5), SimpleTabbedMenu.respond_to_n_emoji(5)),
        keycap(6): EmbedTransition(keycap(6), SimpleTabbedMenu.respond_to_n_emoji(6)),
        keycap(7): EmbedTransition(keycap(7), SimpleTabbedMenu.respond_to_n_emoji(7)),
        keycap(8): EmbedTransition(keycap(8), SimpleTabbedMenu.respond_to_n_emoji(8)),
        keycap(9): EmbedTransition(keycap(9), SimpleTabbedMenu.respond_to_n_emoji(9)),
    }
