import unittest

from sturdy.ioc import resolve
from sturdy.plugins.manager import PluginManager

from tests.mocks.plugins.math_helper import Plugin as MathHelper


class TestPluginManager(unittest.TestCase):
    def test_plugin_manager_register_success(self):
        PluginManager().get_load_command()()

        resolve("Plugins.Register", MathHelper())()

        self.assertEqual(3, resolve("MathHelper.add", 1, 2))
