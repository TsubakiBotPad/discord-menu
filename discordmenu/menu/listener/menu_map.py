import json
from collections import UserDict
from dataclasses import dataclass
from typing import Protocol, Dict, Optional

from discordmenu.embed.menu import EmbedMenu
from discordmenu.embed.transitions import EmbedTransitionsBase


class Menuable(Protocol):
    @staticmethod
    def menu() -> EmbedMenu:
        ...


@dataclass
class MenuMapEntry:
    menuable: Menuable
    transition: EmbedTransitionsBase
    cog_name: Optional[str]


class MenuMap(UserDict[str, MenuMapEntry]):
    def __init__(self, val=None):
        super().__init__(val)

    def __repr__(self):
        return json.dumps(self.data)