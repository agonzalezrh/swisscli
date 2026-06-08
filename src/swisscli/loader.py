import importlib
import pkgutil
import warnings

from .plugin import PluginRegistry


def _import_module(modname: str):
    try:
        return importlib.import_module(modname)
    except Exception as exc:
        warnings.warn(f"Failed to load plugin module '{modname}': {exc}")
        return None


def discover_plugins() -> None:
    import swisscli.plugins as plugins_pkg

    prefix = plugins_pkg.__name__ + "."
    seen = set()

    for importer, modname, ispkg in pkgutil.walk_packages(
        plugins_pkg.__path__, prefix=prefix
    ):
        if ispkg or modname in seen:
            continue
        seen.add(modname)
        mod = _import_module(modname)
        if mod is not None and hasattr(mod, "plugin"):
            PluginRegistry.register(mod.plugin)
