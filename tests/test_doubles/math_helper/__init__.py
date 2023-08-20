from sturdy import resolve, ICommand


class LoadPluginCommand(ICommand):
    def __call__(self) -> None:
        resolve("IoC.Register", "MathHelper.add", lambda a, b: a + b)()
