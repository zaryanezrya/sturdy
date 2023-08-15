from typing import Any, List

from sturdy import resolve, ICommand, CommandException, IStrategy


class PluginLoadCommand(ICommand):
    def __call__(self) -> None:
        action_factory = ActionFactory()
        resolve(
            "IoC.Register",
            "SimpleTransaction.CreateAction",
            lambda *args: action_factory(args),
        )()

        transaction_factory = TransactionFactory()
        resolve(
            "IoC.Register",
            "SimpleTransaction.CreateTransaction",
            lambda raw_actions: transaction_factory(raw_actions),
        )()


class Action:
    def __init__(self, do: ICommand, undo: ICommand) -> None:
        self.__do_command = do
        self.__undo_command = undo

    def do(self) -> None:
        self.__do_command()

    def undo(self) -> None:
        self.__undo_command()


class Transaction(ICommand):
    def __init__(self, actions: List[Action]):
        self.__actions = actions

    def __call__(self) -> None:
        self.__run_actions()

    def __run_actions(self) -> None:
        num_of_executed = 0
        try:
            for action in self.__actions:
                action.do()
                num_of_executed += 1
        except CommandException:
            self.__run_compensations(num_of_executed)

    def __run_compensations(self, num_of_executed) -> None:
        for i in range(num_of_executed, 0, -1):
            self.__actions[i].undo()


class ActionFactory(IStrategy):
    def __init__(self):
        self.__empty_command = resolve("EmptyCommand")

    def __call__(self, *args) -> Action:
        if len(args) == 2:
            return Action(args[0], args[1])

        if issubclass(type(args[0]), ICommand):
            return Action(args[0], self.__empty_command)

        if isinstance(args, tuple):
            return self(*args[0])

        # TODO: exception


class TransactionFactory(IStrategy):
    def __call__(self, raw_actions: List[Any]) -> ICommand:
        actions: List[Action] = []
        for elem in raw_actions:
            actions.append(resolve("SimpleTransaction.CreateAction", elem))
        return Transaction(actions)
