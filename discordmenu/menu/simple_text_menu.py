from typing import Optional, Dict

from discord import Message

from discordmenu.embed.emoji import HOME_EMOJI, EmojiRef
from discordmenu.embed.menu import EmbedMenu
from discordmenu.embed.transitions import EmbedTransitionsBase, EmbedTransition
from discordmenu.embed.wrapper import EmbedWrapper
from discordmenu.menu.view.simple_text_view import SimpleTextViewState, SimpleTextView


class SimpleTextMenu:
    MENU_TYPE = 'SimpleTextMenu'
    message = None

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
        return EmbedWrapper(SimpleTextView.embed(state), [])


class SimpleTextMenuTransitions(EmbedTransitionsBase):
    INITIAL_EMOJI: EmojiRef = HOME_EMOJI
    DATA: Dict[EmojiRef, EmbedTransition] = {
        HOME_EMOJI: EmbedTransition(HOME_EMOJI, SimpleTextMenu.embed_from_message),
    }
