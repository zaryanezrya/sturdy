import unittest

from sturdy import resolve
from sturdy.deprecated.empty_command import EmptyCommand


@unittest.skip("refactoring")
class TestEmptyCommandPlugin(unittest.TestCase):
    def setUp(self) -> None:
        resolve("Plugin.Load", "sturdy.extras.empty_command")()

    def test_normal(self):
        cmd1 = resolve("EmptyCommand")
        cmd2 = resolve("EmptyCommand")
        cmd3 = EmptyCommand()

        self.assertEqual(cmd1, cmd2)
        self.assertNotEqual(cmd1, cmd3)
