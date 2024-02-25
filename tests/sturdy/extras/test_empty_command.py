import unittest

from sturdy import resolve
from sturdy.extras import InitScopeBasedIoCCommand, InitPluginSystemCommand
from sturdy.extras.empty_command import EmptyCommand


class TestEmptyCommandPlugin(unittest.TestCase):
    def setUp(self) -> None:
        InitScopeBasedIoCCommand()()
        InitPluginSystemCommand()()

    def test_normal(self):
        resolve("Plugin.Load", "sturdy.extras.empty_command")()
        cmd1 = resolve("EmptyCommand")
        cmd2 = resolve("EmptyCommand")
        cmd3 = EmptyCommand()

        self.assertEqual(cmd1, cmd2)
        self.assertNotEqual(cmd1, cmd3)
