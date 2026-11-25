# pqc-inventory

Cryptographic inventory and post-quantum readiness assessment.

`pqc-inventory` lists the cryptography used by TLS endpoints, SSH servers and
local certificate and key files, then ranks each finding by its exposure to
quantum attacks.

> **Status:** early development. The command-line interface is in place;
> scanners, risk classification and reports are not implemented yet.

## Requirements

- Python 3.11 or later

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

The `-e` flag installs the package in editable mode: changes under `src/` take
effect without reinstalling. Reinstall after editing `pyproject.toml`.

## Usage

```bash
pqc-inventory --files ./certs
pqc-inventory --tls targets.txt --exposure internet
pqc-inventory --help
```

At least one of `--files`, `--tls` or `--ssh` is required.

| Option | Default | Description |
|---|---|---|
| `--files DIR` | | Directory of certificates and keys to inventory |
| `--tls FILE` | | File listing TLS targets, one `host:port` per line |
| `--ssh FILE` | | File listing SSH targets |
| `--out DIR` | `out` | Directory where reports are written |
| `--exposure` | `unknown` | Exposure of network targets: `internet`, `internal` or `unknown` |
| `--timeout` | `5.0` | Network timeout in seconds |
| `--delay` | `1.0` | Delay between hosts in seconds |
| `--version` | | Print the version and exit |

Exit codes: `0` on success, `2` on invalid usage.

## Development

```bash
pytest            # run the tests
ruff check .      # lint
ruff format .     # format
```

## License

MIT