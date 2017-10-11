from smartbotsol import Cache
from smartbotsol import User
from smartbotsol.core.cache import _log

import logging
log = logging.getLogger(__name__)

import os, dill, sys
import errno
from smartbotsol.core.cache import _log
from tinydb import TinyDB, where, Query
import pickle

class TinyCache(Cache):
    """Users cache store based on dictonary"""

    _cache = None
    
    def __str__(self):
        return str(self._cache.all())
    

    def __init__(self, from_dict=None, db_filename='bot_tiny_db.json'):
        self._cache = TinyDB(db_filename)


    @_log
    def get(self, uid):
        # {'uid':'key', 'state':'pickled state'}
        q = Query()
        result = self._cache.get(q.uid == uid)
        user = User(uid)
        if result:
            user.state = result['state']
        else:
            self._cache.insert(
                {
                    'uid': uid,
                    'state': None
                }
            )
        return user

    def set(self, uid, state):
        user = Query()
        result = self._cache.get(user.uid == uid)
        row = dict()
        pickled_state = pickle.dumps(state)
        if result:
            doc_id = result.doc_id
            row['state'] = pickled_state
            self._cache.update(row, doc_ids = [doc_id])
        # else:
        #     row['uid'] = uid
        #     row['state'] = pickled_state
        #     self._cache.insert(row)
            

    def add(self, key, value):
        pass

    def to_dict(self):
        return self._cache

    @classmethod
    def from_dict(cls, fdict):
        pass

