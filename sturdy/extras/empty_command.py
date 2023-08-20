from sturdy import resolve, ICommand


class LoadPluginCommand(ICommand):
    def __call__(self) -> None:
        empty_command = EmptyCommand()
        resolve("IoC.Register", "EmptyCommand", lambda: empty_command)()


class EmptyCommand(ICommand):
    def __call__(self) -> None:
        ...
