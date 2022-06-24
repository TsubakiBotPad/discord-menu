from discordmenu.embed.base import Box
from discordmenu.embed.components import EmbedMain, EmbedField
from discordmenu.embed.text import Text
from discordmenu.embed.view import EmbedView
from discordmenu.menu.footer import embed_footer_with_state
from discordmenu.menu.tabbed_menu import TabbedViewState, TabbedViews

CUSTOM_MENU_ID = "TabbedMenu1"


class CustomTabbedViewState(TabbedViewState):
    def __init__(self, initial_pane: int = 0, extra_state=None):
        super().__init__(0, "", CUSTOM_MENU_ID, initial_pane, extra_state=extra_state)

    @classmethod
    async def deserialize(cls, ims: dict) -> "CustomTabbedViewState":
        return cls(extra_state=ims)


class TabbedView0(EmbedView):
    def __init__(self, state: CustomTabbedViewState):
        super().__init__(
            EmbedMain(),
            embed_footer=embed_footer_with_state(state),
            embed_fields=[
                EmbedField(
                    'Tabbed View Type 0',
                    Box(
                        Text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis bibendum mi, ultricies '
                             'hendrerit est. Pellentesque eget molestie magna, vitae pulvinar arcu.'),
                    )
                ),
            ]
        )


class TabbedView1(EmbedView):
    def __init__(self, state: CustomTabbedViewState):
        super().__init__(
            EmbedMain(),
            embed_footer=embed_footer_with_state(state),
            embed_fields=[
                EmbedField(
                    'Tabbed View Type 1',
                    Box(
                        Text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis bibendum mi, ultricies '
                             'hendrerit est. Pellentesque eget molestie magna, vitae pulvinar arcu.'),
                    )
                ),
            ]
        )


class TabbedView2(EmbedView):
    def __init__(self, state: CustomTabbedViewState):
        super().__init__(
            EmbedMain(),
            embed_footer=embed_footer_with_state(state),
            embed_fields=[
                EmbedField(
                    'Tabbed View Type 2',
                    Box(
                        Text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis bibendum mi, ultricies '
                             'hendrerit est. Pellentesque eget molestie magna, vitae pulvinar arcu.'),
                    )
                ),
            ]
        )


TabbedViews.set(CUSTOM_MENU_ID, [TabbedView0, TabbedView1, TabbedView2])
