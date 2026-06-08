#src/utils/cache.py
from cachetools import TTLCache


class CacheManager:
    def __init__(self, ttl):
        self.ttl = ttl
        self.cache = TTLCache(maxsize=500, ttl=self.ttl)
        
    
    def get(self,key):
        value = self.cache.get(key, None)
        return value
    
    def set(self, key, value):
        self.cache[key] = value
        
    def delete(self, key):
        self.cache.pop(key, None)
        
    def clear(self):
        self.cache.clear()          