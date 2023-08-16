import unittest

from sturdy.ioc import resolve, ResolveDependencyException
from sturdy.extras.scope_based_ioc import (
    Scope,
    InitScopeBasedIoCCommand,
    default_strategy_if_missing,
)


class TestScope(unittest.TestCase):
    def test_default_strategy_if_missing(self):
        store = {
            "a": lambda: 1,
            "b": lambda: 2,
        }
        scope = Scope(store, default_strategy_if_missing)
        self.assertEqual(1, scope.resolve("a"))
        self.assertEqual(2, scope.resolve("b"))
        self.assertRaises(ResolveDependencyException, resolve, "c")

    def test_custom_strategy_if_missing(self):
        store = {
            "a": lambda: 1,
            "b": lambda: 2,
        }
        scope = Scope(store, lambda key: f"{key} not found")
        self.assertEqual(1, scope.resolve("a"))
        self.assertEqual(2, scope.resolve("b"))
        self.assertEqual("c not found", scope.resolve("c"))


class TestInitScopeBasedIoCCommand(unittest.TestCase):
    def test_scopes_storage(self):
        InitScopeBasedIoCCommand()()
        self.assertNotEqual(
            id(resolve("Scopes.Storage")), id(resolve("Scopes.Storage"))
        )

    def test_scopes_new_default(self):
        InitScopeBasedIoCCommand()()
        scope = resolve("Scopes.New")
        self.assertRaises(ResolveDependencyException, scope.resolve, "MISSING")

    def test_scopes_new_with_strategy(self):
        InitScopeBasedIoCCommand()()
        scope = resolve("Scopes.New", lambda key: f"{key} not found")
        self.assertEqual("c not found", scope.resolve("c"))

    def test_scopes_new_with_parent(self):
        InitScopeBasedIoCCommand()()
        current = resolve("Scopes.Current")
        scope = resolve("Scopes.New", current)
        self.assertEqual(current, scope.resolve("Scopes.Current"))

    def test_ioc_register(self):
        InitScopeBasedIoCCommand()()
        resolve("IoC.Register", "always_one", lambda: 1)()
        self.assertEqual(resolve("always_one"), 1)

    def test_ioc_scopes_current_set(self):
        InitScopeBasedIoCCommand()()

        base_scope = resolve("Scopes.Current")
        resolve("IoC.Register", "Scopes.Id", lambda: 0)()

        scope1 = resolve("Scopes.New", base_scope)
        resolve("Scopes.Current.Set", scope1)()
        resolve("IoC.Register", "Scopes.Id", lambda: 1)()

        scope2 = resolve("Scopes.New", base_scope)
        resolve("Scopes.Current.Set", scope2)()
        resolve("IoC.Register", "Scopes.Id", lambda: 2)()

        resolve("Scopes.Current.Set", base_scope)()
        self.assertEqual(resolve("Scopes.Id"), 0)

        resolve("Scopes.Current.Set", scope1)()
        self.assertEqual(resolve("Scopes.Id"), 1)

        resolve("Scopes.Current.Set", scope2)()
        self.assertEqual(resolve("Scopes.Id"), 2)
