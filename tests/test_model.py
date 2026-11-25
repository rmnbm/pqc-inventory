"""Tests for model.py."""

import json
from dataclasses import replace
from datetime import date

import pytest

from pqc_inventory.model import CryptoUsage, Exposure, Function, Source


def make_usage(**kwargs) -> CryptoUsage:
    defaults = {
        "source": Source.TLS,
        "target": "example.com:443",
        "function": Function.KEY_EXCHANGE,
        "algorithm": "X25519",
    }
    return CryptoUsage(**(defaults | kwargs))


def test_function_compares_as_string():
    assert Function.KEY_EXCHANGE == "key_exchange"


def test_exposure_from_string():
    assert Exposure("internet") is Exposure.INTERNET


def test_unknown_value_is_rejected():
    with pytest.raises(ValueError):
        Exposure("moon")


def test_minimal_usage_has_defaults():
    usage = make_usage()
    assert usage.key_size is None
    assert usage.expires is None
    assert usage.error is None
    assert usage.risk is None
    assert usage.details == ""
    assert usage.exposure is Exposure.UNKNOWN


def test_usages_with_the_same_values_are_equal():
    a = make_usage()
    b = make_usage()
    assert a == b
    assert a != replace(a, key_size=4096)


def test_to_dict_converts_date_to_iso_string():
    usage = make_usage(expires=date(2027, 3, 1))
    assert usage.to_dict()["expires"] == "2027-03-01"


def test_to_dict_converts_enums_to_plain_string():
    usage = make_usage(exposure=Exposure.INTERNET)
    dict_usage = usage.to_dict()
    assert type(dict_usage["source"]) is str
    assert type(dict_usage["function"]) is str
    assert type(dict_usage["exposure"]) is str


def test_to_dict_json_is_serializable():
    usage = make_usage(expires=date(2027, 3, 1))
    json.dumps(usage.to_dict())


def test_field_names_starts_with_required_fields():
    assert CryptoUsage.field_names()[:4] == ["source", "target", "function", "algorithm"]
