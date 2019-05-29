#!D:\Program Files\Python37\python.exe
# -*- coding: UTF-8 -*-

import cgi
import oa_agent

# url = cgi.FieldStorage()
# bbox = url['BBOX'].value
# bbox = bbox.split(',')
# west = float(bbox[0])
# south = float(bbox[1])
# east = float(bbox[2])
# north = float(bbox[3])

# postion_files = oa_agent.request_position_files(north,south, west, east)

postion_files = oa_agent.request_position_files(0,0, 0, 0)

files = postion_files['files']

kml = ( 
   '<?xml version="1.0" encoding="UTF-8"?>\n'
   '<kml xmlns="http://www.opengis.net/kml/2.2">\n')

for file in files:
    kml = (kml + '<Placemark>\n'
    + '<name>potionFile</name>\n'
    + '<Point>\n'
    + '<coordinates>%.6f,%.6f</coordinates>\n' %(file['longtitude'], file['latitude'])
    + '</Point>\n'
    + '</Placemark>\n' )

kml = kml + '</kml>'

print('Content-Type: application/vnd.google-earth.kml+xml\n')
print(kml)
