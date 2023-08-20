import importlib

from .command import ICommand, CommandException


def load_plugin_command_factory(uri: str) -> ICommand:
    return LoadPluginCommand(uri)


class LoadPluginCommand(ICommand):
    def __init__(self, plugin_uri: str) -> None:
        self.__plugin_uri = plugin_uri

    def __call__(self) -> None:
        try:
            plugin = importlib.import_module(self.__plugin_uri)
        except ModuleNotFoundError:
            raise CommandException(f"Module {self.__plugin_uri} not found")

        try:
            lpc = plugin.LoadPluginCommand()
            lpc()
        except AttributeError:
            raise CommandException(
                f"Module {self.__plugin_uri} doesn't contain a LoadPluginCommand"
            )
