#!D:\Program Files\Python37\python.exe
# -*- coding: UTF-8 -*-

' oa_agent module for communicate with outdoor_assistant '

__author__ = 'scutxd'

import requests
import json

import logging

logger = logging.getLogger('oa_overlay_for_ge.oa_agent')

'''
GET
https://helper.2bulu.com/position/reqPositionFiles?authCode=8b2ac95bd33a4cafb539df2cd616e817&authType=1
&isMaxHierarchy=0
&latitudeLeftTop=28.50024550504075&latitudeRightBottom=28.9146476014468
&longtitudeLeftTop=115.2401327220437&longtitudeRightBottom=115.5141341097449
&mapHierarchy=11.91052055358887
&p_appVersion=6.3.6.2&p_productType=0&p_terminalType=3&p_userId=2134096&userId=2134096&version=1
'''
'''
HTTP/1.1
Host: helper.2bulu.com
Accept: */*
Cookie: token=GHk9y9OZl0o%3D; UM_distinctid=169eddabcd24d6-093d9d3fe58ccc-66542941-3d10d-169eddabcd3495
User-Agent: OutdoorAssistantApplication/6.3.6 (Model/iPhone10,1; Screen/375x667; iOS 12.1.1; Scale/2.00)
Accept-Language: zh-Hans-CN;q=1, en-CN;q=0.9
Accept-Encoding: br, gzip, deflate
Connection: keep-alive
'''

# authCode='8b2ac95bd33a4cafb539df2cd616e817'
# authType='1'
# isMaxHierarchy='0'
# p_appVersion='6.3.6.2'
# p_productType='0'
# p_terminalType='3'
# p_userId='0'
# version='1'

def request_position_files(latitudeLeftTop=0, latitudeRightBottom=0,
                           longtitudeLeftTop=0, longtitudeRightBottom=0, mapHierarchy=0):
    # 武汉市黄陂区姚家山
    # latitudeLeftTop = 31.23257211197333
    # latitudeRightBottom = 31.27027234988102
    # longtitudeLeftTop = 114.1778958951424
    # longtitudeRightBottom = 114.2035015071832
    # mapHierarchy = 15.33358669281006

    logger.info('latitudeLeftTop: %f, latitudeRightBottom: %f, longtitudeLeftTop: %f, longtitudeRightBottom: %f, mapHierarchy: %f', 
                latitudeLeftTop,
                latitudeRightBottom,
                longtitudeLeftTop,
                longtitudeRightBottom,
                mapHierarchy)

    # 这个dict后面可能要放到函数外面，作为全局变量
    headers = {
    'User-Agent': 'OutdoorAssistantApplication/6.3.6 (Model/iPhone10,1; Screen/375x667; iOS 12.1.1; Scale/2.00)',
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
        'p_userId': '0',#不需要登录也可以获取信息
        'version': '1'
    }

    params['latitudeLeftTop'] = str(latitudeLeftTop)
    params['latitudeRightBottom'] = str(latitudeRightBottom)
    params['longtitudeLeftTop'] = str(longtitudeLeftTop)
    params['longtitudeRightBottom'] = str(longtitudeRightBottom)
    params['mapHierarchy'] = str(mapHierarchy)

    response_postion_files = requests.get(
    'https://helper.2bulu.com/position/reqPositionFiles',
    params=params,
    headers=headers)

    logger.info('Get %d position files info', len(response_postion_files.json()['files']))

    return response_postion_files.json()

