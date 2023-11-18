from shelved_cache import PersistentCache
from cachetools import TTLCache
from shelved_cache.decorators import asynccached

filename = 'mycache'


def momoized_async(ttl=5):
    return asynccached(PersistentCache(TTLCache, filename, maxsize=500, ttl=ttl))
