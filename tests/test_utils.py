from datetime import datetime
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network

from netaddr import EUI, mac_unix
from pytest import mark

from openvpn_status.utils import (
    FileSize,
    PeerAddress,
    parse_filesize,
    parse_peer,
    parse_time,
    parse_vaddr,
)


@mark.parametrize(
    "text,time",
    [
        ("Thu Jun 18 04:23:03 2015", datetime(2015, 6, 18, 4, 23, 3)),
        ("Thu Jun 18 04:08:39 2015", datetime(2015, 6, 18, 4, 8, 39)),
        ("Thu Jun 18 07:57:25 2015", datetime(2015, 6, 18, 7, 57, 25)),
        ("2026-10-20 17:48:08", datetime(2026, 10, 20, 17, 48, 8)),
        (datetime(2015, 6, 18, 7, 57, 25), datetime(2015, 6, 18, 7, 57, 25)),
    ],
)
def test_parse_time(text, time):
    assert parse_time(text) == time


@mark.parametrize(
    "text,peer",
    [
        ("10.0.0.1:49502", PeerAddress(IPv4Address("10.0.0.1"), 49502)),
        ("10.0.0.2:64169", PeerAddress(IPv4Address("10.0.0.2"), 64169)),
        ("10.0.0.3:63414", PeerAddress(IPv4Address("10.0.0.3"), 63414)),
        (PeerAddress("10.0.0.1", 80), PeerAddress("10.0.0.1", 80)),
    ],
)
def test_parse_peer(text, peer):
    assert parse_peer(text) == peer
    assert str(text) == str(peer)


@mark.parametrize(
    "text,peer",
    [
        ("udp4:181.126.36.3:1194", PeerAddress(IPv4Address("181.126.36.3"), 1194)),
        ("tcp4:181.126.36.4:1194", PeerAddress(IPv4Address("181.126.36.4"), 1194)),
        ("udp6:[2001:db8::3]:1194", PeerAddress(IPv6Address("2001:db8::3"), 1194)),
        ("tcp6:[2001:db8::4]:1194", PeerAddress(IPv6Address("2001:db8::4"), 1194)),
    ],
)
def test_parse_transport_prefixed_peer(text, peer):
    assert parse_peer(text) == peer


@mark.parametrize(
    "text,virtual_addr",
    [
        ("10.0.0.1", IPv4Address("10.0.0.1")),
        ("2001:db8:2de::e13", IPv6Address("2001:db8:2de::e13")),
        ("10.200.0.0/16", IPv4Network("10.200.0.0/16")),
        ("2001:db8::1000/124", IPv6Network("2001:db8::1000/124")),
        ("28:d2:44:d4:e6:ea", EUI("28:d2:44:d4:e6:ea", dialect=mac_unix)),
    ],
)
def test_parse_vaddr(text, virtual_addr):
    assert parse_vaddr(text) == virtual_addr
    assert str(text) == str(virtual_addr)


def test_parse_vaddr_with_interface_index():
    assert parse_vaddr("28:d2:44:d4:e6:ea@5") == EUI(
        "28:d2:44:d4:e6:ea", dialect=mac_unix
    )


@mark.parametrize(
    "text,humanized",
    [
        (10240, "10.2 kB"),
        ("10240", "10.2 kB"),
        (FileSize(10240), "10.2 kB"),
    ],
)
def test_parse_filesize(text, humanized):
    assert str(parse_filesize(text)) == humanized
