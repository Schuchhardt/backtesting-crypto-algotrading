import importlib
from types import ModuleType


ALGORITHMS_PACKAGE = 'algorithms'


def load_algorithm(slug: str) -> ModuleType:
    """Load algorithm module by slug."""
    module_name = f"{ALGORITHMS_PACKAGE}.{slug}"
    return importlib.import_module(module_name)
