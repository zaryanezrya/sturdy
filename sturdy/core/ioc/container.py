from abc import ABC, abstractmethod

from sturdy.core.strategy import IStrategy


class IDependenciesContainer(ABC):
    @abstractmethod
    def __getitem__(self, key: str) -> IStrategy:
        ...

    @abstractmethod
    def __setitem__(self, key: str, strategy: IStrategy):
        ...
