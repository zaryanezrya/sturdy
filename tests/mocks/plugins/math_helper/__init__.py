from sturdy import resolve, ICommand


class PluginLoadCommand(ICommand):
    def __call__(self) -> None:
        resolve("IoC.Register", "MathHelper.add", lambda *args: args[0] + args[1])()
