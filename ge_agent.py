#!D:\Program Files (x86)\Python38-32\python.exe
# -*- coding: UTF-8 -*-

' google_earth_pro_agent module for communicate with google earth pro '

__author__ = 'scutxd'

import logging
import os
import time

from lxml import etree

import log
import oa_agent

logger = logging.getLogger("log.{module_name}".format(module_name=__name__))

XML_FILE_PATH = os.path.dirname(__file__) + '/log/'
XML_FILE_NAME = 'kml.kml'
XML_FILE = XML_FILE_PATH + XML_FILE_NAME


def generate_track_positions_list_kml(track_id):
    track_positions_list = oa_agent.find_track_positions_list(track_id)

    kml = '''<Placemark>
        <styleUrl>#LineStringStyle</styleUrl>
        <LineString>
        <coordinates>'''
    for track_positions in track_positions_list:
        kml += '{},{} '.format(track_positions['lng'], track_positions['lat'])
    kml += '''</coordinates>
        </LineString>
    </Placemark>
    '''
    return kml


def generate_track_marker_list_kml(track_id):
    track_marker_list = oa_agent.get_track_marker_list(track_id)
    kml = ''
    for track_marker in track_marker_list:
        kml += '''
        <Placemark id="realPoint">
            <name>{text}</name>
            <description>
                <div>
                    <a href="" target="_blank">
                        <img style="height:360" src="{commnFileUrl}" />
                    </a>
                </div>
                <div>经度: {longtitude}</div>
                <div>纬度: {latitude}</div>
                <div>时间: {time}</div>
            </description>
            <Point>
                <coordinates>{co_longtitude},{co_latitude},0.0</coordinates>
            </Point>
        </Placemark>
        '''.format(text=track_marker['text'],
                   commnFileUrl=track_marker['commnFileUrl']
                   if 'commnFileUrl' in track_marker.keys() else '',
                   longtitude=track_marker['longitude'],
                   latitude=track_marker['latitude'],
                   time=time.strftime(
                       '%Y-%m-%d %H:%M:%S',
                       time.localtime(track_marker['createTime'] / 1000)),
                   co_longtitude=track_marker['longitude'],
                   co_latitude=track_marker['latitude'])
    return kml


def generate_around_track_kml(lat=0, lng=0, page_number=1, page_size=8):
    logger.info('lat={}, lng ={}, page_number={}, page_size={}'.format(
        lat, lng, page_number, page_size))
    kml = '<Folder>'
    track_id_list = oa_agent.find_around_track_list(lat, lng, page_number,
                                                    page_size)
    for track_id in track_id_list:
        kml += generate_track_positions_list_kml(track_id)
        kml += generate_track_marker_list_kml(track_id)

    kml += '</Folder>'
    return kml


def generate_position_files_kml(north, south, west, east):
    kml = '<Folder>'

    postion_files = oa_agent.request_position_files(north, south, west, east,
                                                    15)
    for file in postion_files:
        longtitude = file['longtitude']
        latitude = file['latitude']

        kml += '''
        <Placemark>
        <name></name>
        <Point>
        '''

        kml += '<coordinates>{},{},0</coordinates>'.format(
            longtitude, latitude)

        kml += '''
        </Point>
        </Placemark>
        '''
    kml += '</Folder>'
    return kml


def generate_kml(url):
    logger.debug('url = {}'.format(url))

    url = url.split(',')
    west = float(url[0])
    south = float(url[1])
    east = float(url[2])
    north = float(url[3])

    center_lng = ((east - west) / 2) + west
    center_lat = ((north - south) / 2) + south

    kml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
           '<Document>\n'
           '<name></name>\n')
    kml += '''<Style id="LineStringStyle">
            <LineStyle>
                <width>2</width>
                <color>990074FF</color>
            </LineStyle>
            </Style>'''

    kml += generate_around_track_kml(center_lat, center_lng, 1, 10)

    kml = kml + '</Document>\n</kml>'

    with open(XML_FILE, mode='w', encoding='utf-8') as kml_file:
        kml_file.write(kml)

    try:
        b_kml = bytes(bytearray(kml, encoding='utf-8'))
        etree.fromstring(b_kml)
    except etree.XMLSyntaxError as exception:
        # validation for kml failed, write the kml to a xml file to debug
        logging.critical(exception)
        with open(XML_FILE, mode='w', encoding='utf-8') as kml_file:
            kml_file.write(kml)
        return None
    else:
        return kml


if (__name__ == '__main__'):
    # pass
    generate_kml(
        '113.3181589196196, 30.97968899527223, 113.3384812250916, 30.99556779277229'
    )
