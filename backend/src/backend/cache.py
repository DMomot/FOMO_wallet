from shelved_cache import PersistentCache
from cachetools import TTLCache
from shelved_cache.decorators import asynccached

filename = '/tmp/mycache'

cache = PersistentCache(TTLCache, filename, maxsize=5, ttl=5)

def momoized_async():
    return asynccached(cache)
