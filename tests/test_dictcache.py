#!/usr/bin/env python


"""Tests for `DictCache."""


import unittest

from smartbotsol import DictCache, User



class TestSmartbotsol(unittest.TestCase):
    """Tests for `smartbotsol` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.dump_path = './backups'
        self.user_uids = [111,222,333]
        self.dict_cache = { x: User(x) for x in self.user_uids }

    def tearDown(self):
        """Tear down test fixtures, if any."""


    def test_get_user(self):
        """Test something."""
        cache = DictCache()
        for u in self.user_uids:
            cache.get(u)
        self.assertTrue(isinstance(cache.to_dict(), dict))
        self.assertDictEqual(cache.to_dict(), self.dict_cache)
