"""Data model for a single cryptographic usage.

A usage is one algorithm, observed at one location, serving one function.
For example, on `example.com:443` the TLS key exchange uses X25519.
A single endpoint therefore yields several rows: protocol, key exchange,
cipher, and the key and signature of each certificate in the chain.
"""

from dataclasses import asdict, dataclass, fields
from datetime import date
from enum import StrEnum


class Source(StrEnum):
    TLS = "tls"
    SSH = "ssh"
    FILE = "file"


class Function(StrEnum):
    """Cryptographic role of an algorithm.

    The role drives migration urgency. Key exchange is exposed to
    "harvest now, decrypt later": recorded traffic can be decrypted once a
    quantum computer exists. Signatures and certificate keys cannot be broken
    retroactively. Symmetric ciphers are only weakened by Grover's algorithm.
    """

    PROTOCOL = "protocol"
    KEY_EXCHANGE = "key_exchange"
    CIPHER = "cipher"
    CERT_KEY = "cert_key"
    SIGNATURE = "signature"
    HOST_KEY = "host_key"
    PRIVATE_KEY = "private_key"
    PUBLIC_KEY = "public_key"

    ERROR = "error"  # Not a cryptographic role: marks a failed scan


class Exposure(StrEnum):
    INTERNET = "internet"
    INTERNAL = "internal"
    UNKNOWN = "unknown"


@dataclass
class CryptoUsage:
    """One row of the inventory."""

    source: Source
    target: str  # "host:port" or file path
    function: Function
    algorithm: str  # normalized name, e.g. "RSA", "X25519"
    key_size: int | None = None  # bits
    details: str = ""
    expires: date | None = None
    exposure: Exposure = Exposure.UNKNOWN
    error: str | None = None

    # Set by the classifier
    risk: str | None = None
    priority: str | None = None
    recommendation: str | None = None

    def to_dict(self) -> dict[str, str | int | None]:
        """Convert a CryptoUsage object to a dict."""

        d = asdict(self)
        if d["expires"] is not None:
            d["expires"] = d["expires"].isoformat()
        for element in ("source", "function", "exposure"):
            d[element] = str(d[element])
        return d

    @staticmethod
    def field_names() -> list[str]:
        """Return a list of the field names of a CryptoUsage object."""
        return [f.name for f in fields(CryptoUsage)]
