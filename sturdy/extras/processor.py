from abc import ABC, abstractmethod
from typing import Dict, Any
from queue import Queue

from sturdy import ICommand


class IProcessable(ABC):
    @abstractmethod
    def process(self) -> None:
        ...

    @abstractmethod
    def can_continue(self) -> bool:
        ...

    @abstractmethod
    def terminate(self, exception: Exception) -> None:
        ...


class Processable(IProcessable):
    def __init__(self, context: Dict[str, Any]) -> None:
        self.context = context

    def process(self) -> None:
        return self.context["process"]()

    def can_continue(self) -> bool:
        return self.context["can_continue"]()

    def terminate(self, exception: Exception) -> None:
        return self.context["terminate"](exception)


class InitContextCommand(ICommand):
    def __init__(self, context: Dict[str, Any]) -> None:
        self.context = context

    def __call__(self) -> None:
        self.context["queue"] = Queue()
        self.context["process"] = self.__process
        self.context["can_continue"] = lambda: True
        self.context["terminate"] = self.__terminate
        self.context["handle_exception"] = self.__handle_exception

    def __process(self) -> None:
        q: Queue[ICommand] = self.context["queue"]
        cmd = q.get()
        try:
            cmd()
        except Exception as e:
            self.context["handle_exception"](cmd, e)

    def __terminate(self, exception: Exception) -> None:
        self.context["can_continue"] = lambda: False
        self.context["terminate_exception"] = exception

    def __handle_exception(self, cmd: ICommand, exception: Exception):
        raise exception


def create_default_context() -> Dict[str, Any]:
    context: Dict[str, Any] = dict()
    InitContextCommand(context)()
    return context


class PutCommandInContextCommand(ICommand):
    def __init__(self, context: Dict[str, Any], command: ICommand) -> None:
        self.context = context
        self.command = command

    def __call__(self) -> None:
        q: Queue[ICommand] = self.context["queue"]
        q.put(self.command)


class Processor(ICommand):
    def __init__(self, processable: IProcessable) -> None:
        self.processable = processable

    def __call__(self) -> None:
        try:
            while self.processable.can_continue():
                self.processable.process()
        except Exception as e:
            self.processable.terminate(e)


class HardStopCommand(ICommand):
    def __init__(self, context: Dict[str, Any]) -> None:
        self.context = context

    def __call__(self) -> None:
        self.context["can_continue"] = lambda: False


class SoftStopCommand(ICommand):
    def __init__(self, context: Dict[str, Any]) -> None:
        self.context = context

    def __call__(self) -> None:
        previous_process = self.context["process"]

        def new_process():
            previous_process()
            q: Queue[ICommand] = self.context["queue"]
            if 0 == q.qsize():
                self.context["can_continue"] = lambda: False

        self.context["process"] = new_process


class LoadPluginCommand(ICommand):
    def __call__(self) -> None:
        ...
