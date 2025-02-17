from typing import Any

class Cache:
    def __init__(self):
        self.cache: dict = {}
    
    def get(self, key: str, fallback: Any = {}) -> Any:
        result = self.cache.get(key, fallback)
        return result
        
    def set(self, key: str, value: Any, return_value: bool = False):
        self.cache[key] = value
        
        if return_value:
            return value

    def delete(self, key: str):
        try:
            self.cache.pop(key)
        except KeyError:
            pass
    
    def return_cache(self):
        return self.cache

global_cache = Cache()
    
    
    

        