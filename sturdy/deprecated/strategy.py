from abc import ABC, abstractmethod
from typing import Any


class IStrategy(ABC):
    @abstractmethod
    def __call__(self, *args: Any) -> Any:
        ...
