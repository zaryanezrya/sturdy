from typing import Any

from .command import ICommand


def default_resolve_strategy(key: str, *args, **kwargs) -> Any:
    if "IoC.SetupStrategy" == key:
        return SetupStrategyCommand(args[0])
    if "IoC.Default" == key:
        return default_resolve_strategy
    raise ResolveDependencyException(
        f"Unknown IoC dependency with key: {key}. Make sure that {key} has been registered before try to resolve the dependency"
    )


class IoC:
    resolve_strategy = default_resolve_strategy

    def resolve(key: str, *args, **kwargs) -> Any:
        try:
            return IoC.resolve_strategy(key, *args, **kwargs)
        except ResolveDependencyException as e:
            raise e
        except Exception as e:
            raise ResolveDependencyException(
                f"An unexpected exception occurred with key: {key} and args: {args}, and kwargs: {kwargs}: {e}"
            )


class ResolveDependencyException(Exception):
    ...


class SetupStrategyCommand(ICommand):
    def __init__(self, new_strategy) -> None:
        self.new_strategy = new_strategy

    def __call__(self) -> None:
        IoC.resolve_strategy = self.new_strategy


def resolve(key: str, *args, **kwargs) -> Any:
    return IoC.resolve(key, *args, **kwargs)
