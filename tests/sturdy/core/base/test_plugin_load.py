import unittest

from sturdy import resolve, CommandException


@unittest.skip("refactoring")
class TestBasePluginLoad(unittest.TestCase):
    def test_plugin_load(self):
        resolve("Plugin.Load", "tests.mocks.plugins.math_helper")()
        self.assertEqual(3, resolve("MathHelper.add", 1, 2))

    def test_plugin_load_not_found(self):
        cmd = resolve("Plugin.Load", "DEFINITELYDOESNTEXIST")
        self.assertRaises(CommandException, cmd)
