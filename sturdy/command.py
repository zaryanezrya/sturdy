from abc import ABC, abstractmethod


class ICommand(ABC):
    @abstractmethod
    def __call__(self) -> None:
        ...


class CommandException(Exception):
    ...
