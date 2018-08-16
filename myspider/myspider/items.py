# -*- coding: utf-8 -*-

import scrapy

class HangbanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    flight = scrapy.Field()
    planeType = scrapy.Field()
    date = scrapy.Field()
    offTime = scrapy.Field()
    landTime = scrapy.Field()
    homeIcao = scrapy.Field()
    pointIcao = scrapy.Field()
    time = scrapy.Field()
    dateHref = scrapy.Field()

class MyspiderItem(scrapy.Item):
    selfUrl = scrapy.Field()
    # 本页面url，必须抓取
    airline = scrapy.Field()  # 航空公司

    homeName = scrapy.Field()  # 始发地城市名
    homeAirport = scrapy.Field()  # 始发地机场
    pointName = scrapy.Field()  # 目的地城市名
    pointAirport = scrapy.Field()  # 目的地机场

    planOffTime = scrapy.Field()  # 计划起飞时间
    actOffTime = scrapy.Field()  # 实际起飞时间
    planGateOffTime = scrapy.Field()  # 计划离开停机坪时间
    # 实际离开停机位时间在历史记录页已经抓取完毕

    planLandTime = scrapy.Field()  # 计划降落时间
    planGateLandTime = scrapy.Field()  # 计划抵达停机坪时间
    actLandTime = scrapy.Field()  # 实际降落时间

class ZbItem(scrapy.Item):
    jd=scrapy.Field()
    wd=scrapy.Field()
    icao=scrapy.Field()