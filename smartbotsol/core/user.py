from smartbotsol import BaseState

class User(object):
    def __init__(self, uid):
        self.uid = uid
        self.state = None
        self.lang = 'ru'

    def __eq__(self, other):
        if self.uid == other.uid:
            return True
        return False

    def to_dict(self):
        data = dict()

        for key in iter(self.__dict__):

            value = self.__dict__[key]
            
            if isinstance(value, BaseState):
                value = value.__class__.__name__

            if value is not None:
                if hasattr(value, 'to_dict'):
                    data[key] = value.to_dict()
                else:
                    data[key] = value

        return data        
