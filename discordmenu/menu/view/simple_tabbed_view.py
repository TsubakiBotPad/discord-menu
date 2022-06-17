from typing import Any, Dict

from discordmenu.embed.components import EmbedMain
from discordmenu.embed.view import EmbedView
from discordmenu.embed.view_state import ViewState
from discordmenu.menu.footer import embed_footer_with_state


class SimpleTabbedViewState(ViewState):
    def __init__(self, message, extra_state=None):
        super().__init__(0, "SimpleTabbedMenu", "", extra_state=extra_state)
        self.message = message

    def serialize(self) -> Dict[str, Any]:
        ret = super().serialize()
        ret.update({
            'message': self.message
        })
        return ret

    @classmethod
    async def deserialize(cls, ims: dict) -> "SimpleTabbedViewState":
        return cls(ims.get('message'), extra_state=ims)


class SimpleTabbedView(EmbedView):
    VIEW_TYPE = 'SimpleTabbed'

    def __init__(self, state: SimpleTabbedViewState):
        super().__init__(
            EmbedMain(description=state.message),
            embed_footer=embed_footer_with_state(state)
        )
