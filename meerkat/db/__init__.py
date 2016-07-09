import redis

from meerkat import app
from meerkat import g
from meerkat.constants import PACKAGES


def get_db():
    if not hasattr(g, 'redis'):
        g.redis = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])
    return g.redis


class DataAccess(object):
    @staticmethod
    def total_packages():
        conn = get_db()
        return conn.scard(PACKAGES)
