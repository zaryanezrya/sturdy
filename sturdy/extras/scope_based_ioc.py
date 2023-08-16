from abc import ABC, abstractmethod
from typing import Any, Callable, Dict
import threading

from sturdy.ioc import resolve, ICommand, ResolveDependencyException


class IScope(ABC):
    @abstractmethod
    def resolve(key: str, *args, **kwargs) -> Any:
        ...


def default_strategy_if_missing(key, *args, **kwargs):
    raise ResolveDependencyException(
        f"Unknown IoC dependency with key: {key}. Make sure that {key} has been registered before try to resolve the dependency"
    )


class Scope(IScope):
    def __init__(
        self,
        store: Dict[str, Callable],
        strategy_if_missing,
    ) -> None:
        self.store = store
        self.__strategy_if_missing = strategy_if_missing

    def resolve(self, key: str, *args, **kwargs) -> Any:
        if key in self.store:
            return self.store[key](*args, **kwargs)
        else:
            return self.__strategy_if_missing(key, *args, **kwargs)


class ScopeBasedResolveDependencyStrategy:
    root = None
    default_scope = lambda: ScopeBasedResolveDependencyStrategy.root
    current_scope = threading.local()

    def get_current_scope() -> IScope:
        tl_cs = ScopeBasedResolveDependencyStrategy.current_scope.value
        if not tl_cs:
            return ScopeBasedResolveDependencyStrategy.default_scope
        else:
            return tl_cs

    def set_current_scope(new_scope: IScope) -> None:
        ScopeBasedResolveDependencyStrategy.current_scope.value = new_scope

    def resolve(key: str, *args, **kwargs):
        return ScopeBasedResolveDependencyStrategy.get_current_scope().resolve(
            key, *args, **kwargs
        )


class RegisterIoCDependencyCommand(ICommand):
    def __init__(self, key, strategy) -> None:
        self.key = key
        self.strategy = strategy

    def __call__(self) -> None:
        ScopeBasedResolveDependencyStrategy.get_current_scope().store[
            self.key
        ] = self.strategy


class SetScopeInCurrentThreadCommand(ICommand):
    def __init__(self, scope: IScope) -> None:
        self.scope = scope

    def __call__(self) -> None:
        ScopeBasedResolveDependencyStrategy.set_current_scope(self.scope)


def scopes_new_strategy(*args, **kwargs):
    store = resolve("Scopes.Storage")
    if 0 == len(args):
        return Scope(store, default_strategy_if_missing)

    if issubclass(type(args[0]), IScope):
        parent: IScope = args[0]
        return Scope(
            store, lambda key, *args, **kwargs: parent.resolve(key, *args, **kwargs)
        )

    if issubclass(type(args[0]), Callable):
        return Scope(store, args[0])

    raise Exception("Failed to create scope")


class InitScopeBasedIoCCommand(ICommand):
    def __call__(self) -> None:
        if ScopeBasedResolveDependencyStrategy.root:
            return

        store = {}
        scope = Scope(store, default_strategy_if_missing)

        store["Scopes.Root"] = lambda: ScopeBasedResolveDependencyStrategy.root
        store["Scopes.Storage"] = lambda: {}
        store["Scopes.New"] = scopes_new_strategy
        store[
            "Scopes.Current"
        ] = lambda: ScopeBasedResolveDependencyStrategy.get_current_scope()
        store["Scopes.Current.Set"] = lambda scope: SetScopeInCurrentThreadCommand(
            scope
        )
        store["IoC.Register"] = lambda key, strategy: RegisterIoCDependencyCommand(
            key, strategy
        )

        ScopeBasedResolveDependencyStrategy.root = scope
        resolve(
            "IoC.SetupStrategy",
            lambda key, *args, **kwargs: ScopeBasedResolveDependencyStrategy.resolve(
                key, *args, **kwargs
            ),
        )()
        SetScopeInCurrentThreadCommand(scope)()
