# -*- coding: UTF-8 -*-

__author__ = 'scutxd'
import oa_agent
import unittest


class TestOAAgent(unittest.TestCase):
    def test_find_around_track_list(self):
        self.assertEqual(
            len(
                oa_agent.find_around_track_list(40.32325381410464,
                                                116.43962005594483, 1, 15)),
            15)

    def test_find_track_positions_list(self):
        self.assertEqual(
            len(oa_agent.find_track_positions_list('5yhrp%252F88gr0%253D')),
            100)

    def test_get_track_marker_list(self):
        #还没有写好
        self.assertEqual(
            len(oa_agent.get_track_marker_list('156g%25252BsXGkoI%25253D')),
            29)

    def test_request_position_files(self):
        self.assertEqual(
            len(
                oa_agent.request_position_files(31.23257211197333,
                                                31.27027234988102,
                                                114.1778958951424,
                                                114.2035015071832,
                                                15.33358669281006)), 29)


if (__name__ == 'main'):
    unittest.main()
