from abc import ABC, abstractmethod
from typing import Callable

from sturdy.interfaces import IStrategy


class IResolveDependencyStrategy(IStrategy):
    ...


class IDependenciesContainer(ABC):
    @abstractmethod
    def __init__(self, not_found_strategy: Callable):
        ...

    @abstractmethod
    def __getitem__(self, key: str) -> IResolveDependencyStrategy:
        ...

    @abstractmethod
    def __setitem__(self, key: str, strategy: IResolveDependencyStrategy):
        ...
