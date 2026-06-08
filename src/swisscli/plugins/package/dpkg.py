from swisscli.plugin import Plugin, Subcommand


class DpkgPlugin(Plugin):
    name = "dpkg"
    description = "Debian package manager (low-level)"
    category = "package"

    @property
    def subcommands(self):
        return {
            "list": Subcommand(
                name="list",
                description="List installed packages",
                prefix_args=["-l"],
            ),
            "info": Subcommand(
                name="info",
                description="Show package info",
                prefix_args=["-s"],
            ),
            "search": Subcommand(
                name="search",
                description="Search which package owns a file",
                prefix_args=["-S"],
            ),
            "contents": Subcommand(
                name="contents",
                description="List files installed by a package",
                prefix_args=["-L"],
            ),
        }


plugin = DpkgPlugin()
