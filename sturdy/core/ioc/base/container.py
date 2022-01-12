from typing import Callable

from sturdy.core.strategy import IStrategy

from sturdy.core.ioc.container import IDependenciesContainer
from sturdy.core.ioc.exceptions import ResolveDependencyException

from sturdy.core.ioc.base.ioc_resolve import IOCBaseResolveResolver
from sturdy.core.ioc.base.plugin_load import IOCBaseLoadPluginCommandResolver
from sturdy.core.ioc.base.ioc_register import IOCBaseRegisterCommandResolver


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
