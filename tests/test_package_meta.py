from pytest import mark, raises

import openvpn_status
from openvpn_status import version as version_module
from openvpn_status.version import get_version


def test_shortcut():
    with raises(openvpn_status.ParsingError):
        openvpn_status.parse_status("")
    with raises(openvpn_status.ParsingError):
        openvpn_status.parse_status(b"")


@mark.parametrize(
    "version, expected",
    [
        ((1, 2, 3, "alpha", 0), "1.2.3 pre-alpha"),
        ((1, 2, 3, "post1"), "1.2.3.post1"),
        ((1, 2, 3, "beta", 4), "1.2.3b4"),
        ((1, 2, 3, "rc"), "1.2.3r0"),
    ],
)
def test_get_version(monkeypatch, version, expected):
    monkeypatch.setattr(version_module, "VERSION", version)
    assert get_version() == expected
