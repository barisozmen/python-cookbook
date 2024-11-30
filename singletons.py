from metaclasses import SingletonMetaclass

class Counter(metaclass=SingletonMetaclass):
    def __init__(self):
        self.count = 0
        
    @property
    def next_id(self):
        self.count += 1
        return self.count