from smartbotsol.singleton import Singleton

class Cache(object):
    """Cache interface"""

    __metaclass__ = Singleton

    STORE = None
    
    def get(self, parameter):
        raise NotImplementedError

    def add(self, key, value):
        raise NotImplementedError

    def to_dict(self):
        """Serializer"""
        raise NotImplementedError

    def from_dict(self, fdict):
        """Deserializer"""
        raise NotImplementedError
