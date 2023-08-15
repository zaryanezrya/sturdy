from abc import abstractmethod

from typing import Any


class IUObject:
    @abstractmethod
    def get_property(self, name: str) -> Any:
        ...

    @abstractmethod
    def set_property(self, name: str, value: Any) -> None:
        ...
