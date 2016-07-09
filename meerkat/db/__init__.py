import time

import redis

from meerkat import app
from meerkat import g
from meerkat import utils
from meerkat.constants import PACKAGES
from meerkat.constants import SIMPLES


def get_db():
    if not hasattr(g, 'redis'):
        g.redis = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])
    return g.redis


class DataAccess(object):
    # -------------------------------------
    # package
    # -------------------------------------
    @staticmethod
    def total_packages():
        conn = get_db()
        return conn.scard(PACKAGES)

    @staticmethod
    def add_package(filename, pkg_name, version, md5, url):
        conn = get_db()
        safe_filename = filename.lower()
        conn.sadd(PACKAGES, filename)
        conn.sadd(SIMPLES, pkg_name)

        _, pkg_name = utils.normalize_pkg_name(pkg_name)
        key = 'packages:{0}'.format(pkg_name)
        conn.sadd(key, filename)

        key = 'package:{0}'.format(safe_filename)
        info = dict(md5=md5, url=url, timestamp=time.time(), filename=filename, version=version)
        conn.hmset(key, info)
        DataAccess.add_download_score(filename, 0)

    @staticmethod
    def get_packages():
        conn = get_db()
        return conn.smembers(PACKAGES)

    @staticmethod
    def get_package(filename):
        conn = get_db()
        package_key = 'package:{0}'.format(filename.lower())
        return conn.hgetall(package_key)

    @staticmethod
    def has_package_file(filename):
        conn = get_db()
        key = 'package:{0}'.format(filename.lower())
        return conn.exists(key)

    @staticmethod
    def get_libs():
        conn = get_db()
        return conn.smembers(SIMPLES)

    @staticmethod
    def has_lib(lib_name):
        conn = get_db()
        key = 'packages:{0}'.format(lib_name.lower())
        return conn.exists(key)

    @staticmethod
    def get_packages_by_lib(lib_name):
        conn = get_db()
        key = 'packages:{0}'.format(lib_name.lower())
        return conn.smembers(key)

    # -------------------------------------
    # download score
    # -------------------------------------
    @staticmethod
    def add_download_score(filename, score=1):
        conn = get_db()
        conn.zincrby('score:total', filename.lower(), score)

    @staticmethod
    def get_download_range(start=0, end=-1):
        conn = get_db()
        return conn.zrevrange('score:total', start, end, withscores=True)
