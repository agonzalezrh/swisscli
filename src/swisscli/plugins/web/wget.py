from swisscli.plugin import ArgMapper, Plugin


class WgetPlugin(Plugin):
    name = "wget"
    description = "Wrapper around wget for downloading files"
    category = "web-cli"

    @property
    def arg_mapper(self):
        return ArgMapper({
            "--insecure": "--no-check-certificate",
            "--quiet": "-q",
            "--output": "-O",
            "--timeout": "-T",
        })


plugin = WgetPlugin()
