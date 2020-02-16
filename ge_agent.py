#!D:\Program Files (x86)\Python38-32\python.exe
# -*- coding: UTF-8 -*-

' google_earth_pro_agent module for communicate with google earth pro '

__author__ = 'scutxd'

import logging

import log
import oa_agent

logger = logging.getLogger("log.{module_name}".format(module_name=__name__))


def generate_kml(url):
    logger.debug('url = {}'.format(url))

    url = url.split(',')
    west = float(url[0])
    south = float(url[1])
    east = float(url[2])
    north = float(url[3])

    postion_files = oa_agent.request_position_files(north, south, west, east,
                                                    15)

    kml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
           '<Document>\n'
           '<name>position files</name>')

    for file in postion_files:
        longtitude = file['longtitude']
        latitude = file['latitude']

        kml = (kml + '<Placemark>\n' + '<name></name>\n' + '<Point>\n' +
               f'<coordinates>{longtitude},{latitude},0</coordinates>\n' +
               '</Point>\n' + '</Placemark>\n')

    kml = kml + '</Document>\n</kml>'

    logger.info(kml)
    return kml


if (__name__ == '__main__'):
    # pass
    generate_kml(
        '113.3181589196196, 30.97968899527223, 113.3384812250916, 30.99556779277229'
    )
