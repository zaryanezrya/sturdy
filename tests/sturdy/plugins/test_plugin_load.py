import unittest

from sturdy import resolve


class TestPluginLoadCommand(unittest.TestCase):
    def test_plugin_load_success(self):
        from tests.mocks.plugins.math_helper import PluginLoadCommand

        PluginLoadCommand()()

        self.assertEqual(3, resolve("MathHelper.add", 1, 2))
