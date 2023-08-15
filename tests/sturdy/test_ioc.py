import unittest

from sturdy.ioc import resolve, ResolveDependencyException
from sturdy.ioc import default_resolve_strategy, SetupStrategyCommand


class TestIoCDefault(unittest.TestCase):
    def test_ioc_default_resolve_missing_key_fail(self):
        self.assertRaises(ResolveDependencyException, resolve, "MISSING_KEY")

    def test_ioc_default_resolve_IoC_default_success(self):
        self.assertEqual(resolve("IoC.Default"), default_resolve_strategy)

    def test_ioc_default_resolve_IoC_SetupStrategy_success(self):
        setup_strategy_command = resolve("IoC.SetupStrategy", lambda key: "CHANGED")
        self.assertTrue(isinstance(setup_strategy_command, SetupStrategyCommand))
