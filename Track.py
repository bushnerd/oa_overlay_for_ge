#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

' Class Track '

__author__ = 'scutxd'


class Track:
    def __init__(self,
                 id='',
                 title='',
                 distance=0,
                 marks_num=0,
                 positions_list=[],
                 marks_list=[]):
        self.id = id
        self.title = title
        self.distance = distance
        self.marks_num = marks_num
        self.positions_list = positions_list
        self.marks_list = marks_list
