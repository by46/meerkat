import os.path
import re

_bottle_upload_filename_re = re.compile(r'^[a-z0-9_.!+-]+$', re.I)

_archive_suffix_rx = re.compile(
    r"(\.zip|\.tar\.gz|\.tgz|\.tar\.bz2|-py[23]\.\d-.*|"
    "\.win-amd64-py[23]\.\d\..*|\.win32-py[23]\.\d\..*|\.egg)$",
    re.I)
wheel_file_re = re.compile(
    r"""^(?P<namever>(?P<name>.+?)-(?P<ver>\d.*?))
    ((-(?P<build>\d.*?))?-(?P<pyver>.+?)-(?P<abi>.+?)-(?P<plat>.+?)
    \.whl|\.dist-info)$""",
    re.VERBOSE)

_pkgname_re = re.compile(r'-\d+[a-z_.!+]', re.I)
_pkgname_parts_re = re.compile(
    r"[\.\-](?=cp\d|py\d|macosx|linux|sunos|solaris|irix|aix|cygwin|win)",
    re.I)

pkg_normalize = re.compile('[\.\-]')


def is_valid_pkg_filename(fname):
    """See https://github.com/pypiserver/pypiserver/issues/102"""
    return _bottle_upload_filename_re.match(fname) is not None


def _guess_pkgname_and_version_wheel(basename):
    m = wheel_file_re.match(basename)
    if not m:
        return None, None
    name = m.group("name")
    ver = m.group("ver")
    build = m.group("build")
    if build:
        return name, ver + "-" + build
    else:
        return name, ver


def guess_pkgname_and_version(path):
    path = os.path.basename(path)
    if path.endswith(".asc"):
        path = path.rstrip(".asc")
    if path.endswith(".whl"):
        return _guess_pkgname_and_version_wheel(path)
    if not _archive_suffix_rx.search(path):
        return
    path = _archive_suffix_rx.sub('', path)
    if '-' not in path:
        pkgname, version = path, ''
    elif path.count('-') == 1:
        pkgname, version = path.split('-', 1)
    elif '.' not in path:
        pkgname, version = path.rsplit('-', 1)
    else:
        pkgname = _pkgname_re.split(path)[0]
        ver_spec = path[len(pkgname) + 1:]
        parts = _pkgname_parts_re.split(ver_spec)
        version = parts[0]
    return pkgname, version


def make_alias(pkg_name):
    return [pkg_name]


def normalize_pkg_name(pkg_name):
    """
    normalize pkg name , replace '.' and '-' to '_'
    and lower the pkg name
    :param pkg_name: pkg name
    :return: `class`:`bool`, `class`:`str`
    """
    pkg_name = pkg_name.lower()
    normalized = re.search(pkg_normalize, pkg_name) is not None
    if normalized:
        return normalized, re.sub(pkg_normalize, '_', pkg_name)
    return False, pkg_name
