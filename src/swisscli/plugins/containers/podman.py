from swisscli.plugin import Plugin, Subcommand


class PodmanPlugin(Plugin):
    name = "podman"
    description = "Rootless container management tool"
    category = "containers"

    @property
    def subcommands(self):
        return {
            "ps": Subcommand(
                name="ps",
                description="List containers",
                prefix_args=["ps"],
            ),
            "images": Subcommand(
                name="images",
                description="List images",
                prefix_args=["images"],
            ),
            "pull": Subcommand(
                name="pull",
                description="Pull an image",
                prefix_args=["pull"],
            ),
            "run": Subcommand(
                name="run",
                description="Run a container",
                prefix_args=["run"],
            ),
            "stop": Subcommand(
                name="stop",
                description="Stop a container",
                prefix_args=["stop"],
            ),
            "rm": Subcommand(
                name="rm",
                description="Remove a container",
                prefix_args=["rm"],
            ),
            "rmi": Subcommand(
                name="rmi",
                description="Remove an image",
                prefix_args=["rmi"],
            ),
            "logs": Subcommand(
                name="logs",
                description="Show container logs",
                prefix_args=["logs"],
            ),
            "exec": Subcommand(
                name="exec",
                description="Execute a command in a container",
                prefix_args=["exec"],
            ),
        }


plugin = PodmanPlugin()
