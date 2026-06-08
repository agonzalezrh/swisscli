from swisscli.plugin import ArgMapper, Plugin


class CurlPlugin(Plugin):
    name = "curl"
    description = "Wrapper around curl for HTTP requests"
    category = "web-cli"

    @property
    def arg_mapper(self):
        return ArgMapper({
            "--insecure": "-k",
            "--silent": "-s",
            "--location": "-L",
            "--output": "-o",
            "--header": "-H",
            "--data": "-d",
        })


plugin = CurlPlugin()
