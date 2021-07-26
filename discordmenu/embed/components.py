from typing import List, Union

from discord import Color

from discordmenu.embed.base import CustomMapping, Box
from discordmenu.embed.text import Text


class EmbedField(CustomMapping):
    @property
    def fields(self) -> List[str]:
        return ["name", "value", "inline"]

    def __init__(self, title: Union[Box, str], body: Union[Box, str], inline: bool = False,
                 chunk_delimiter: str = '\n', continuation_title: str = ''):
        self.continuation_title = continuation_title
        self.chunk_delimiter = chunk_delimiter
        self._name = Text(title)
        self._value = body
        self.inline = inline

    @property
    def name(self) -> Text:
        return self._name

    @name.setter
    def name(self, title: Union[Box, str]) -> None:
        self._name = Text(title)

    @property
    def value(self) -> Union[Box, str]:
        return self._value

    @value.setter
    def value(self, body: Union[Box, str]) -> None:
        self._value = Box(body)


class EmbedMain(CustomMapping):
    @property
    def fields(self) -> List[str]:
        return ["url", "title", "color", "description"]

    def __init__(self, title: str = "", url: str = "", color: Union[str, Color] = Color.default(),
                 description: Union[Box, str] = ""):
        self.title = title
        self.url = url
        if isinstance(color, Color):
            self.color = color
        else:
            self.color = int(color, 16 if not color.startswith("0x") else 0)
        self.description = description


class EmbedFooter(CustomMapping):
    @property
    def fields(self) -> List[str]:
        return ["icon_url", "text"]

    def __init__(self, value: Union[Box, str], icon_url: str = ""):
        self.icon_url = icon_url
        self.text = value


class EmbedAuthor(CustomMapping):
    @property
    def fields(self) -> List[str]:
        return ["name", "url", "icon_url"]

    def __init__(self, name: str, url: str = "", icon_url: str = ""):
        self.name = name
        self.icon_url = icon_url
        self.url = url


class EmbedThumbnail(CustomMapping):
    @property
    def fields(self) -> List[str]:
        return ["url"]

    def __init__(self, url: str):
        self.url = url


class EmbedBodyImage(CustomMapping):
    @property
    def fields(self) -> List[str]:
        return ["url"]

    def __init__(self, url: str):
        self.url = url
