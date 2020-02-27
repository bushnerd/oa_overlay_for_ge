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

MIN_TRACK_MARKS_NUM = 5
PAGE_SIZE = 30
PAGE_NUMBER = 1


def generate_track_positions_list_kml(track_id):
    track_positions_list = oa_agent.find_track_positions_list(track_id)

    kml = '''
            <Placemark>
                <styleUrl>#LineStringStyle</styleUrl>
                <LineString>
                    <coordinates>
        '''
    for track_positions in track_positions_list:
        kml += '{},{} '.format(track_positions['lng'], track_positions['lat'])

    kml += '''
                    </coordinates>
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
                <div>longtitude: {longtitude}</div>
                <div>latitude: {latitude}</div>
                <div>time: {time}</div>
            </description>
            <Point>
                <coordinates>{co_longtitude},{co_latitude},0.0</coordinates>
            </Point>
        </Placemark>
        '''.format(
            # TODO:名称如果为中文的话，在google earth显示乱码,先暂时都设为空
            # text=track_marker['text'] if track_marker['text'] else '',
            text='',
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
    kml = '''
        <Folder>
            <name>{},{}</name>
            <description>tracks and marks nearby</description>
            '''.format(lng, lat)

    track_list = oa_agent.find_around_track_list(lat, lng, page_number,
                                                 page_size)
    for track in track_list:
        kml += generate_track_positions_list_kml(track.id)
        if track.marks_num >= MIN_TRACK_MARKS_NUM:
            kml += generate_track_marker_list_kml(track.id)

    kml += '''
        </Folder>
        '''
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
    logger.info('url = {}'.format(url))

    url = url.split(',')
    west = float(url[0])
    south = float(url[1])
    east = float(url[2])
    north = float(url[3])

    center_lng = ((east - west) / 2) + west
    center_lat = ((north - south) / 2) + south

    kml = '''<?xml version="1.0" encoding="UTF-8" ?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <name></name>
        <Style id="LineStringStyle">
            <LineStyle>
                <width>2</width>
                <color>990074FF</color>
            </LineStyle>
        </Style>
    '''

    kml += generate_around_track_kml(center_lat, center_lng, PAGE_NUMBER,
                                     PAGE_SIZE)
    kml += '''
    </Document>
</kml>
    '''

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
