import unittest

from sturdy import resolve
from sturdy.extras import InitScopeBasedIoCCommand, InitPluginSystemCommand


class TestScopeContextManager(unittest.TestCase):
    def setUp(self) -> None:
        InitScopeBasedIoCCommand()()
        InitPluginSystemCommand()()
        resolve("Plugin.Load", "sturdy.extras.scope_context_manager")()

    def test_run_in_scope(self):
        scope = resolve("Scopes.New", resolve("Scopes.Current"))
        resolve("IoC.Register", "test_dep", lambda: False)()

        with resolve("Scopes.RunInScope", scope):
            resolve("IoC.Register", "test_dep", lambda: True)()
            self.assertTrue(resolve("test_dep"))

        self.assertFalse(resolve("test_dep"))

    def test_run_in_new_scope(self):
        resolve("IoC.Register", "test_dep", lambda: False)()

        with resolve("Scopes.RunInNewScope"):
            resolve("IoC.Register", "test_dep", lambda: True)()
            self.assertTrue(resolve("test_dep"))

        self.assertFalse(resolve("test_dep"))
