from typing import List, Union

from discord import Emoji

from discordmenu.embed.base import Box


class Text(Box):
    def __init__(self, value: Union[str, Box]):
        super().__init__(self)
        self.value = value

    def to_markdown(self) -> str:
        if isinstance(self.value, Box):
            return self.value.to_markdown()
        return self.value

    def __bool__(self) -> bool:
        return bool(self.value)


class LabeledText(Box):
    def __init__(self, name: str, value: Union[Box, str]):
        super().__init__(self)
        self._name = BoldText(name)
        if isinstance(value, str):
            self._value = Text(value)
        else:
            self._value = value

    def to_markdown(self) -> str:
        if not self._name:
            return self._value.to_markdown()
        if not self._value:
            return self._name.to_markdown()
        return "{} {}".format(self._name.to_markdown(), self._value.to_markdown())

    @property
    def name(self) -> "BoldText":
        return self._name

    @name.setter
    def name(self, name: Union[str, Box]) -> None:
        self._name = BoldText(name)

    @property
    def value(self) -> Box:
        return self._value

    @value.setter
    def value(self, value: Union[str, Box]) -> None:
        self._value = Text(value)

    def __bool__(self) -> bool:
        return bool(self.name or self.value)


class LinkedText(Box):
    def __init__(self, name: str, link: str):
        super().__init__(self)
        self._name = Text(name)
        self.link = link

    def to_markdown(self) -> str:
        return "[{}]({})".format(self._name.to_markdown(), self.link)

    @property
    def name(self) -> Text:
        return self._name

    @name.setter
    def name(self, value: Union[str, Box]) -> None:
        self._name = Text(value)

    def __bool__(self) -> bool:
        return bool(self.name)


class BoldText(Box):
    def __init__(self, value: Union[str, Text, LinkedText]):
        super().__init__(self)
        self._value = Text(value)

    def to_markdown(self) -> str:
        return "**{}**".format(self._value.to_markdown())

    @property
    def value(self) -> Text:
        return self._value

    @value.setter
    def value(self, value: Union[str, Box]) -> None:
        self._value = Text(value)

    def __bool__(self) -> bool:
        return bool(self.value)


class InlineText(Box):
    def __init__(self, value: Union[str, Box]):
        super().__init__(self)
        self._value = Text(value)

    def to_markdown(self) -> str:
        return "`{}`".format(self._value.to_markdown())

    @property
    def value(self) -> Text:
        return self._value

    @value.setter
    def value(self, value: Union[str, Box]) -> None:
        self._value = Text(value)

    def __bool__(self) -> bool:
        return bool(self.value)


class BlockText(Box):
    def __init__(self, value: Union[str, Box]):
        super().__init__(self)
        self._value = Text(value)

    def to_markdown(self) -> str:
        return "```\n{}\n```".format(self._value.to_markdown())

    @property
    def value(self) -> Text:
        return self._value

    @value.setter
    def value(self, value: Union[str, Box]) -> None:
        self._value = Text(value)

    def __bool__(self) -> bool:
        return bool(self.value)


class HighlightableLinks(Box):
    def __init__(self, links: List[LinkedText], highlighted: int, delimiter: str = ", "):
        super().__init__(self)
        self.delimiter = delimiter
        self.links = links
        self._highlighted = links[highlighted]

    def _get_link_markdown(self, link: LinkedText) -> str:
        return link.to_markdown() if link != self.highlighted else BoldText(link.name.value).to_markdown()

    def to_markdown(self) -> str:
        return self.delimiter.join([self._get_link_markdown(link) for link in self.links])

    @property
    def highlighted(self) -> LinkedText:
        return self._highlighted

    @highlighted.setter
    def highlighted(self, highlighted: int) -> None:
        if len(self.links) <= highlighted < 0:
            raise Exception("Selected is out of bounds")
        self.highlighted = self.links[highlighted]

    def __bool__(self) -> bool:
        return any(self.links)


class CustomEmoji(Box):
    def __init__(self, emoji: Emoji):
        super().__init__(self)
        self.emoji = emoji

    def to_markdown(self) -> str:
        return "<{}:{}:{}>".format("a" if self.emoji.animated else "", self.emoji.name, self.emoji.id)

    def __bool__(self) -> bool:
        return True
