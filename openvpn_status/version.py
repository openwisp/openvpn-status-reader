VERSION = (0, 3, 1, "final")


def get_version():
    version = "%s.%s.%s" % VERSION[:3]
    if VERSION[3:] == ("alpha", 0):
        return "%s pre-alpha" % version
    if VERSION[3].startswith("post"):
        return "%s.%s" % (version, VERSION[3])
    if VERSION[3] != "final":
        revision = VERSION[4] if len(VERSION) > 4 else 0
        return "%s%s%s" % (version, VERSION[3][0], revision)
    return version


__version__ = get_version()
