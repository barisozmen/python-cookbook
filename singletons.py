class Counter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Counter, cls).__new__(cls)
            cls._instance.count = 0
        return cls._instance

    def next_id(self):
        self.count += 1
        return self.count