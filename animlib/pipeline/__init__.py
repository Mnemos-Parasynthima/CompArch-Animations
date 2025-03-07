from os import path
from glob import glob
from importlib import import_module

module_files = glob(path.join(path.dirname(__file__), "*.py"))
modules = [path.basename(f)[:-3] for f in module_files if f.endswith(".py") and f != "__init__.py"]

modules.remove("__init__")

__all__ = []
for module in modules:
	_module = import_module(f".{module}", package=__name__)

	names = [name for name in dir(_module) if not name.startswith("_")]
	
	__all__.extend(names)
	globals().update({name: getattr(_module, name) for name in names})