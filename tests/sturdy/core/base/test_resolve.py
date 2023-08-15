import unittest

from sturdy import resolve, ResolveDependencyException


@unittest.skip("refactoring")
class TestBaseResolveAndRegister(unittest.TestCase):
    def test_ioc_resolve_missing_key_fail(self):
        self.assertRaises(ResolveDependencyException, resolve, "MISSING_KEY")

    def test_ioc_register_and_ioc_resolve_lambda(self):
        resolve("IoC.Register", "App.diff1", lambda *args: args[0] - args[1])()
        self.assertEqual(10, resolve("App.diff1", 11, 1))
        self.assertRaises(ResolveDependencyException, resolve, "App.diff1", a=11, b=1)

        resolve("IoC.Register", "App.diff2", lambda a, b: a - b)()
        self.assertEqual(10, resolve("App.diff2", 11, 1))
        self.assertEqual(10, resolve("App.diff2", 11, b=1))
        self.assertEqual(10, resolve("App.diff2", a=11, b=1))
        self.assertEqual(-10, resolve("App.diff2", b=11, a=1))
        self.assertRaises(ResolveDependencyException, resolve, "App.diff2", 11, a=1)

    def test_ioc_register_no_args_fail(self):
        self.assertRaises(ResolveDependencyException, resolve, "IoC.Register")

    def test_ioc_register_none(self):
        resolve("IoC.Register", "App.dummy", None)()
        self.assertRaises(ResolveDependencyException, resolve, "App.dummy")

    def test_ioc_register_non_callable(self):
        non_callable = 1
        resolve("IoC.Register", "App.dummy", non_callable)()
        self.assertRaises(ResolveDependencyException, resolve, "App.dummy")
