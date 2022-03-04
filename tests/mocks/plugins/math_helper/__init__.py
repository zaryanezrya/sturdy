from sturdy import resolve, ICommand


class PluginLoadCommand(ICommand):
    def __call__(self) -> None:
        resolve("IoC.Register", "MathHelper.add", lambda a, b: a + b)()
