import unittest
from abc import abstractmethod
from typing import Any, Dict

from sturdy import resolve
from sturdy.deprecated.iuobject import IUObject


class UObject(IUObject):
    def __init__(self) -> None:
        self.__store: Dict = {}

    def get_property(self, name: str) -> Any:
        return self.__store[name]

    def set_property(self, name: str, value: Any) -> None:
        self.__store[name] = value


class IOneValue:
    @abstractmethod
    def get_value(self):
        ...

    @abstractmethod
    def set_value(self, value):
        ...


@unittest.skip("refactoring")
class TestAdapterGenerator(unittest.TestCase):
    def test_adapter_generate_class(self):
        resolve("Plugin.Load", "sturdy.extras.adapter_generator")()
        u_obj = UObject()
        AdapterClass = resolve("Adapter.GenerateClass", IOneValue)
        adapter_obj: IOneValue = AdapterClass(u_obj)

        val = 100
        adapter_obj.set_value(val)
        self.assertEqual(val, adapter_obj.get_value())

    def test_adapter_generate(self):
        resolve("Plugin.Load", "sturdy.extras.adapter_generator")()
        u_obj = UObject()
        adapter_obj: IOneValue = resolve("Adapter.Generate", IOneValue, u_obj)

        val = 100
        adapter_obj.set_value(val)
        self.assertEqual(val, adapter_obj.get_value())
