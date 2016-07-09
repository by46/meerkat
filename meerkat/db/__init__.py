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
        conn.zadd('packages:downloadtimes', key, 0)
        conn.hmset(key, info)
