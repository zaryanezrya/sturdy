import unittest

from sturdy import resolve


# TODO: ...
class TestPluginLoader(unittest.TestCase):
    def test_normal(self):
        resolve("Plugin.Load", "tests.mocks.plugins.math_helper")()
        self.assertEqual(3, resolve("MathHelper.add", 1, 2))
