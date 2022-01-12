from sturdy.ioc import resolve
from sturdy.core.command import ICommand


class PluginLoadCommand(ICommand):
    def __call__(self) -> None:
        resolve("IoC.Register", "MathHelper.add", lambda *args: args[0] + args[1])()
