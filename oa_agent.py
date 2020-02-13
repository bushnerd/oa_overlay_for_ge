#!D:\Program Files (x86)\Python38-32\python.exe
# -*- coding: UTF-8 -*-

' oa_agent module for communicate with outdoor_assistant '

__author__ = 'scutxd'

import json
import logging

import requests

import log

logger = logging.getLogger("log.{module_name}".format(module_name=__name__))

FIND_AROUND_TRACK_LIST_URL = 'http://www.2bulu.com/track/find_around_track_list.htm'
FIND_TRACK_POSITIONS_LIST_URL = 'http://www.2bulu.com/track/find_track_positions_list.htm'
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
        'Referer':
        'http://www.2bulu.com/track/track_nearby_map.htm?lng=116.439606&lat=40.323242&remark=%E5%8C%97%E4%BA%AC%E5%B8%82-%E5%A4%A7%E7%BE%8A%E5%B1%B1',
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
    logger.debug('{}'.format(response.text))


def find_track_positions_list(track_Id=''):
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
        'pgv_pvid=8835094330; UM_distinctid=1700e0fb6fb23f-0841f4aa994d1e-47e1039-181db4-1700e0fb6fc94c; JSESSIONID=0D958763C840C4037891792E223B5949-n2; CNZZDATA1000341086=1941407547-1542934706-%7C1581405252',
        'DNT':
        '1',
        'Host':
        'www.2bulu.com',
        'Pragma':
        'no-cache',
        'Referer':
        'http://www.2bulu.com/track/track_nearby_map.htm?lng=116.439606&lat=40.323242&remark=%E5%8C%97%E4%BA%AC%E5%B8%82-%E5%A4%A7%E7%BE%8A%E5%B1%B1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    params = {'trackId': track_Id}
    response = requests.get(FIND_TRACK_POSITIONS_LIST_URL,
                            params=params,
                            headers=headers)
    if (response.status_code == 200):
        logger.debug('{}'.format(response.json()))
        track_positions_list = response.json()['trackPositions'][0]
        logger.info('{} track_positions found'.format(
            len(track_positions_list)))
        return track_positions_list


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
    if json['errCode'] is '0':
        logger.info('Get %d position files info', len(json['files']))
        return json['files']


if (__name__ == '__main__'):
    pass
    # find_around_track_list(40.32325381410464, 116.43962005594483, 1, 8)
    # find_track_positions_list('sDWvJaqS%25252BME%25253D')
