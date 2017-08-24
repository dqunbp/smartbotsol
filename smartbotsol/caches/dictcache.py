from smartbotsol import Cache
from smartbotsol import User

import os, dill, sys
import errno
import logging as logger
log = logger.getLogger(__name__)

class DictCache(Cache):
    """Users cache store based on dictonary"""

    _cache = {}
    FILE_NAME = 'bot.pkl'
    BACKUP_DIR_PATH = '~/states_backup'

    def get(self, uid):
        user = self._cache.get(uid)

        if not user:
            user = User(uid)
            self._cache[uid] = user

        return self._cache.get(uid)

    def add(self, key, value):
        assert isinstance(value, User)
        self._cache[key] = value

    def to_dict(self):
        return self._cache

    def from_dict(self, fdict):
        assert isinstance(fdict, dict)
        for k,v in fdict.iteritems():
            if isinstance(v, User):
                self._cache.setdefault(k,v)
            else:
                log.warn('User with id %s, is %s instance, it must be User instance, skip...' % (k, v.__class__.__name__))

    def save(self):
        """Save users cache to file"""
        path = os.path.join(DictCache.BACKUP_DIR_PATH, DictCache.FILE_NAME)
        if not os.path.exists(path):
            os.makedirs(path)

        with open(path, 'wb') as f:
            dill.dump(len(self._cache.keys()), f)
            for user_key in self._cache.keys():
                dill.dump(self._cache[user_key], f)
            log.debug('All states saved to {}.'.format(path))

    def load(self):
        """Loads users cache from file"""
        path = os.path.join(DictCache.BACKUP_DIR_PATH, DictCache.FILE_NAME)
        try:
            with open(path, 'rb') as f:
                log.debug(str(self._cache))
                for i in range(dill.load(f)):
                    user = dill.load(f)
                    self._cache[user.uid] = user
                log.debug('All states have been loaded from {}.'.format(path))
                log.debug(str(self._cache))
        except OSError as e:
            log.debug('User_states file isn`t exist! {}'.format(e))