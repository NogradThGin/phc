class ConfigError(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class OutputSizeMismatch(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message