from typing import Any

class Cache:
    def __init__(self):
        self.cache: dict = {}
    
    def get(self, *args: list, key: Any = None, fallback: Any = {}) -> Any:
        if key:
            return self.cache.get(key, None)
        
        keys = args[0].split('.') if '.' in args[0] else None
        if keys is None:
            return None
        
        cache_value = None
        for key in keys:
            try:
                if cache_value is None:
                    cache_value = self.cache[key]
                    
                else:
                    cache_value = cache_value[key]
                
                # If the last key is reached, return the value
                if key == keys[-1]:
                    return cache_value
            except KeyError:
                pass
         
        if cache_value is None:
            return cache_value
        
    def set(self, *args, key: str | None = None, value: Any, return_value: bool = False) -> dict: 
        def dot_notation_to_dict(key, value) -> dict:
            # Initialize an empty dictionary to hold the result
            result = self.cache
            
            # Split the key using dot as the separator to get each level
            keys = key.split('.')
            
            for key in keys:
                d = result
                
                 # Iterate over each key except the last one to create nested dictionaries
                for k in keys[:-1]:
                    
                    # If the key doesn't exist in the current level, create a new dictionary
                    if k not in d:
                        d[k] = {}
                        
                    # Move to the next level in the dictionary
                    d = d[k]
                    
                # Set the value for the last key in the dot notation
                d[keys[-1]] = value
            return dict(result) if result else None
        
        if '.' not in key:
            cached_value = self.cache[key] = value
            if return_value:
                return cached_value
        
        else:
            cached_value = self.cache.update(dot_notation_to_dict(key, value))
            if return_value:
                return cached_value

    def delete(self, key: str):
        try:
            self.cache.pop(key)
        except KeyError:
            pass
    
    def return_cache(self):
        return self.cache

    def clear_cache(self):
        self.cache = {}

global_cache = Cache()
    
    
    

        