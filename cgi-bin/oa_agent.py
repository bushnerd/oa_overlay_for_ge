#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

' oa_agent module for communicate with outdoor_assistant '

__author__ = 'scutxd'

import json
import logging
import re

import requests
from lxml import etree

import log
from Track import Track

logger = logging.getLogger("log.{module_name}".format(module_name=__name__))

FIND_AROUND_TRACK_LIST_URL = 'http://www.2bulu.com/track/find_around_track_list.htm'
FIND_TRACK_POSITIONS_LIST_URL = 'http://www.2bulu.com/track/find_track_positions_list.htm'

GET_TRACK_POSITIONS_LIST_URL = 'http://www.2bulu.com/track/get_track_positions_list4.htm'
GET_TRACK_MARKER_LIST_URL = 'http://www.2bulu.com/track/get_track_marker_list_2.htm'

REQUEST_POSITIONS_FILES_URL = 'https://helper.2bulu.com/position/reqPositionFiles'


def find_around_track_list(lat=0, lng=0, page_number=1, page_size=8):
    logger.info('lat={}, lng ={}, page_number={}, page_size={}'.format(
        lat, lng, page_number, page_size))
    headers = {
        'Accept':
        '*/*',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Cache-Control':
        'no-cache',
        'Connection':
        'keep-alive',
        'Cookie':
        'pgv_pvid=8835094330; UM_distinctid=1700e0fb6fb23f-0841f4aa994d1e-47e1039-181db4-1700e0fb6fc94c; JSESSIONID=0D958763C840C4037891792E223B5949-n2; CNZZDATA1000341086=1941407547-1542934706-%7C1581405252',
        'DNT':
        '1',
        'Host':
        'www.2bulu.com',
        'Pragma':
        'no-cache',
        # 'Referer':
        # 'http://www.2bulu.com/track/track_nearby_map.htm?lng=116.439606&lat=40.323242&remark=%E5%8C%97%E4%BA%AC%E5%B8%82-%E5%A4%A7%E7%BE%8A%E5%B1%B1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    params = {
        'lat': str(lat),
        'lng': str(lng),
        'pageNumber': str(page_number),
        'pageSize': str(page_size)
    }
    response = requests.get(FIND_AROUND_TRACK_LIST_URL,
                            params=params,
                            headers=headers)

    html_content = etree.HTML(response.text)
    li_id_list = html_content.xpath('//ul/li/input/@value')
    title_list = html_content.xpath(
        '//ul/li/div[@class=\'list_left\']/p/@title')
    span_km_list = html_content.xpath(
        '//ul/li/div[@class=\'list_left\']/span[@class=\'km\']')
    span_num_list = html_content.xpath(
        '//ul/li/div[@class=\'list_left\']/span[@class=\'num\']')

    track_list = []
    if (len(li_id_list) == len(span_km_list)
            and len(li_id_list) == len(span_num_list)
            and len(li_id_list) == len(title_list)):
        for li_id, title, km, num in zip(li_id_list, title_list, span_km_list,
                                         span_num_list):
            # km.text maybe 4km, 0.4km, 4.4km
            km_pattern = re.compile(r'(\d*.*\d+)km')
            distance = float(km_pattern.search(km.text).group(1))
            track_list.append(Track(li_id, str(title), distance,
                                    int(num.text)))

    return track_list


