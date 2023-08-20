import unittest

from sturdy import resolve
from sturdy.extras.scope_based_ioc import InitScopeBasedIoCCommand
from sturdy.plugin import load_plugin_command_factory

from sturdy.extras.empty_command import EmptyCommand


class TestEmptyCommandPlugin(unittest.TestCase):
    def setUp(self) -> None:
        InitScopeBasedIoCCommand()()
        resolve("IoC.Register", "Plugin.Load", load_plugin_command_factory)()

    def test_normal(self):
        resolve("Plugin.Load", "sturdy.extras.empty_command")()
        cmd1 = resolve("EmptyCommand")
        cmd2 = resolve("EmptyCommand")
        cmd3 = EmptyCommand()

        self.assertEqual(cmd1, cmd2)
        self.assertNotEqual(cmd1, cmd3)
