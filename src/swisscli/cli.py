import sys

import click

from . import __version__
from .loader import discover_plugins
from .plugin import PluginRegistry


@click.command(context_settings=dict(
    help_option_names=[],
    ignore_unknown_options=True,
))
@click.argument("args", nargs=-1)
def main(args):
    """swisscli - CLI wrapper ecosystem."""

    discover_plugins()

    if not args:
        click.echo("Usage: swisscli <tool> [ARGS]...")
        click.echo("       swisscli --help")
        sys.exit(1)

    if args[0] in ("--help", "-h"):
        _show_help()
        return

    if args[0] in ("--version", "-V"):
        click.echo(f"swisscli version {__version__}")
        return

    tool = args[0]
    tool_args = list(args[1:])

    if tool_args and tool_args[0] in ("--help", "-h"):
        plugin = PluginRegistry.get(tool)
        if plugin:
            click.echo(plugin.format_help())
        else:
            click.echo(f"Unknown tool: {tool}", err=True)
        return

    plugin = PluginRegistry.get(tool)
    if plugin is None:
        click.echo(f"Error: unknown tool '{tool}'", err=True)
        click.echo("Run 'swisscli --help' for available tools.")
        sys.exit(1)

    if tool_args and tool_args[0] in plugin.subcommands:
        sub_name = tool_args[0]
        sub_args = tool_args[1:]
        if sub_args and sub_args[0] in ("--help", "-h"):
            click.echo(plugin.format_subcommand_help(plugin.subcommands[sub_name]))
            return

    sys.exit(plugin.execute(tool_args))


def _show_help():
    by_category = PluginRegistry.by_category()

    click.echo("Usage: swisscli <tool> [ARGS]...")
    click.echo()
    click.echo("Available tools:")
    click.echo()
    for category in sorted(by_category):
        tools = by_category[category]
        click.echo(f"  {category}:")
        for name in sorted(tools):
            plugin = tools[name]
            click.echo(f"    {name:<12} {plugin.description}")
        click.echo()
    click.echo("Run 'swisscli <tool> --help' for tool-specific help.")
