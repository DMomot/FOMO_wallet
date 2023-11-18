from shelved_cache import PersistentCache
from cachetools import TTLCache
from shelved_cache.decorators import asynccached

filename = '/tmp/mycache'


def momoized_async(ttl=5):
    return asynccached(PersistentCache(TTLCache, filename, maxsize=50, ttl=ttl))
