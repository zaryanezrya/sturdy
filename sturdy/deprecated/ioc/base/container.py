from sturdy.deprecated.strategy import IStrategy

from sturdy.deprecated.ioc.container import IDependenciesContainer
from sturdy.deprecated.ioc.exceptions import ResolveDependencyException

from sturdy.deprecated.ioc.base.ioc_resolve import IOCBaseResolveResolver
from sturdy.deprecated.ioc.base.plugin_load import IOCBaseLoadPluginCommandResolver
from sturdy.deprecated.ioc.base.ioc_register import IOCBaseRegisterCommandResolver


class IOCBaseContainer(IDependenciesContainer):
    def __init__(self):
        self.__not_found_strategy = lambda key: raise_(
            ResolveDependencyException(f"Dependency {key} is missing")
        )
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


def raise_(ex):
    raise ex
