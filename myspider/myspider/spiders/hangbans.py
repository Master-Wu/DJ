# -*- coding: utf-8 -*-
# __author__ = "吴道子mr.worth@qq.com"
# coding=utf-8
import pymysql
import scrapy

from myspider.items import HangbanItem

# 需要传入的header信息
headers2={"Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
	"Cache-Control": "max-age=0",
	"Connection": "keep-alive",
	"DNT": "1",
	"Host": "zh.flightaware.com",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0"
	}
# 需要传入的cookie信息, 如此条cookie无法使用, 可以创建一个flightaware.com账号,
# 在浏览器端登录后复制相应cookie按此格式粘贴到此处
# 本条cookie最近一次更新: 2018/7/22
cookies2 = {
'_ga':'GA1.2.2108668497.1526196590',
'__gads':'ID=135813048302ac86:T=1526196594:S=ALNI_MZEc2MARDYohp6vd-OqWaiPX50-PQ',
'__qca':'P0-1231556144-1526196627396',
'_gid':'GA1.2.1555899607.1532230904',
'w_sid':'ad7af8b0cd7e64b7a1d7d183b06f45102f10fd8368aaedfdf6af690031f14f33',
'update_time':'1532232244',
'__rtgt_sid':'jjwbju4sx6s0r9',
'd7s_uid':'jh4i1mtt3azybx',
'd7s_spc':'4'
}
class HangbansSpider(scrapy.Spider):
	name = 'hangbans'
	allowed_domains = ['flightaware.com']
	start_urls = []

	def start_requests(self):
		conn = pymysql.connect(host="", port=3306, user="", passwd="", db="flight",
							   charset="utf8")
		cur = conn.cursor()
		sql_select_all_plane = "select flightid from test_flightnum"
		cur.execute(sql_select_all_plane)
		rows = cur.fetchall()
		flightUrlList = []
		for dr in rows:
			if dr[0]:
				url2 = "https://flightaware.com/live/flight/{}/history/9999".format(dr[0])  # 加 /9999，登陆后可查询约四个月的数据
				flightUrlList.append(url2)
			else:
				pass
		for url in flightUrlList:
			yield scrapy.Request(url,cookies=cookies2)

	def parse(self, response):

		flight="unknown"
		date="unknown"
		datehref="unknown"
		planetype="unknown"
		offtime="unknown"
		landtime="unknown"
		homeicao="unknown"
		pointicao="unknown"
		time="unknown"
		try:
			flight = response.xpath("//td[@align='right']//input/@value").extract_first()
			if flight:
				pass
			else:
				flight = "unknown"
		except:
			flight = "unknown either"
		# print("开始新的一页，页码：：：：：：：：：：：：：：：：：：：：：：：：：：：：：：",self.i)
		for line in response.selector.xpath("//tr[contains(@class,'rowClickTarget')]"):
			# 日期
			try:
				date = str(line.xpath('.//td[@class="nowrap"]//a/text()').extract_first()).replace(" ","")
			except:
				date="unknown"
			# 航班某日详情超链接可用来抓取延误信息，航空公司中文等信息
			try:
				datehref = "https://flightaware.com" + str(line.xpath('.//td[@class="nowrap"]//a/@href').extract_first()).replace(" ","")
			except:
				datehref="unknown"
			# 机型
			try:
				planetypel = line.xpath(".//td[2]//i/text()").extract_first()
				if planetypel:
					pass
				else:
					planetypel = line.xpath(".//td[2]/text()").extract_first()
					if planetypel:
						pass
					else:
						planetypel="unknown"
				planetype = planetypel
			except:
				planetype = "unknown"
			# 始发地icao
			try:
				homeicaol = line.xpath(".//td[3]//a/text()").extract_first()
				homeicao = homeicaol[-4:]
			except:
				homeicao="unknown"
			# 目的地icao
			try:
				pointicaol = line.xpath(".//td[4]//a/text()").extract_first()
				pointicao = pointicaol[-4:]
			except:
				pointicao="unknown"
			# 起飞时间
			try:
				offtime = line.xpath(".//td[5]//em/text()").extract()
				if offtime:
					offtime = offtime[0][0:5]
				else:
					offtime = line.xpath(".//td[5]/text()").extract_first()[0:5]
			except:
				offtime="unknown"
			# 降落时间
			try:
				landtime = line.xpath(".//td[6]//em/text()").extract()
				if landtime:
					landtime = landtime[0][0:5]
				else:
					landtimel=line.xpath(".//td[6]/text()").extract_first()
					if landtimel:
						landtime = landtimel[0:5].strip()
					else:
						landtimel=line.xpath(".//td[6]//i/text()").extract_first()
						# 运行此步有时因网站无信息且标签H5异常而报错无法提取
						landtime = landtimel[0:5].strip() # 遂为全部提取项添加try catch语句
						if landtime:
							pass
						else:
							landtime="unknown"
			except:
				landtime="unknown"
			try:
				time = line.xpath(".//td[7]//span/text()").extract()
				if time:
					time = str(time[0])
				else:
					time = str(line.xpath(".//td[7]/text()").extract_first())
			except:
				time="unknown"

			item = HangbanItem()
			item['flight'] = flight
			item['date'] = date
			item['dateHref'] = datehref
			item['planeType'] = planetype
			item['offTime'] = offtime
			item['landTime'] = landtime
			item['homeIcao'] = homeicao
			item['pointIcao'] = pointicao
			item['time'] = time
			yield item
