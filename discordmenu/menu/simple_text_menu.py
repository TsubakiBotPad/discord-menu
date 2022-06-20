from typing import Any, Dict
from typing import Optional

from discord import Message

from discordmenu.embed.components import EmbedMain
from discordmenu.embed.emoji import HOME_EMOJI, EmojiRef
from discordmenu.embed.menu import EmbedMenu
from discordmenu.embed.transitions import EmbedTransitions, EmbedTransition
from discordmenu.embed.view import EmbedView
from discordmenu.embed.view_state import ViewState
from discordmenu.embed.wrapper import EmbedWrapper
from discordmenu.menu.base import PMenuable
from discordmenu.menu.footer import embed_footer_with_state


class SimpleTextViewState(ViewState):
    MENU_TYPE = "SimpleTextMenu"

    def __init__(self, message, extra_state=None):
        super().__init__(0, SimpleTextViewState.MENU_TYPE, "", extra_state=extra_state)
        self.message = message

    def serialize(self) -> Dict[str, Any]:
        ret = super().serialize()
        ret.update({
            'message': self.message
        })
        return ret

    @classmethod
    async def deserialize(cls, ims: dict) -> "SimpleTextViewState":
        return cls(ims.get('message'), extra_state=ims)


class SimpleTextView(EmbedView):
    def __init__(self, state: SimpleTextViewState):
        super().__init__(
            EmbedMain(description=state.message),
            embed_footer=embed_footer_with_state(state)
        )


class SimpleTextMenu(PMenuable[SimpleTextViewState]):
    MENU_TYPE = SimpleTextViewState.MENU_TYPE

    @staticmethod
    def menu() -> EmbedMenu:
        return EmbedMenu(SimpleTextMenuTransitions.transitions(), SimpleTextMenu.embed)

    @staticmethod
    async def embed_from_message(message: Optional[Message], ims, **data) -> EmbedWrapper:
        view_state = await SimpleTextViewState.deserialize(ims)
        return SimpleTextMenu.embed(view_state)

    @staticmethod
    def embed(state: SimpleTextViewState) -> Optional[EmbedWrapper]:
        if state is None:
            return None
        return EmbedWrapper(SimpleTextView(state), [])


class SimpleTextMenuTransitions(EmbedTransitions):
    INITIAL_EMOJI: EmojiRef = HOME_EMOJI
    DATA: Dict[EmojiRef, EmbedTransition] = {
        HOME_EMOJI: EmbedTransition(HOME_EMOJI, SimpleTextMenu.embed_from_message),
    }
