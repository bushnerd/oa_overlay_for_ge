#!/usr/bin/python

import cgi

url = cgi.FieldStorage()
bbox = url['BBOX'].value
bbox = bbox.split(',')
west = float(bbox[0])
south = float(bbox[1])
east = float(bbox[2])
north = float(bbox[3])

center_lng = ((east - west) / 2) + west
center_lat = ((north - south) / 2) + south

kml = ( 
   '<?xml version="1.0" encoding="UTF-8"?>\n'
   '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
   '<Placemark>\n'
   '<name>View-centered placemark</name>\n'
   '<Point>\n'
   '<coordinates>%.6f,%.6f</coordinates>\n'
   '</Point>\n'
   '</Placemark>\n'
   '</kml>'
   ) %(center_lng, center_lat)

print 'Content-Type: application/vnd.google-earth.kml+xml\n'
print kml