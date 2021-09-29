from sturdy.ioc import resolve
from sturdy.ioc.interfaces import IResolveDependencyStrategy
from sturdy.interfaces import ICommand

from .interfaces import IPlugin


class PluginManager(IPlugin):
    def get_load_command(self) -> ICommand:
        return PluginManagerLoadCommand()

    def get_unload_command(self) -> ICommand:
        return PluginManagerUnloadCommand()


class PluginManagerLoadCommand(ICommand):
    def __call__(self) -> None:
        resolve("IoC.Register", "Plugins.Register", PluginsRegisterCommandResolver())()


class PluginManagerUnloadCommand(ICommand):
    def __call__(self) -> None:
        ...


class PluginsRegisterCommandResolver(IResolveDependencyStrategy):
    def __call__(self, plugin: IPlugin) -> ICommand:
        return PluginsRegisterCommand(plugin)


class PluginsRegisterCommand(ICommand):
    def __init__(self, plugin: IPlugin):
        self.plugin = plugin

    def __call__(self) -> None:
        plugin_load_command = self.plugin.get_load_command()
        plugin_load_command()
