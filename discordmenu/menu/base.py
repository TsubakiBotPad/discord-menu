from typing import Optional, Protocol, TypeVar

from discord import Message

from discordmenu.embed.menu import EmbedMenu
from discordmenu.embed.wrapper import EmbedWrapper

T = TypeVar('T')


class PMenuable(Protocol[T]):
    @staticmethod
    def menu() -> EmbedMenu:
        ...

    @staticmethod
    async def embed_from_message(message: Optional[Message], ims, **data) -> EmbedWrapper:
        ...

    @staticmethod
    def embed(state: T) -> Optional[EmbedWrapper]:
        ...

    def __repr__(self):
        return str(type(self))


class PMenuableCM(Protocol[T]):
    @classmethod
    def menu(cls) -> EmbedMenu:
        ...

    @classmethod
    async def embed_from_message(cls, message: Optional[Message], ims, **data) -> EmbedWrapper:
        ...

    @classmethod
    def embed(cls, state: T) -> Optional[EmbedWrapper]:
        ...

    def __repr__(self):
        return str(type(self))
