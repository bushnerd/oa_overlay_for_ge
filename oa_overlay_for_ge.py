#!python
# -*- coding: UTF-8 -*-

import cgi
# import cgitb
# cgitb.enable()
import codecs
import logging
import sys

import ge_agent
import log
import oa_agent

logger = logging.getLogger("log.{module_name}".format(module_name=__name__))

form = cgi.FieldStorage()
bbox_url = form.getvalue('BBOX')
logger.warning('BBOX url from Google Earth = {}'.format(bbox_url))

kml = ge_agent.generate_kml(bbox_url)
if kml:
    # print到cgi时，会按照操作系统的默认编码，导致乱码，这里强制stdout修改为utf-8
    sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
    print('Content-Type: text/plain; charset=utf-8\n')
    print(kml)