def find_track_positions_list(track):
    logger.info('trackId={}'.format(track.id))
    headers = {
        'Accept':
        '*/*',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Cache-Control':
        'no-cache',
        'Connection':
        'keep-alive',
        'Cookie':
        'pgv_pvid=8835094330; UM_distinctid=1700e0fb6fb23f-0841f4aa994d1e-47e1039-181db4-1700e0fb6fc94c; JSESSIONID=0D958763C840C4037891792E223B5949-n2; CNZZDATA1000341086=1941407547-1542934706-%7C1581405252',
        'DNT':
        '1',
        'Host':
        'www.2bulu.com',
        'Pragma':
        'no-cache',
        # 'Referer':
        # 'http://www.2bulu.com/track/track_nearby_map.htm?lng=116.439606&lat=40.323242&remark=%E5%8C%97%E4%BA%AC%E5%B8%82-%E5%A4%A7%E7%BE%8A%E5%B1%B1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    # https://stackoverflow.com/questions/23496750/how-to-prevent-python-requests-from-percent-encoding-my-urls/23497912
    # If the params is dict, requests lib encodes url(Such as '%' to '%25')
    # So i change the params to string
    params = '&trackId={}'.format(track.id)
    response = requests.get(FIND_TRACK_POSITIONS_LIST_URL,
                            params=params,
                            headers=headers)
    if (response.status_code == 200):
        logger.debug('{}'.format(response.json()))
        track_positions_list = response.json()['trackPositions'][0]
        logger.info('{} track_positions found'.format(
            len(track_positions_list)))
        track.track_positions_list = track_positions_list


def get_track_positions_list(track_Id=''):
    logger.info('trackId={}'.format(track_Id))
    headers = {
        'Accept':
        '*/*',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Cache-Control':
        'no-cache',
        'Connection':
        'keep-alive',
        'Cookie':
        'pgv_pvid=8835094330; UM_distinctid=1700e0fb6fb23f-0841f4aa994d1e-47e1039-181db4-1700e0fb6fc94c; JSESSIONID=437B1CA9024515AE952DBC0FC564BC2B-n2; CNZZDATA1000341086=1941407547-1542934706-%7C1581947357',
        'DNT':
        '1',
        'Host':
        'www.2bulu.com',
        'Pragma':
        'no-cache',
        # 'Referer':
        # 'http://www.2bulu.com/track/t-6B5KR8eFZE8%253D.htm',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    params = {'trackId': track_Id}
    response = requests.get(GET_TRACK_POSITIONS_LIST_URL,
                            params=params,
                            headers=headers)
    if (response.status_code == 200):
        track_positions_list = response.json()['trackPositions'][0]
        logger.debug('{}'.format(track_positions_list))
        logger.info('{} track_positions found'.format(
            len(track_positions_list)))
        return track_positions_list


def get_track_marker_list(track):
    logger.info('trackId={}'.format(track.id))
    headers = {
        'Accept':
        '*/*',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Cache-Control':
        'no-cache',
        'Connection':
        'keep-alive',
        'Cookie':
        'pgv_pvid=8835094330; UM_distinctid=1700e0fb6fb23f-0841f4aa994d1e-47e1039-181db4-1700e0fb6fc94c; JSESSIONID=437B1CA9024515AE952DBC0FC564BC2B-n2; CNZZDATA1000341086=1941407547-1542934706-%7C1581947357',
        'DNT':
        '1',
        'Host':
        'www.2bulu.com',
        'Pragma':
        'no-cache',
        # 'Referer':
        # 'http://www.2bulu.com/track/t-6B5KR8eFZE8%253D.htm',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    params = '&trackId={}'.format(track.id)
    response = requests.get(GET_TRACK_MARKER_LIST_URL,
                            params=params,
                            headers=headers)
    if (response.status_code == 200):
        track_marker_list = response.json()
        logger.debug('{}'.format(track_marker_list))
        logger.info('{} track_marker found'.format(len(track_marker_list)))
        track.track_marker_list = track_marker_list


# mapHierarchy不确定这个参数是否有用，还有一个isMaxHierarchy，可能是缩放层级大于多少才请求图片，要不然请求了也显示不完全
def request_position_files(latitudeLeftTop=0,
                           latitudeRightBottom=0,
                           longtitudeLeftTop=0,
                           longtitudeRightBottom=0,
                           mapHierarchy=0):
    # GET
    # https://helper.2bulu.com/position/reqPositionFiles?authCode=8b2ac95bd33a4cafb539df2cd616e817&authType=1
    # &isMaxHierarchy=0
    # &latitudeLeftTop=28.50024550504075&latitudeRightBottom=28.9146476014468
    # &longtitudeLeftTop=115.2401327220437&longtitudeRightBottom=115.5141341097449
    # &mapHierarchy=11.91052055358887
    # &p_appVersion=6.3.6.2&p_productType=0&p_terminalType=3&p_userId=2134096&userId=2134096&version=1

    # HTTP/1.1
    # Host: helper.2bulu.com
    # Accept: */*
    # Cookie: token=GHk9y9OZl0o%3D; UM_distinctid=169eddabcd24d6-093d9d3fe58ccc-66542941-3d10d-169eddabcd3495
    # User-Agent: OutdoorAssistantApplication/6.3.6 (Model/iPhone10,1; Screen/375x667; iOS 12.1.1; Scale/2.00)
    # Accept-Language: zh-Hans-CN;q=1, en-CN;q=0.9
    # Accept-Encoding: br, gzip, deflate
    # Connection: keep-alive

    # authCode='8b2ac95bd33a4cafb539df2cd616e817'
    # authType='1'
    # isMaxHierarchy='0'
    # p_appVersion='6.3.6.2'
    # p_productType='0'
    # p_terminalType='3'
    # p_userId='0'
    # version='1'
    # 武汉市黄陂区姚家山
    # latitudeLeftTop = 31.23257211197333
    # latitudeRightBottom = 31.27027234988102
    # longtitudeLeftTop = 114.1778958951424
    # longtitudeRightBottom = 114.2035015071832
    # mapHierarchy = 15.33358669281006

    logger.info(
        'latitudeLeftTop: %f, latitudeRightBottom: %f, longtitudeLeftTop: %f, longtitudeRightBottom: %f, mapHierarchy: %f',
        latitudeLeftTop, latitudeRightBottom, longtitudeLeftTop,
        longtitudeRightBottom, mapHierarchy)

    # 这个dict后面可能要放到函数外面，作为全局变量
    headers = {
        'User-Agent':
        'OutdoorAssistantApplication/6.3.6 (Model/iPhone10,1; Screen/375x667; iOS 12.1.1; Scale/2.00)',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        'Accept-Encoding': 'br, gzip, deflate',
        'Connection': 'keep-alive'
    }

    params = {
        'authCode': 'e11e5203351c489ba1dedc5cbb817a24',
        'authType': '1',
        'isMaxHierarchy': '0',
        'latitudeLeftTop': '',
        'latitudeRightBottom': '',
        'longtitudeLeftTop': '',
        'longtitudeRightBottom': '',
        'mapHierarchy': '',
        'p_appVersion': '6.3.6.2',
        'p_productType': '0',
        'p_terminalType': '3',
        'p_userId': '0',  #不需要登录也可以获取信息
        'version': '1'
    }

    params['latitudeLeftTop'] = str(latitudeLeftTop)
    params['latitudeRightBottom'] = str(latitudeRightBottom)
    params['longtitudeLeftTop'] = str(longtitudeLeftTop)
    params['longtitudeRightBottom'] = str(longtitudeRightBottom)
    params['mapHierarchy'] = str(mapHierarchy)

    response_postion_files = requests.get(REQUEST_POSITIONS_FILES_URL,
                                          params=params,
                                          headers=headers)
    json = response_postion_files.json()
    if json['errCode'] == '0':
        logger.info('Get %d position files info', len(json['files']))
        return json['files']


if (__name__ == '__main__'):
    # find_around_track_list(40.32325381410464, 116.43962005594483, 1, 8)
    # find_track_positions_list('sDWvJaqS%25252BME%25253D')
    # find_around_track_list(40.32325381410464, 116.43962005594483, 1, 100)
    # get_track_marker_list('6B5KR8eFZE8%253D')
    # get_track_positions_list('6B5KR8eFZE8%253D')
    pass
