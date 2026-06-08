from __future__ import annotations

import shutil
import subprocess
import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

import click


class ArgMapper:
    def __init__(self, mapping: Dict[str, str]):
        self._mapping = mapping

    def translate(self, args: List[str]) -> List[str]:
        result = []
        for arg in args:
            result.append(self._mapping.get(arg, arg))
        return result


class Subcommand:
    def __init__(
        self,
        name: str,
        description: str,
        prefix_args: Optional[List[str]] = None,
        suffix_args: Optional[List[str]] = None,
        arg_mapper: Optional[ArgMapper] = None,
    ):
        self.name = name
        self.description = description
        self.prefix_args = prefix_args or []
        self.suffix_args = suffix_args or []
        self.arg_mapper = arg_mapper

    def translate_args(self, args: List[str]) -> List[str]:
        if self.arg_mapper:
            return self.arg_mapper.translate(args)
        return list(args)

    def build_command(self, tool_name: str, args: List[str]) -> List[str]:
        return [tool_name, *self.prefix_args, *self.translate_args(args), *self.suffix_args]


class Plugin(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        ...

    @property
    def category(self) -> str:
        return "general"

    @property
    def arg_mapper(self) -> Optional[ArgMapper]:
        return None

    @property
    def subcommands(self) -> Dict[str, Subcommand]:
        return {}

    def translate_args(self, args: List[str]) -> List[str]:
        if self.arg_mapper:
            return self.arg_mapper.translate(args)
        return list(args)

    def build_command(self, args: List[str]) -> List[str]:
        return [self.name, *self.translate_args(args)]

    def _is_available(self) -> bool:
        return shutil.which(self.name) is not None

    def _get_fallback(self) -> Optional[Plugin]:
        for plugin in PluginRegistry.all().values():
            if plugin is not self and plugin.category == self.category and plugin._is_available():
                return plugin
        return None

    def execute(self, args: List[str]) -> int:
        if not self._is_available():
            fallback = self._get_fallback()
            if fallback is not None:
                click.echo(
                    f"'{self.name}' not found, falling back to '{fallback.name}'",
                    err=True,
                )
                return fallback.execute(args)
            click.echo(
                f"Error: '{self.name}' not found and no fallback available in category '{self.category}'.",
                err=True,
            )
            return 1

        if args and args[0] in self.subcommands:
            sub = self.subcommands[args[0]]
            cmd = sub.build_command(self.name, args[1:])
            return subprocess.call(cmd)

        cmd = self.build_command(args)
        return subprocess.call(cmd)

    def format_help(self) -> str:
        lines = [f"{self.name}: {self.description}", ""]
        if self.subcommands:
            lines.append("Subcommands:")
            for name, sub in self.subcommands.items():
                lines.append(f"  {name:<12} {sub.description}")
            lines.append("")
        if self.arg_mapper and self.arg_mapper._mapping:
            lines.append("Argument mappings:")
            for alias, native in self.arg_mapper._mapping.items():
                lines.append(f"  {alias} \u2192 {native}")
        lines.append("")
        lines.append(f"Category: {self.category}")
        return "\n".join(lines)

    def format_subcommand_help(self, sub: Subcommand) -> str:
        lines = [f"{self.name} {sub.name}: {sub.description}", ""]
        if sub.arg_mapper and sub.arg_mapper._mapping:
            lines.append("Argument mappings:")
            for alias, native in sub.arg_mapper._mapping.items():
                lines.append(f"  {alias} \u2192 {native}")
            lines.append("")
        lines.append(f"Runs: {' '.join(sub.build_command(self.name, ['<args>']))}")
        return "\n".join(lines)


class PluginRegistry:
    _plugins: Dict[str, Plugin] = {}

    @classmethod
    def register(cls, plugin: Plugin) -> None:
        cls._plugins[plugin.name] = plugin

    @classmethod
    def get(cls, name: str) -> Optional[Plugin]:
        return cls._plugins.get(name)

    @classmethod
    def all(cls) -> Dict[str, Plugin]:
        return dict(cls._plugins)

    @classmethod
    def by_category(cls) -> Dict[str, Dict[str, Plugin]]:
        result: Dict[str, Dict[str, Plugin]] = {}
        for name, plugin in cls._plugins.items():
            cat = plugin.category
            if cat not in result:
                result[cat] = {}
            result[cat][name] = plugin
        return result
