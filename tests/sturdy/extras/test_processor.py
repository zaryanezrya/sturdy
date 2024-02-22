import unittest
from unittest.mock import MagicMock

from sturdy import resolve
from sturdy.extras import InitScopeBasedIoCCommand, InitPluginSystemCommand

from sturdy.extras.processor import (
    Processor,
    create_default_context,
    Processable,
    PutCommandInContextCommand,
    HardStopCommand,
    SoftStopCommand,
)


class TestProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        InitScopeBasedIoCCommand()()
        InitPluginSystemCommand()()
        resolve("Plugin.Load", "sturdy.extras.scope_context_manager")()

    def test_terminate(self):
        with resolve("Scopes.RunInNewScope"):
            context = create_default_context()

            exception = Exception()
            command = MagicMock(side_effect=exception)
            PutCommandInContextCommand(context, command)()

            Processor(Processable(context))()

            self.assertEqual(exception, context["terminate_exception"])

    def test_hard_stop(self):
        with resolve("Scopes.RunInNewScope"):
            context = create_default_context()

            command = MagicMock()

            PutCommandInContextCommand(context, command)()
            PutCommandInContextCommand(context, command)()
            PutCommandInContextCommand(context, HardStopCommand(context))()
            PutCommandInContextCommand(context, command)()

            Processor(Processable(context))()

            self.assertEqual(2, command.call_count)

    def test_soft_stop(self):
        with resolve("Scopes.RunInNewScope"):
            context = create_default_context()

            command = MagicMock()

            PutCommandInContextCommand(context, command)()
            PutCommandInContextCommand(context, command)()
            PutCommandInContextCommand(context, SoftStopCommand(context))()
            PutCommandInContextCommand(context, command)()

            Processor(Processable(context))()

            self.assertEqual(3, command.call_count)
