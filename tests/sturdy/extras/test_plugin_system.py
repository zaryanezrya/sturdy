import unittest

from sturdy import resolve, CommandException
from sturdy.extras import InitScopeBasedIoCCommand, InitPluginSystemCommand


class TestPluginLoad(unittest.TestCase):
    def setUp(self) -> None:
        InitScopeBasedIoCCommand()()
        InitPluginSystemCommand()()

    def test_success(self):
        resolve("Plugin.Load", "tests.test_doubles.math_helper")()
        self.assertEqual(3, resolve("MathHelper.add", 1, 2))

    def test_plugin_not_found(self):
        cmd = resolve("Plugin.Load", "DEFINITELYDOESNTEXIST")
        self.assertRaises(CommandException, cmd)

    def test_plugin_load_command_not_found(self):
        cmd = resolve("Plugin.Load", "tests.test_doubles.not_plugin")
        self.assertRaises(CommandException, cmd)
