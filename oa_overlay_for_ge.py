#!D:\Program Files\Python37\python.exe
# -*- coding: UTF-8 -*-

import cgi
import logging

import oa_agent

logger = logging.getLogger('logger') 

url = cgi.FieldStorage()
bbox = url['BBOX'].value

bbox = bbox.split(',')
west = float(bbox[0])
south = float(bbox[1])
east = float(bbox[2])
north = float(bbox[3])

postion_files = oa_agent.request_position_files(north, south, west, east, 15)

files = postion_files['files']

kml = ( 
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    '<Document>\n'
    '<name>position files</name>')

for file in files:
    longtitude = file['longtitude']
    latitude = file['latitude']

    kml = (kml + '<Placemark>\n'
    + '<name></name>\n'
    + '<Point>\n'
    + f'<coordinates>{longtitude},{latitude},0</coordinates>\n'
    + '</Point>\n'
    + '</Placemark>\n' )

kml = kml + '</Document>\n</kml>'

print('Content-Type: application/vnd.google-earth.kml+xml\n')
# logger.debug(kml)
print(kml)
