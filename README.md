# swisscli

A plugin-based CLI wrapper ecosystem for common command-line tools. swisscli wraps native tools like `curl`, `wget`, `openssl`, `ssh-keygen`, `apt`, `dnf`, `yum`, `dpkg`, and `rpm`, providing consistent argument naming, subcommand interfaces, and automatic fallback between tools in the same category.

## Installation

```bash
git clone https://github.com/agonzalezrh/swisscli.git
cd swisscli
pip install .
```

Or install directly:

```bash
pip install swisscli
```

## Usage

```bash
swisscli --help                    # list tools grouped by category
swisscli --version                 # show version
swisscli <tool> --help             # tool-specific help
swisscli <tool> <subcommand> --help  # subcommand details
swisscli <tool> [ARGS]...          # run a tool
```

## Available tools

### web-cli

| Tool | Description |
|------|-------------|
| `curl` | HTTP requests with long-flag aliases (`--insecure` → `-k`, `--silent` → `-s`, `--location` → `-L`, etc.) |
| `wget` | File downloads with long-flag aliases (`--insecure` → `--no-check-certificate`, `--quiet` → `-q`, etc.) |

```bash
swisscli curl --insecure --location https://example.com
swisscli wget --output file.zip https://example.com/file.zip
```

### ssl

| Tool | Subcommands | Description |
|------|-------------|-------------|
| `openssl` | `show`, `generate` | OpenSSL certificate toolkit |
| `ssh-keygen` | `show`, `generate` | SSH key management tool |

```bash
swisscli openssl show cert.pem
swisscli openssl generate --days 730 --out mycert.pem
swisscli ssh-keygen show ~/.ssh/id_rsa
swisscli ssh-keygen generate --type ed25519 --file mykey
```

### package

| Tool | Subcommands | Description |
|------|-------------|-------------|
| `apt` | `install`, `remove`, `search`, `list` | Debian/Ubuntu package manager |
| `dnf` | `install`, `remove`, `search`, `list` | RPM package manager (modern) |
| `yum` | `install`, `remove`, `search`, `list` | RPM package manager (legacy) |
| `dpkg` | `list`, `info`, `search`, `contents` | Debian low-level package manager |
| `rpm` | `list`, `info`, `search`, `files` | RPM low-level package manager |

```bash
swisscli apt install curl
swisscli apt remove --purge firefox
swisscli apt search build-essential
swisscli dpkg list
swisscli dpkg info bash
swisscli rpm list
swisscli rpm files coreutils
```

## Fallback behavior

If a tool binary is not found on the system, swisscli automatically falls back to another tool in the same category. For example, running `swisscli dnf install curl` on a Debian system will fall back to `apt install curl`. The fallback notice is printed to stderr.

## Adding your own plugin

Create a file at `src/swisscli/plugins/<category>/<tool>.py`. Define a `Plugin` subclass with a `name`, `description`, and `category`. Export a module-level `plugin = MyPlugin()` instance — auto-discovery picks it up on next run.

Two patterns:
- **Simple flag mapping** — override `arg_mapper` for long-flag aliases
- **Subcommand-based** — override `subcommands` dict with `Subcommand` objects (prefix args, suffix args, optional arg mapper)

## Architecture

- **Plugin** — base class wrapping a CLI tool (argument mapping, execution, fallback)
- **ArgMapper** — translates user-friendly long flags to native tool flags
- **Subcommand** — defines prefix/suffix args injected between tool name and user args
- **PluginRegistry** — singleton registry discovered automatically via `pkgutil.walk_packages`
- **Categories** — plugins grouped by domain; fallback operates within the same category
