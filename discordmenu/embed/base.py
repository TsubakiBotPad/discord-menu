from abc import abstractmethod, ABC
from typing import List, Mapping, Union, Iterable, Any


class Box:
    def __init__(self, *contents: Union[str, "Box"], delimiter: str = "\n"):
        self.contents = contents
        self.delimiter = delimiter

    def _get_markdown(self, arg: Union[str, "Box"]) -> str:
        if isinstance(arg, Box):
            return arg.to_markdown()
        return arg

    def to_markdown(self) -> str:
        return self.delimiter.join(self._get_markdown(a) for a in self.contents if a)

    def __bool__(self) -> bool:
        return any(self.contents)


class CustomMapping(Mapping[str, Any], ABC):
    def __len__(self) -> int:
        return len(self.fields)

    def __iter__(self) -> Iterable[str]:
        yield from self.fields

    def __getitem__(self, key: str) -> Any:
        ret = getattr(self, key)
        if hasattr(ret, 'to_markdown'):
            return ret.to_markdown()
        return ret

    @property
    @abstractmethod
    def fields(self) -> List[str]:
        pass
