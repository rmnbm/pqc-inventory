"""Command Line Interface for pqc-inventory."""

import argparse
import sys
from pathlib import Path

from pqc_inventory import __version__
from pqc_inventory.model import Exposure


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pqc-inventory",
        description="Cryptographic inventory and post-quantum readiness assessment.",
    )
    parser.add_argument(
        "--files",
        type=Path,
        default=None,
        metavar="DIR",
        help="Folder containing certificates and keys to inventory.",
    )
    parser.add_argument(
        "--tls",
        type=Path,
        default=None,
        metavar="FILE",
        help="File listing TLS targets. One per line using 'host:port'.",
    )
    parser.add_argument(
        "--ssh",
        type=Path,
        default=None,
        metavar="FILE",
        help="File listing SSH targets.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("out"),
        metavar="DIR",
        help="Target folder to store reports.",
    )
    parser.add_argument(
        "--exposure",
        type=Exposure,
        choices=list(Exposure),
        default=Exposure.UNKNOWN,
        help="Exposure of network targets, used for prioritisation.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Maximum waiting time of a network response, in seconds.",
    )
    parser.add_argument(
        "--delay", type=float, default=1.0, help="Pause between two hosts, in seconds."
    )
    parser.add_argument("--version", action="version", version=f"pqc-inventory {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not (args.files or args.tls or args.ssh):
        print(
            "Nothing to scan: specify at least --files, --tls or --ssh.",
            file=sys.stderr,
        )
        return 2
    return 0
