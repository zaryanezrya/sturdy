import unittest

from sturdy import resolve
from sturdy.extras.scope_based_ioc import InitScopeBasedIoCCommand
from sturdy.plugin import load_plugin_command_factory


class TestEventLoop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        InitScopeBasedIoCCommand()()
        resolve("IoC.Register", "Plugin.Load", load_plugin_command_factory)()
        resolve("Plugin.Load", "sturdy.extras.scope_context_manager")()
        resolve("Plugin.Load", "sturdy.extras.empty_command")()
        resolve("Plugin.Load", "sturdy.extras.event_loop")()

    def test_hard_stop(self):
        with resolve("Scopes.RunInNewScope"):
            event_loop_id = "test_hard_stop"
            resolve("EventLoop.New", event_loop_id)()
            resolve("EventLoop.Send", event_loop_id, resolve("EmptyCommand"))
            resolve(
                "EventLoop.Send",
                event_loop_id,
                resolve("EventLoop.Commands.HardStop", event_loop_id),
            )
            resolve("EventLoop.Send", event_loop_id, resolve("EmptyCommand"))

            event_loop = resolve("EventLoop.Get", event_loop_id)
            event_loop()
            self.assertTrue(event_loop.stop)

            queue = resolve("EventLoop.Queue.Get", event_loop_id)
            self.assertFalse(queue.empty())
