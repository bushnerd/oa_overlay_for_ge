# -*- coding: UTF-8 -*-

__author__ = 'scutxd'
import unittest

import ge_agent


class TestGEAgent(unittest.TestCase):
    def test_generate_kml(self):
        RESULT_KML = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<name></name>
<Folder>
        <Placemark>
        <name></name>
        <Point>
        <coordinates>113.329384,30.986006,0</coordinates>
        </Point>
        </Placemark>
        </Folder></Document>
</kml>'''
        self.assertEqual(
            RESULT_KML,
            ge_agent.generate_kml(
                '113.3181589196196, 30.97968899527223, 113.3384812250916, 30.99556779277229'
            ))
        # self.assertLogs()


if (__name__ == 'main'):
    unittest.main()
