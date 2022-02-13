from typing import Any

from .exceptions import ResolveDependencyException
from sturdy.core.ioc.base.container import IOCBaseContainer


ioc_base_container = IOCBaseContainer()


def resolve(key: str, *args) -> Any:
    try:
        return ioc_base_container["IoC.Resolve"](key, *args)
    except ResolveDependencyException as e:
        raise e
    except Exception as e:
        raise ResolveDependencyException(
            f"An unexpected exception occurred with key: {key} and args: {args}: {e}"
        )
