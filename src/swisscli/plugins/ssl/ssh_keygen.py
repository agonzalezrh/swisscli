from swisscli.plugin import ArgMapper, Plugin, Subcommand


class SshKeygenPlugin(Plugin):
    name = "ssh-keygen"
    description = "SSH key management tool"
    category = "ssl"

    @property
    def subcommands(self):
        return {
            "show": Subcommand(
                name="show",
                description="Show SSH key fingerprint",
                prefix_args=["-l", "-f"],
            ),
            "generate": Subcommand(
                name="generate",
                description="Generate an SSH key pair",
                prefix_args=["-t", "rsa", "-b", "4096", "-f", "key", "-N", ""],
                arg_mapper=ArgMapper({
                    "--type": "-t",
                    "--bits": "-b",
                    "--file": "-f",
                    "--comment": "-C",
                }),
            ),
        }


plugin = SshKeygenPlugin()
