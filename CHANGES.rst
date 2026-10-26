Changelog
=========

Version 0.3.1 [2026-10-26]
--------------------------

Bugfixes
~~~~~~~~

- Normalized OpenVPN status peer addresses

Version 0.3.0 [2026-10-20]
--------------------------

Changes
~~~~~~~

Other changes
+++++++++++++

- Renamed package to OpenVPN Status Reader

  The distribution and repository now use openvpn-status-reader while the
  openvpn_status import remains compatible.

- Added compatibility with OpenVPN 2.5+.

Dependencies
++++++++++++

- Removed Python 2 compatibility

  Python 3.11 is the minimum supported version, so six and the
  compatibility constructs are no longer needed.

- Upgraded all dependencies.

Bugfixes
~~~~~~~~

- Rejected malformed status schemas

  Malformed status logs now raise ParsingError instead of uncaught
  KeyError.

Version 0.2.2 [2023-01-11]
--------------------------

- Fix GH-14: u'192.168.100.110C' does not appear to be an IPv4 or IPv6
  address (GH-17, thanks to @mrevilme)
- Update for Python 3.10+ compatibility

Version 0.2.1 [2019-08-27]
--------------------------

- Fix GH-11: Fix the parser which throws ``ValueError`` on interrupted
  stream.

Version 0.2.0 [2017-10-20]
--------------------------

- Feature GH-1: Add support to TAP mode of OpenVPN servers by parsing
  virtual addresses as MAC and IP both.
- Feature GH-4: Add support to client-config-dir (ccd) and iroute.
- Fix GH-2: **BREAK-COMPATIBILITY** Use real or virtual addresses as the
  key of client_list and routing_table, instead of using common name.

Version 0.1.1 [2016-06-29]
--------------------------

- Fix GH-3: The depended six must later than 1.9.0 because we need the
  "python_2_unicode_compatible" decorator.

Version 0.1.0 [2015-06-19]
--------------------------

The first release.
