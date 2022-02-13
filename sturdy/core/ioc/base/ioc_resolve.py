from typing import Any

from sturdy.core.strategy import IStrategy
from sturdy.core.ioc.container import IDependenciesContainer


class IOCBaseResolveResolver(IStrategy):
    def __init__(self, container: IDependenciesContainer):
        self.__container = container

    def __call__(self, *args: Any) -> IStrategy:
        key = args[0]
        return self.__container[key](*args[1:])
