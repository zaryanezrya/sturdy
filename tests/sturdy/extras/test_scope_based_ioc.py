import unittest

from sturdy.ioc import resolve, ResolveDependencyException
from sturdy.extras.scope_based_ioc import (
    Scope,
    InitScopeBasedIoCCommand,
    ScopeBasedResolveDependencyStrategy,
)


class TestScope(unittest.TestCase):
    def test_default_strategy_if_missing(self):
        store = {
            "a": lambda: 1,
            "b": lambda: 2,
        }
        scope = Scope(store)
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
    def test_scopes_root(self):
        InitScopeBasedIoCCommand()()
        self.assertEqual(
            resolve("Scopes.Root"), ScopeBasedResolveDependencyStrategy.root
        )

    def test_scopes_storage(self):
        InitScopeBasedIoCCommand()()
        self.assertNotEqual(
            id(resolve("Scopes.Storage")), id(resolve("Scopes.Storage"))
        )

    def test_scopes_new_default(self):
        InitScopeBasedIoCCommand()()
        scope = resolve("Scopes.New")
        self.assertRaises(ResolveDependencyException, scope.resolve, "MISSING")

    def test_scopes_new_custom(self):
        InitScopeBasedIoCCommand()()
        scope = resolve("Scopes.New", lambda key: f"{key} not found")
        self.assertEqual("c not found", scope.resolve("c"))

    def test_ioc_register(self):
        InitScopeBasedIoCCommand()()
        resolve("IoC.Register", "always_one", lambda: 1)()
        self.assertEqual(resolve("always_one"), 1)
