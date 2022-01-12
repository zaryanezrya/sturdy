from typing import Any, Callable

from sturdy.core.command import ICommand
from sturdy.core.strategy import IStrategy

from .interfaces import IDependenciesContainer
from .exceptions import ResolveDependencyException

from sturdy.core.ioc.base.plugin_load import IOCBaseLoadPluginCommandResolver


class IOCBaseContainer(IDependenciesContainer):
    def __init__(self, not_found_strategy: Callable):
        self.__not_found_strategy = not_found_strategy
        self.__store = {}

        self.__store["IoC.Resolve"] = IOCBaseResolveResolver(self)
        self.__store["IoC.Register"] = IOCBaseRegisterCommandResolver(self)
        self.__store["IoC.BaseContainer"] = lambda: self
        self.__store["Plugin.Load"] = IOCBaseLoadPluginCommandResolver()

    def __getitem__(self, key: str) -> IStrategy:
        try:
            return self.__store[key]
        except KeyError:
            return self.__not_found_strategy(key)
        except ResolveDependencyException as e:
            raise e

    def __setitem__(self, key: str, strategy: IStrategy):
        self.__store[key] = strategy


class IOCBaseResolveResolver(IStrategy):
    def __init__(self, container: IDependenciesContainer):
        self.__container = container

    def __call__(self, *args: Any) -> IStrategy:
        key = args[0]
        return self.__container[key](*args[1:])


class IOCBaseRegisterCommandResolver(IStrategy):
    def __init__(self, container: IDependenciesContainer):
        self.__container = container

    def __call__(self, *args: Any) -> IStrategy:
        try:
            key = args[0]
            strategy = args[1]
            # TODO: Throw ResolveDependencyException "agrs[0] must have type String, args[1] must have IStrategy"
            return IOCBaseRegisterCommand(self.__container, key, strategy)
        except IndexError:
            raise ResolveDependencyException(
                "IoC.Register requires two args: key(str) and strategy(IStrategy)"
            )


class IOCBaseRegisterCommand(ICommand):
    def __init__(
        self,
        container: IDependenciesContainer,
        key: str,
        strategy: IStrategy,
    ):
        self.container = container
        self.key = key
        self.strategy = strategy

    def __call__(self) -> None:
        self.container[self.key] = self.strategy
