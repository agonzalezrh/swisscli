from swisscli.plugin import ArgMapper, Plugin, Subcommand


class YumPlugin(Plugin):
    name = "yum"
    description = "RPM package manager (legacy)"
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
                    "--assumeyes": "-y",
                }),
            ),
            "remove": Subcommand(
                name="remove",
                description="Remove packages",
                prefix_args=["remove"],
                arg_mapper=ArgMapper({
                    "--yes": "-y",
                    "--assumeyes": "-y",
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
                prefix_args=["list", "installed"],
            ),
        }


plugin = YumPlugin()
