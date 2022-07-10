from discordmenu.embed.base import Box
from discordmenu.embed.components import EmbedMain, EmbedField
from discordmenu.embed.text import Text
from discordmenu.embed.view import EmbedView
from discordmenu.menu.footer import embed_footer_with_state
from discordmenu.menu.scrollable_menu import ScrollableViewState


class ScrollableView0(EmbedView):
    def __init__(self, state: ScrollableViewState):
        super().__init__(
            EmbedMain(),
            embed_footer=embed_footer_with_state(state),
            embed_fields=[
                EmbedField(
                    'Scrollable View Type 0 of {}'.format(state.num_pages),
                    Box(
                        Text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis bibendum mi, ultricies '
                             'hendrerit est. Pellentesque eget molestie magna, vitae pulvinar arcu.'),
                        Text('Navigated from pane {}'.format(state.prev_pane_num))
                    )
                ),
            ]
        )


class ScrollableView1(EmbedView):
    def __init__(self, state: ScrollableViewState):
        super().__init__(
            EmbedMain(),
            embed_footer=embed_footer_with_state(state),
            embed_fields=[
                EmbedField(
                    'Scrollable View Type 1 of {}'.format(state.num_pages),
                    Box(
                        Text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis bibendum mi, ultricies '
                             'hendrerit est. Pellentesque eget molestie magna, vitae pulvinar arcu.'),
                        Text('Navigated from pane {}'.format(state.prev_pane_num))
                    )
                ),
            ]
        )


class ScrollableView2(EmbedView):
    def __init__(self, state: ScrollableViewState):
        super().__init__(
            EmbedMain(),
            embed_footer=embed_footer_with_state(state),
            embed_fields=[
                EmbedField(
                    'Scrollable View Type 2 of {}'.format(state.num_pages),
                    Box(
                        Text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis bibendum mi, ultricies '
                             'hendrerit est. Pellentesque eget molestie magna, vitae pulvinar arcu.'),
                        Text('Navigated from pane {}'.format(state.prev_pane_num))
                    )
                ),
            ]
        )

