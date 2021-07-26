from abc import abstractmethod, ABC
from collections.abc import Mapping
from typing import List, Union, Iterable, Any


class Box:
    def __init__(self, *args: Union[str, "Box"], delimiter: str = "\n"):
        self._inner_object = [a for a in args if a]
        self.delimiter = delimiter

    def _get_markdown(self, arg: Union[str, "Box"]) -> str:
        if hasattr(arg, 'to_markdown'):
            return arg.to_markdown()
        return arg

    def to_markdown(self) -> str:
        if len(self._inner_object) == 1:
            return self._get_markdown(self._inner_object[0])
        return self.delimiter.join([self._get_markdown(a) for a in self._inner_object])


class CustomMapping(Mapping[str, Any], ABC):
    def __len__(self) -> int:
        return len(self.fields)

    def __iter__(self) -> Iterable[str]:
        for f in self.fields:
            yield f

    def __getitem__(self, key: str) -> Any:
        ret = getattr(self, key)
        if hasattr(ret, 'to_markdown'):
            return ret.to_markdown()
        return ret

    @property
    @abstractmethod
    def fields(self) -> List[str]:
        pass
