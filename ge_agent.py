#!/usr/bin/env python3
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
MAX_TRACK_DISTANCE = 100
PAGE_SIZE = 30
PAGE_NUMBER = 1


def generate_track_positions_list_kml(track):
    track_positions_list = oa_agent.find_track_positions_list(track.id)

    kml = '''
            <Placemark>
                <name>Distance:{distance}Km</name>
                <visibility>1</visibility>            <!-- boolean -->
                <open>0</open>                        <!-- boolean -->
                <styleUrl>#TrackStyle</styleUrl>
                <LineString>
                    <coordinates>
        '''.format(distance=track.distance)
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
        if 'commnFileUrl' in track_marker.keys():
            # kml += '''
            # <Style id="{style_id_lng},{style_id_lat}">
            #     <IconStyle>
            #         <scale>2</scale>
            #         <Icon>
            #             <href>{icon_url}</href>
            #         </Icon>
            #         <hotSpot x="0.5" y="0.5" xunits="pixels" yunits="fraction" />
            #     </IconStyle>
            #     <LineStyle>
            #         <color>8000aaff</color>
            #         <width>3</width>
            #     </LineStyle>
            # </Style>
            # <Placemark id="realPoint">
            #     <visibility>0</visibility>            <!-- boolean -->
            #     <styleUrl>#{style_url_lng},{style_url_lat}</styleUrl>
            #     <name>{name}</name>
            #     <description><![CDATA[
            #         <img style="height:360" src="{commnFileUrl}"/><br>
            #         {time}]]>
            #     </description>
            #     <Point>
            #         <extrude>1</extrude>
            #         <altitudeMode>relativeToGround</altitudeMode>
            #         <coordinates>{co_longtitude},{co_latitude},30</coordinates>
            #     </Point>
            # </Placemark>
            # TODO:google kml中提供<gx:balloonVisibility>来实现遍历mark，依次打开，但是需要创建<gx:Tour>，构造需要做两次遍历
            # google earth有个选项，Touring->When creating a tour from a folder->Show ballon when waiting at features，但是不奏效
            kml += '''
            <Placemark id="realPoint">
                <visibility>0</visibility>            <!-- boolean -->
                <name>{name}</name>
                <description><![CDATA[
                    <a href="{commnFileUrl}">
                    <img src="{bigUrl}"/><br>
                    </a>
                    {time}]]>
                </description>
                <Point>
                    <extrude>1</extrude>
                    <altitudeMode>relativeToGround</altitudeMode>
                    <coordinates>{co_longtitude},{co_latitude},30</coordinates>
                </Point>
            </Placemark>
            '''.format(
                # TODO:如果用图片直接作为图标的话，造成太多请求，导致图片无法访问
                # style_id_lng=track_marker['longitude'],
                # style_id_lat=track_marker['latitude'],
                # icon_url=track_marker['centerUrl'],
                # style_url_lng=track_marker['longitude'],
                # style_url_lat=track_marker['latitude'],
                name=track_marker['text'] if track_marker['text'] else '',
                commnFileUrl=track_marker['commnFileUrl'],
                # 图片大小依次递增：
                # centerUrl:
                # bigUrl
                # commnFileUrl
                bigUrl=track_marker['centerUrl'],
                time=time.strftime(
                    'Time: %Y-%m-%d %H:%M:%S',
                    time.localtime(track_marker['createTime'] / 1000))
                if track_marker['createTime'] else '',
                co_longtitude=track_marker['longitude'],
                co_latitude=track_marker['latitude'])
    return kml


def generate_around_track_kml(lat=0, lng=0, page_number=1, page_size=8):
    logger.info('lat={}, lng ={}, page_number={}, page_size={}'.format(
        lat, lng, page_number, page_size))
    kml = ''

    track_list = oa_agent.find_around_track_list(lat, lng, page_number,
                                                 page_size)
    for track in track_list:
        if track.marks_num >= MIN_TRACK_MARKS_NUM and track.distance <= MAX_TRACK_DISTANCE:
            kml += '''
                <Folder>
                    <name>{track_title}</name>
                    <visibility>1</visibility>            <!-- boolean -->
                    <open>0</open>                        <!-- boolean -->
                    '''.format(track_title=track.title)
            kml += generate_track_positions_list_kml(track)
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

    center_lng = float(url[0])
    center_lat = float(url[1])

    kml = '''<?xml version="1.0" encoding="utf-8" ?>
    <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/atom">
    <Document>
        <name></name>
        <Style id="TrackStyle_n">
            <LineStyle>
                <color>880000cc</color>
                <colorMode>random</colorMode> <!-- kml:colorModeEnum: normal or random -->
                <width>2</width>
            </LineStyle>
        </Style>
        <Style id="TrackStyle_h">
            <LineStyle>
                <color>ff0000cc</color>
                <colorMode>random</colorMode> <!-- kml:colorModeEnum: normal or random -->
                <width>3</width>
            </LineStyle>
        </Style>
        <StyleMap id="TrackStyle">
            <Pair>
                <key>normal</key>
                <styleUrl>#TrackStyle_n</styleUrl>
            </Pair>
            <Pair>
                <key>highlight</key>
                <styleUrl>#TrackStyle_h</styleUrl>
            </Pair>
        </StyleMap>
        <Style id="MarkStyle">
            <IconStyle>
                <scale>1</scale>
                <Icon>
                    <href>grn-blank.png</href>
                </Icon>
                <hotSpot x="0.5" y="0.5" xunits="pixels" yunits="fraction" />
            </IconStyle>
        </Style>
    '''

    kml += generate_around_track_kml(center_lat, center_lng, PAGE_NUMBER,
                                     PAGE_SIZE)
    kml += '''
    </Document>
</kml>
    '''

    # with open(XML_FILE, mode='w', encoding='utf-8') as kml_file:
    #     kml_file.write(kml)

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
    # generate_track_marker_list_kml('6B5KR8eFZE8%253D')
    generate_kml(
        '113.3181589196196, 30.97968899527223, 113.3384812250916, 30.99556779277229'
    )
