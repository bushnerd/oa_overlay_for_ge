# -*- coding: UTF-8 -*-

__author__ = 'scutxd'
import oa_agent
import unittest


class TestOAAgent(unittest.TestCase):
    def test_find_around_track_list(self):
        oa_agent.find_around_track_list(40.32325381410464, 116.43962005594483,
                                        1, 8)

    def test_find_track_positions_list(self):
        oa_agent.find_track_positions_list('5yhrp%252F88gr0%253D')


if (__name__ == 'main'):
    unittest.main()
