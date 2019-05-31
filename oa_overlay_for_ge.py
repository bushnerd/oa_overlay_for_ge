#!D:\Program Files\Python37\python.exe
# -*- coding: UTF-8 -*-

import cgi
import logging

import oa_agent

logger = logging.getLogger('oa_overlay_for_ge')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('oa_overlay_for_ge.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 
# url = cgi.FieldStorage()
# bbox = url['BBOX'].value
# bbox = bbox.split(',')
# west = float(bbox[0])
# south = float(bbox[1])
# east = float(bbox[2])
# north = float(bbox[3])

# postion_files = oa_agent.request_position_files(north,south, west, east)

postion_files = oa_agent.request_position_files()

files = postion_files['files']

kml = ( 
   '<?xml version="1.0" encoding="UTF-8"?>\n'
   '<kml xmlns="http://www.opengis.net/kml/2.2">\n')

for file in files:
    longtitude = file['longtitude']
    latitude = file['latitude']

    kml = (kml + '<Placemark>\n'
    + '<name>potionFile</name>\n'
    + '<Point>\n'
    + f'<coordinates>{longtitude},{latitude}</coordinates>\n'
    + '</Point>\n'
    + '</Placemark>\n' )

kml = kml + '</kml>'

print('Content-Type: application/vnd.google-earth.kml+xml\n')
print(kml)
