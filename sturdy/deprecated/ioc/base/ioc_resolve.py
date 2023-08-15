from typing import Any

from sturdy.deprecated.strategy import IStrategy
from sturdy.deprecated.ioc.container import IDependenciesContainer


class IOCBaseResolveResolver(IStrategy):
    def __init__(self, container: IDependenciesContainer):
        self.__container = container

    def __call__(self, *args: Any, **kwargs: Any) -> IStrategy:
        key = args[0]
        return self.__container[key](*args[1:], **kwargs)
