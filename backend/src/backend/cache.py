from shelved_cache import PersistentCache
from cachetools import TTLCache

filename = '/tmp/mycache'

cache = PersistentCache(TTLCache, filename, maxsize=1024, ttl=600)
