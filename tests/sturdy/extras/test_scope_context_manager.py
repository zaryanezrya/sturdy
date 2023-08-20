import unittest

from sturdy import resolve
from sturdy.extras.scope_based_ioc import InitScopeBasedIoCCommand
from sturdy.plugin import load_plugin_command_factory


class TestScopeContextManager(unittest.TestCase):
    def setUp(self) -> None:
        InitScopeBasedIoCCommand()()
        resolve("IoC.Register", "Plugin.Load", load_plugin_command_factory)()
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
