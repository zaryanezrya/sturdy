from sturdy.ioc import resolve
from sturdy.interfaces import ICommand
from sturdy.plugins.interfaces import IPlugin


class Plugin(IPlugin):
    def get_load_command(self) -> ICommand:
        return PluginLoadCommand()

    def get_unload_command(self) -> ICommand:
        ...


class PluginLoadCommand(ICommand):
    def __call__(self) -> None:
        resolve("IoC.Register", "MathHelper.add", lambda *args: args[0] + args[1])()
