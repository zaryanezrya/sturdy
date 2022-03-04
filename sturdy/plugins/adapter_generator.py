from typing import Any, TypeVar
from sturdy import resolve, ICommand, IUObject


class PluginLoadCommand(ICommand):
    def __call__(self) -> None:
        resolve("IoC.Register", "Adapter.GenerateClass", generate_adapter_class)()
        resolve("IoC.Register", "Adapter.Generate", generate_adapter)()


def adapter_constructor():
    def constructor(self, obj: IUObject):
        self.__obj = obj

    return constructor


def adapter_getter(property):
    def getter(self) -> Any:
        return self.__obj.get_property(property)

    return getter


def adapter_setter(property):
    def setter(self, val) -> None:
        self.__obj.set_property(property, val)

    return setter


T = TypeVar("T")


def generate_adapter_class(interface: T) -> T:
    attributes = {"__init__": adapter_constructor()}
    members = dir(interface)

    interface_setters = list(filter(lambda item: item.startswith("set_"), members))
    for setter in interface_setters:
        property = setter.replace("set_", "")
        attributes[setter] = adapter_setter(property)

    interface_getters = list(filter(lambda item: item.startswith("get_"), members))
    for getter in interface_getters:
        property = getter.replace("get_", "")
        attributes[getter] = adapter_getter(property)

    name = interface.__name__ + "Adapter"
    return type(name, (interface,), attributes)


def generate_adapter(interface, object: IUObject):
    Adapter = resolve("Adapter.GenerateClass", interface)
    return Adapter(object)
