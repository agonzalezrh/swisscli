from swisscli.plugin import ArgMapper, Plugin, Subcommand


class AptPlugin(Plugin):
    name = "apt"
    description = "Debian/Ubuntu package manager"
    category = "package"

    @property
    def subcommands(self):
        return {
            "install": Subcommand(
                name="install",
                description="Install packages",
                prefix_args=["install"],
                arg_mapper=ArgMapper({
                    "--yes": "-y",
                    "--assume-yes": "-y",
                    "--no-install-recommends": "--no-install-recommends",
                    "--reinstall": "--reinstall",
                }),
            ),
            "remove": Subcommand(
                name="remove",
                description="Remove packages",
                prefix_args=["remove"],
                arg_mapper=ArgMapper({
                    "--yes": "-y",
                    "--assume-yes": "-y",
                    "--purge": "--purge",
                    "--autoremove": "--autoremove",
                }),
            ),
            "search": Subcommand(
                name="search",
                description="Search for packages",
                prefix_args=["search"],
            ),
            "list": Subcommand(
                name="list",
                description="List installed packages",
                prefix_args=["list", "--installed"],
            ),
        }


plugin = AptPlugin()
