import sys

from setuptools import find_packages, setup

sys.path.insert(0, "openvpn_status")
from version import get_version

sys.path.remove("openvpn_status")

with open("README.rst") as readme:
    long_description = readme.read().strip()


setup(
    name="openvpn-status-reader",
    version=get_version(),
    url="https://github.com/openwisp/openvpn-status-reader",
    author="OpenWISP",
    author_email="support@openwisp.org",
    description="Parse OpenVPN status logs in Python",
    long_description=long_description,
    packages=find_packages(),
    zip_safe=False,
    license="MIT",
    keywords=["openvpn", "status", "log"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3.15",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: Log Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    install_requires=[
        "humanize>=4.16,<5",
        "netaddr>=1.3,<2",
    ],
    python_requires=">=3.11",
    platforms=["Any"],
)
