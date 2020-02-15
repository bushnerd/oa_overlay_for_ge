#!D:/Program Files (x86)/Python38-32/python.exe
# -*- coding: UTF-8 -*-

import cgi
# import cgitb
import logging

import ge_agent
import log
import oa_agent

# cgitb.enable()
logger = logging.getLogger("log.{module_name}".format(module_name=__name__))

form = cgi.FieldStorage()
bbox_url = form.getvalue('BBOX')
logger.info('BBOX url from Google Earth = {}'.format(bbox_url))

ge_agent.generate_kml(bbox_url)
