from swisscli.plugin import Plugin, Subcommand


class RpmPlugin(Plugin):
    name = "rpm"
    description = "RPM package manager (low-level)"
    category = "package"

    @property
    def subcommands(self):
        return {
            "list": Subcommand(
                name="list",
                description="List installed packages",
                prefix_args=["-qa"],
            ),
            "info": Subcommand(
                name="info",
                description="Show package info",
                prefix_args=["-qi"],
            ),
            "search": Subcommand(
                name="search",
                description="Search installed packages",
                prefix_args=["-q"],
            ),
            "files": Subcommand(
                name="files",
                description="List files in a package",
                prefix_args=["-ql"],
            ),
        }


plugin = RpmPlugin()
