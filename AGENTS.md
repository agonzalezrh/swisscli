# swisscli — AGENTS.md

## Build, install, test

```bash
pip install -e .                                    # editable install
python -m build                                     # sdist + wheel
python -m build && pip install dist/swisscli-0.1.0-py3-none-any.whl --force-reinstall
swisscli --help                                     # verify
```

No test framework, no lint, no typecheck — manual verification only.

## Architecture

- **`cli.py`** — single Click command with `help_option_names=[]` and `ignore_unknown_options=True`. All args via `nargs=-1`. `--help`/`--version` handled in user code (lines 25-55), not by Click.
- **`plugin.py`** — `Plugin` ABC, `Subcommand` (prefix/suffix args), `ArgMapper` (flag aliases), `PluginRegistry` (singleton dict keyed by `name`).
- **`loader.py`** — `discover_plugins()` uses `pkgutil.walk_packages` over `swisscli.plugins`. Every subpackage is scanned. Any module with a top-level `plugin` attribute is registered.
- **`__init__.py`** — version from `importlib.metadata` with fallback to `"0.1.0"`.

## Discovery & registration

- Plugin modules go under `src/swisscli/plugins/<category>/<tool>.py`.
- Every plugin module **must** export `plugin = ClassName()` at module level — this is the sole discovery contract.
- Categories are not hardcoded; they come from each plugin's `category` property.
- Existing categories: `web-cli` (curl, wget), `ssl` (openssl, ssh-keygen), `package` (apt, dnf, yum, dpkg, rpm).

## Two plugin patterns

**Simple flag mapping** — override `arg_mapper` property, args pass through:
```python
class CurlPlugin(Plugin):
    name = "curl"
    category = "web-cli"
    @property
    def arg_mapper(self):
        return ArgMapper({"--insecure": "-k"})
plugin = CurlPlugin()
```

**Subcommand-based** — override `subcommands` property. Each `Subcommand` has `prefix_args` (inserted between tool name and user args) and optional `suffix_args` / `arg_mapper`:
```python
class OpenSslPlugin(Plugin):
    name = "openssl"
    category = "ssl"
    @property
    def subcommands(self):
        return {
            "show": Subcommand(
                name="show", description="Show certificate details",
                prefix_args=["x509", "-in"], suffix_args=["-text", "-noout"],
            ),
        }
plugin = OpenSslPlugin()
```

## Fallback

If `shutil.which(tool_name)` fails, `execute()` scans `PluginRegistry.all()` for another plugin in the **same `category`** that is available. First match wins (insertion order). Prints fallback notice to stderr.

Example: on Debian, `swisscli dnf install curl` → `'dnf' not found, falling back to 'apt'`.

## Help system

- `swisscli --help` — tools grouped by category
- `swisscli <tool> --help` — subcommands + arg mappings
- `swisscli <tool> <subcommand> --help` — subcommand details + "Runs:" command preview
- `--help` is handled manually in `cli.py`, not by Click. Unknown options pass through silently.

## Style

- No docstrings or comments in code.
- `from __future__ import annotations` at top of `plugin.py`.
