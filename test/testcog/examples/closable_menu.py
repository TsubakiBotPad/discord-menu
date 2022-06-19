from discordmenu.embed.base import Box
from discordmenu.embed.components import EmbedMain, EmbedField
from discordmenu.embed.text import Text
from discordmenu.embed.view import EmbedView
from discordmenu.menu.closable_menu import ClosableMenusBase, ClosableMenuViewState
from discordmenu.menu.footer import embed_footer_with_state


class ClosableView1Props:
    VIEW_TYPE = 'ClosableViewType1'

    def __init__(self, inner_message: str):
        self.inner_message = inner_message


class ClosableView1(EmbedView):
    def __init__(self, state: ClosableMenuViewState, props: ClosableView1Props):
        super().__init__(
            EmbedMain(),
            embed_footer=embed_footer_with_state(state),
            embed_fields=[
                EmbedField(
                    'Closable View Type 1',
                    Box(
                        Text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis bibendum mi, ultricies '
                             'hendrerit est. Pellentesque eget molestie magna, vitae pulvinar arcu.'),
                        Text(props.inner_message)
                    )
                ),
            ]
        )


class ClosableView2Props:
    VIEW_TYPE = 'ClosableViewType2'

    def __init__(self, inner_message: str):
        self.inner_message = inner_message


class ClosableView2(EmbedView):
    def __init__(self, state: ClosableMenuViewState, props: ClosableView2Props):
        super().__init__(
            EmbedMain(),
            embed_footer=embed_footer_with_state(state),
            embed_fields=[
                EmbedField(
                    'Closable View Type 2',
                    Box(
                        Text('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In quis bibendum mi, ultricies '
                             'hendrerit est. Pellentesque eget molestie magna, vitae pulvinar arcu.'),
                        Text(props.inner_message)
                    )
                ),
            ]
        )


class ClosableMenus(ClosableMenusBase):
    view_types = {
        ClosableView1Props.VIEW_TYPE: ClosableView1,
        ClosableView2Props.VIEW_TYPE: ClosableView2,
    }
