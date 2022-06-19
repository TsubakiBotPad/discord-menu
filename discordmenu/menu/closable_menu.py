from typing import Dict, Any, Optional, Type

from discord import Message

from discordmenu.embed.menu import EmbedMenu
from discordmenu.embed.view_state import ViewState
from discordmenu.embed.wrapper import EmbedWrapper
from discordmenu.menu.base import PMenuableCM


class ClosableMenuViewState(ViewState):
    def __init__(self, original_author_id: int, menu_type: str, raw_query: str, view_type: str, sub_props: Any):
        super().__init__(original_author_id, menu_type, raw_query)
        self.view_type = view_type
        self.sub_props = sub_props


class ClosableMenusBase(PMenuableCM[ClosableMenuViewState]):
    MENU_TYPE = 'ClosableMenu'
    message = None
    view_types: Dict[str, Type] = {}

    @classmethod
    def menu(cls):
        # Menus added to view_types are independent and only support the default close button.
        # No additional transitions are defined.
        embed = EmbedMenu({}, cls.embed)
        return embed

    @classmethod
    async def embed_from_message(cls, message: Optional[Message], ims, **data) -> EmbedWrapper:
        # Because no actions can be taken on the menu, a menu would not need to be constructed from an existing message.
        # However, one could conceivably save the view state in a view_types dict, extract the menu type, and
        # reconstruct a menu from an existing message if such a use case arose.
        pass

    @classmethod
    def embed(cls, state: ClosableMenuViewState):
        view_cls = cls.view_types[state.view_type]
        return EmbedWrapper(
            view_cls(state, state.sub_props),
            []
        )
