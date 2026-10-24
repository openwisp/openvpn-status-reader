import collections
import datetime
import ipaddress
import re

from humanize.filesize import naturalsize
from netaddr import EUI, mac_unix

DATETIME_FORMAT_OPENVPN_V2_5 = "%Y-%m-%d %H:%M:%S"
DATETIME_FORMAT_OPENVPN_V2_4 = "%a %b %d %H:%M:%S %Y"
RE_VIRTUAL_ADDR_MAC = re.compile(r"^(?:[a-f0-9]{2}:){5}[a-f0-9]{2}(?:@\d+)?$", re.I)
RE_VIRTUAL_ADDR_NETWORK = re.compile("/(\\d{1,3})$")
RE_VIRTUAL_ADDR_CLIENT = re.compile("C$")


def parse_time(time):
    """Parses date and time from input string in OpenVPN logging format."""
    if isinstance(time, datetime.datetime):
        return time
    try:
        # Try the current numeric timestamp before the legacy format.
        return datetime.datetime.strptime(time, DATETIME_FORMAT_OPENVPN_V2_5)
    except ValueError:
        return datetime.datetime.strptime(time, DATETIME_FORMAT_OPENVPN_V2_4)


def parse_peer(peer):
    if isinstance(peer, PeerAddress):
        return peer
    for protocol in ("udp4:", "tcp4:", "udp6:", "tcp6:"):
        if peer.startswith(protocol):
            peer = peer.removeprefix(protocol)
            break
    host, port = peer.rsplit(":", 1)
    if host.startswith("[") and host.endswith("]"):
        host = host[1:-1]
    return PeerAddress(ipaddress.ip_address(host), int(port))


def parse_vaddr(virtual_addr):
    match = RE_VIRTUAL_ADDR_MAC.search(virtual_addr)
    if match:
        return EUI(virtual_addr.split("@")[0], dialect=mac_unix)

    match = RE_VIRTUAL_ADDR_NETWORK.search(virtual_addr)
    if match and 0 < int(match.group(1)) <= 128:
        return ipaddress.ip_network(virtual_addr)

    match = RE_VIRTUAL_ADDR_CLIENT.search(virtual_addr)
    if match:
        return ipaddress.ip_address(RE_VIRTUAL_ADDR_CLIENT.sub("", virtual_addr))

    return ipaddress.ip_address(virtual_addr)


def parse_filesize(size):
    if isinstance(size, FileSize):
        return size
    return FileSize(size)


class PeerAddress(collections.namedtuple("PeerAddress", "host port")):
    """The address of peer entity.

    :param host: The host address of peer entity.
    :type host: :class:`~ipaddress.IPv4Address` or
                :class:`~ipaddress.IPv6Address`
    :param port: The port of peer entity.
    :type port: :class:`int`
    """

    def __str__(self):
        return "{0}:{1}".format(self.host, self.port)


class FileSize(int):
    """The size of bytes."""

    def __str__(self):
        return self.humanize()

    def humanize(self, **kwargs):
        """Gets the human-friendly representation of file size.

        :param kwargs: All keyword arguments will be passed to
                       :func:`humanize.filesize.naturalsize`.
        """
        return naturalsize(self, **kwargs)
