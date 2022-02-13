import importlib
from typing import Any

from sturdy.core.command import ICommand, CommandException
from sturdy.core.strategy import IStrategy


class IOCBaseLoadPluginCommandResolver(IStrategy):
    def __call__(self, plugin_uri: str) -> Any:
        return IOCBaseLoadPluginCommand(plugin_uri)


class IOCBaseLoadPluginCommand(ICommand):
    def __init__(self, plugin_uri: str) -> None:
        self.__plugin_uri = plugin_uri

    def __call__(self) -> None:
        try:
            plugin = importlib.import_module(self.__plugin_uri)
        except ModuleNotFoundError:
            raise CommandException(f"Module {self.__plugin_uri} not found")

        # TODO: exceptions
        load_command = plugin.PluginLoadCommand()
        load_command()
