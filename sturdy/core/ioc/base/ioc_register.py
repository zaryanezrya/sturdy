from typing import Any

from sturdy.core.strategy import IStrategy
from sturdy.core.command import ICommand
from sturdy.core.ioc.interfaces import IDependenciesContainer
from sturdy.core.ioc.exceptions import ResolveDependencyException


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
