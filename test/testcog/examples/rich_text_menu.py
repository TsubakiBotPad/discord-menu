from typing import Dict
from typing import Optional

from discord import Message

from discordmenu.embed.base import Box
from discordmenu.embed.components import EmbedMain, EmbedThumbnail, EmbedField
from discordmenu.embed.emoji import HOME_EMOJI, EmojiRef
from discordmenu.embed.menu import EmbedMenu
from discordmenu.embed.text import Text, LabeledText
from discordmenu.embed.transitions import EmbedTransitions, EmbedTransition
from discordmenu.embed.view import EmbedView
from discordmenu.embed.view_state import ViewState
from discordmenu.embed.wrapper import EmbedWrapper
from discordmenu.menu.footer import embed_footer_with_state, DEFAULT_ICON_URL


class RichTextViewState(ViewState):
    MENU_TYPE = "RichTextMenu"

    def __init__(self, extra_state=None):
        super().__init__(0, RichTextViewState.MENU_TYPE, "", extra_state=extra_state)

    @classmethod
    async def deserialize(cls, ims: dict) -> "RichTextViewState":
        return cls(extra_state=ims)


class RichTextView(EmbedView):
    def __init__(self, state: RichTextViewState):
        super().__init__(
            EmbedMain(
                color="0x0035e4",
                title="This title links to discord.com",
                url="https://discord.com"),
            embed_thumbnail=EmbedThumbnail(DEFAULT_ICON_URL),
            embed_footer=embed_footer_with_state(state),
            embed_fields=[
                EmbedField(
                    'Subsection ish',
                    Box(
                        Box(
                            Text("Some text here. With emojis:"),
                            Text("\N{HOUSE BUILDING}"),
                            Text("\N{CROSS MARK}"),
                            Text("\N{NO ENTRY SIGN}"),
                            delimiter=' '
                        ),
                        Text("Another row of text."),
                        Text("Anddddd one more."),
                        delimiter='\n'
                    )
                ),
                EmbedField(
                    'Subsection 2 Left',
                    Box(
                        LabeledText('KeyA', 'one'),
                        LabeledText('KeyB', 'two'),
                        LabeledText('KeyC', 'three'),
                    ),
                    inline=True
                ),
                EmbedField(
                    'Subsection 2 Right',
                    Box(
                        LabeledText('KeyD', 'four'),
                        LabeledText('KeyE', 'five'),
                    ),
                    inline=True
                ),
                EmbedField(
                    'Subsection 3',
                    Text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis bibendum mi, ultricies '
                         'hendrerit est. Pellentesque eget molestie magna, vitae pulvinar arcu.')
                ),
            ]

        )


class RichTextMenu:
    MENU_TYPE = RichTextViewState.MENU_TYPE

    @staticmethod
    def menu() -> EmbedMenu:
        return EmbedMenu(RichTextMenuTransitions.transitions(), RichTextMenu.embed)

    @staticmethod
    async def embed_from_message(message: Optional[Message], ims, **data) -> EmbedWrapper:
        view_state = await RichTextViewState.deserialize(ims)
        return RichTextMenu.embed(view_state)

    @staticmethod
    def embed(state: RichTextViewState) -> Optional[EmbedWrapper]:
        if state is None:
            return None
        return EmbedWrapper(RichTextView(state), [])


class RichTextMenuTransitions(EmbedTransitions):
    INITIAL_EMOJI: EmojiRef = HOME_EMOJI
    DATA: Dict[EmojiRef, EmbedTransition] = {
        HOME_EMOJI: EmbedTransition(HOME_EMOJI, RichTextMenu.embed_from_message),
    }
