import json
from collections import UserDict
from dataclasses import dataclass
from typing import Optional, Type

from discordmenu.embed.transitions import EmbedTransitions
from discordmenu.menu.base import PMenuable


@dataclass
class MenuMapEntry:
    menuable: PMenuable
    transitions: Type[EmbedTransitions]
    cog_name: Optional[str] = None

    def __repr__(self):
        return json.dumps({
            'menuable': str(self.menuable),
            'transitions': str(self.transitions),
            'cog_name': self.cog_name,
        })


class MenuMap(UserDict[str, MenuMapEntry]):
    def __init__(self, val=None):
        super().__init__(val)

    def __repr__(self):
        return json.dumps(self.data)
