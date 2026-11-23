OpenVPN Status Reader
=====================

.. image:: https://github.com/openwisp/openvpn-status-reader/actions/workflows/ci.yml/badge.svg?branch=master
    :target: https://github.com/openwisp/openvpn-status-reader/actions/workflows/ci.yml
    :alt: CI build status

.. image:: https://coveralls.io/repos/openwisp/openvpn-status-reader/badge.svg
    :target: https://coveralls.io/r/openwisp/openvpn-status-reader

.. image:: https://badge.fury.io/py/openvpn-status-reader.svg
    :target: https://badge.fury.io/py/openvpn-status-reader

.. image:: https://pepy.tech/badge/openvpn-status-reader
    :target: https://pepy.tech/project/openvpn-status-reader
    :alt: downloads

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://pypi.org/project/black/
    :alt: code style: black

.. summary-begin

**openvpn-status-reader** is an OpenWISP-maintained Python library for
parsing OpenVPN status-version-1 logs into Python data structures. It
supports both legacy and current numeric OpenVPN timestamps.

.. summary-end

This project is a fork of the original openvpn-status_ repository. It
retains the ``openvpn_status`` import namespace for compatibility.

It supports Python 3.11 and newer.

Installation
------------

.. code-block:: bash

    pip install openvpn-status-reader

Don't forget to put it in ``setup.py`` / ``requirements.txt``.

Getting Started
---------------

You could configure your OpenVPN server to log for client status. In usual
it could be achieved by adding ``status /path/to/openvpn-status.log`` line
to ``/etc/openvpn/openvpn.conf``. For example:

::

    proto udp
    port 1194
    dev tun0
    status /var/run/openvpn-status.log

Once OpenVPN server running, the log file will be created and written. It
looks like:

::

    OpenVPN CLIENT LIST
    Updated,Thu Jun 18 08:12:15 2015
    Common Name,Real Address,Bytes Received,Bytes Sent,Connected Since
    foo@example.com,10.10.10.10:49502,334948,1973012,Thu Jun 18 04:23:03 2015
    bar@example.com,10.10.10.10:64169,1817262,28981224,Thu Jun 18 04:08:39 2015
    ROUTING TABLE
    Virtual Address,Common Name,Real Address,Last Ref
    192.168.255.134,foo@example.com,10.10.10.10:49502,Thu Jun 18 08:12:09 2015
    192.168.255.126,bar@example.com,10.10.10.10:64169,Thu Jun 18 08:11:55 2015
    GLOBAL STATS
    Max bcast/mcast queue length,0
    END

Now we could parse log file with this library:

.. code-block:: python

    from openvpn_status import parse_status

    with open("/var/run/openvpn-status.log") as logfile:
        status = parse_status(logfile.read())

    print(status.updated_at)  # datetime.datetime(2015, 6, 18, 8, 12, 15)

    foo_client = status.client_list["169.254.0.1"]
    print(foo_client.common_name)  # foo@example.com
    print(foo_client.bytes_received)  # 334.9 kB
    print(foo_client.bytes_sent)  # 2.0 MB
    print(int(foo_client.bytes_sent))  # 2097152

More details are in the `API reference`_.

.. _api reference: https://openvpn-status-reader.readthedocs.io/en/latest/api.html

.. _openvpn-status: https://github.com/sgares/openvpn-status

Tests
-----

Run the test suite with ``./runtests``. To run one test, pass its path:

.. code-block:: shell

    ./runtests tests/test_package_meta.py::test_shortcut

The entry point accepts test paths under ``tests/`` and the ``-q``,
``-v``, ``-x``, and ``--cov-report=xml`` options.
