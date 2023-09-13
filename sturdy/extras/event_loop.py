from abc import ABC, abstractmethod
from typing import Dict

from sturdy import resolve, ICommand


class IQueue(ABC):
    @abstractmethod
    def get(self) -> ICommand:
        ...

    @abstractmethod
    def put(self, command: ICommand) -> None:
        ...

    @abstractmethod
    def empty(self) -> bool:
        ...


class EventLoop(ICommand):
    def __init__(self, command_queue: IQueue) -> None:
        self.command_queue = command_queue
        self.stop = False
        self.behavior = self.__default_behavior

    def __call__(self) -> None:
        while not self.stop:
            self.behavior()

    def __default_behavior(self) -> None:
        try:
            cmd = self.command_queue.get()
            cmd()
        except Exception as e:
            resolve("Exception.Handle", e, cmd)()

    def set_stop(self):
        self.stop = True

    def set_behavior(self, new_behavior):
        self.behavior = new_behavior


class HardStopEventLoopCommand(ICommand):
    def __init__(self, event_loop: EventLoop) -> None:
        self.__event_loop = event_loop

    def __call__(self) -> None:
        self.__event_loop.set_stop()


class SoftStopEventLoopCommand(ICommand):
    def __init__(self, event_loop: EventLoop, action: ICommand) -> None:
        self.event_loop = event_loop
        self.action = action

    def __new_behavior(self):
        if self.event_loop.command_queue.empty():
            self.event_loop.set_stop()
            self.action()
            return
        try:
            cmd = self.event_loop.command_queue.get()
            cmd()
        except Exception as e:
            resolve("Exception.Handle", e, cmd)()

    def __call__(self) -> None:
        self.event_loop.set_behavior(self.__new_behavior)


class SetBehaviorEventLoop(ICommand):
    def __init__(self, event_loop: EventLoop, new_behavior) -> None:
        self.__event_loop = event_loop
        self.__new_behavior = new_behavior

    def __call__(self) -> None:
        self.__event_loop.set_behavior(self.__new_behavior)


def event_loop_new(id):
    ...


class LoadPluginCommand(ICommand):
    def __call__(self) -> None:
        event_loop_registry: Dict[str, EventLoop] = {}
        queue_registry: Dict[str, IQueue] = {}
        resolve("IoC.Register", "EventLoop.Registry.Get", lambda: event_loop_registry)
        resolve("IoC.Register", "EventLoop.Queue.Registry.Get", lambda: event_loop_registry)

        resolve(
            "IoC.Register",
            "EventLoop.Get",
            lambda event_loop_id: event_loop_registry[event_loop_id],
        )
        resolve(
            "IoC.Register",
            "EventLoop.Queue.Get",
            lambda event_loop_id: queue_registry[event_loop_id],
        )

        # EventLoop.Delete
        # EventLoop.Queue.Delete -> ICommand

        # EventLoop.SendCommand(event_loop_id, ICommand) -> ICommand

        # EventLoop.New(id) -> ICommand
        resolve("IoC.Register", "EventLoop.New", event_loop_new)
        # EventLoop.Delete(id) -> ICommand
