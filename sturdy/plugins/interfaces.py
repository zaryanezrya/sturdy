from abc import ABC, abstractmethod

from sturdy.ioc.interfaces import ICommand


class IPlugin(ABC):
    @abstractmethod
    def get_load_command(self) -> ICommand:
        ...

    @abstractmethod
    def get_unload_command(self) -> ICommand:
        ...
