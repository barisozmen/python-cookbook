from metaclasses import SingletonMetaclass

class Counter(metaclass=SingletonMetaclass):
    def __init__(self):
        self.count = 0
        
    @property
    def next_id(self):
        self.count += 1
        return self.count
    

class Config(metaclass=SingletonMetaclass):
    def __init__(self):
        self._settings = {}
    
    def set(self, key, value):
        self._settings[key] = value
        
    def get(self, key, default=None):
        return self._settings.get(key, default) 