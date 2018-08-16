# -*- coding: utf-8 -*-
# __author__ = "吴道子mr.worth@qq.com"
# coding=utf-8
import pymysql

import scrapy
from myspider.items import ZbItem

headers2={"Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
	"Cache-Control": "max-age=0",
	"Connection": "keep-alive",
	"DNT": "1",
	"Host": "zh.flightaware.com",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0"
	}

class ZbSpider(scrapy.Spider):
	name = 'zb'
	allowed_domains = ['www.flightaware.com']
	start_urls = []

	# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') 如遇编码问题可尝试开启此句
	def start_requests(self):
		# 由于部分机场坐标在openflight.rog里没有提供, 而flightaware里有, 故进行查漏补缺, 尽可能补全坐标信息
		conn = pymysql.connect(host="", port=3306, user="", passwd="", db="flight",
							   charset="utf8")
		cur = conn.cursor()
		sql_select_all_null_icao = "select icao from test_icao WHERE name=''"
		cur.execute(sql_select_all_null_icao)
		print("坐标抓取启动中"*3)
		rows = cur.fetchall()
		flightUrlList = []
		for dr in rows:
			if dr[0]:
				url = "https://flightaware.com/resources/airport/{}/summary".format(dr[0])
				flightUrlList.append(url)
			else:
				pass
		cur.close()
		for url in flightUrlList:
			yield self.make_requests_from_url(url)

	def parse(self, response):

		# 纬度
		jd="unknown"
		# 经度
		wd="unknown"
		icao=""
		try:
			wd = response.xpath("//table[contains(@class,'prettyTable')][1]//tr[1]/td[4]/text()").extract_first()
			jd = response.xpath("//table[contains(@class,'prettyTable')][1]//tr[1]/td[4]/text()").extract()[1]
			
			icao=response.xpath('//meta[13]/@content').extract_first()[41:-8]
		except:
			print("something went wrong"*3)

		item = ZbItem()
		item['jd'] = jd
		item['wd'] = wd
		item['icao']=icao
		yield item
