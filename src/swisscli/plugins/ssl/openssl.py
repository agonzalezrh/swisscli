from swisscli.plugin import ArgMapper, Plugin, Subcommand


class OpenSslPlugin(Plugin):
    name = "openssl"
    description = "OpenSSL certificate toolkit"
    category = "ssl"

    @property
    def subcommands(self):
        return {
            "show": Subcommand(
                name="show",
                description="Show certificate details",
                prefix_args=["x509", "-in"],
                suffix_args=["-text", "-noout"],
            ),
            "generate": Subcommand(
                name="generate",
                description="Generate a self-signed certificate",
                prefix_args=[
                    "req", "-x509", "-newkey", "rsa:4096",
                    "-keyout", "key.pem", "-out", "cert.pem",
                    "-days", "365", "-nodes",
                    "-subj", "/CN=SelfSigned",
                ],
                arg_mapper=ArgMapper({
                    "--days": "-days",
                    "--keyout": "-keyout",
                    "--out": "-out",
                    "--subj": "-subj",
                }),
            ),
        }


plugin = OpenSslPlugin()
