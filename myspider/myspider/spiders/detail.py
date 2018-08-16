# -*- coding: utf-8 -*-
# __author__ = "吴道子mr.worth@qq.com"
import pymysql
import scrapy
import json
from argparse import Namespace
from myspider.items import MyspiderItem

# cookie设定地址为en_gb, 而非中文, 避免中文时出现的全球各城市与机场名称的中英文混杂无法有效提取问题
cookies2={
"w_locale":"en_GB"
}

def json_to_object(data):
	'''
	用来转换具有json样式的str到python对象
	:param data: str类型参数
	:return: 返回一个json对象
	'''
	return json.loads(data, object_hook=lambda d: Namespace(**d))

class DetailSpider(scrapy.Spider):
	name = 'detail'
	allowed_domains = ['flightaware.com']

	start_urls = []

	# 重写start_request()
	def start_requests(self):
		# 从数据库中获取分段抓取中已获得的 航班详情页url
		# 并并将url存入list[] detailUrlList中
		conn = pymysql.connect(host="", port=3306, user="", passwd="", db="flight", charset="utf8")
		cur = conn.cursor()
		print("详细信息爬虫"*6)
		sql_select_all_dateHref = "select dateHref from `test_flight` WHERE inserted=5 and idid<101"

		cur.execute(sql_select_all_dateHref)
		rows = cur.fetchall()  # 此句或对应cur.excute(sql_select_all_plane)
		detailUrlList = []
		iii = 0
		for dr in rows:
			if dr[0]:
				detailUrlList.append(dr[0])
				print(iii)
				iii += 1
			else:
				print("""
					""")
				pass
		conn.close()
		for url in detailUrlList:
			yield scrapy.Request(url,cookies=cookies2)

	count=1
	def parse(self, response):
		self_url = "unknown"
		# 本页面url，必须抓取，因为要更新数据库做判断
		airline = "unknown"  # 航空公司

		home_name = "unknown"  # 始发地城市名
		home_airport = "unknown"  # 始发地机场
		point_name = "unknown"  # 目的地城市名
		point_airport = "unknown"  # 目的地机场
		plan_off_time = "unknown"  # 计划起飞时间
		act_off_time = "unknown"  # 实际起飞时间
		plan_gate_off_time = "unknown"  # 计划离开停机坪时间

		plan_land_time = "unknown"  # 计划降落时间
		plan_gate_land_time = "unknown"  # 计划抵达停机坪时间
		act_land_time = "unknown"  # 实际降落时间

		# 截取包含有json的js代码，并将其转换为dictionary
		# try:
		script_40_splited_selector=response.xpath('/html/body/script[40]/text()').extract_first()# 待分割
		script_40_splited=script_40_splited_selector[25:-1] # 已分割
		json_to_dict_script_40_splited = json.loads(script_40_splited)
		key="" # 获取字典的key
		key=list(json_to_dict_script_40_splited['flights'].keys())[0]
		# print(key)
		flight_value_str=json.dumps(json.loads(script_40_splited)["flights"])
		py_object=json_to_object(flight_value_str[len(key)+5:-1])
		try:
			self_url = response.xpath('//*[@id="popupLogin"]/div/div[2]/div/form/input[1]/@value').extract_first()
			# 截去url里可能会有的“uk.“
			self_url = self_url.replace("uk.", "")
			print(self_url,"77777777777777777777777777777777777777777777777777777777777777777")
		except:
			self_url = "unknown"
		# 始发地城市
		try:
			tyy = py_object.origin.friendlyLocation
			home_name = tyy.split(',')[0]
		except:
			home_name="unknown"
		# 始发地机场
		try:
			home_airport =py_object.origin.friendlyName
		except:
			home_airport="unknown"
		# 航空公司
		try:
			airline=py_object.airline.fullName
		except:
			airline="unknown"
		# 目的地城市
		try:
			tyy2=py_object.destination.friendlyLocation
			point_name=tyy2.split(',')[0]
		except:
			point_name="unknown"
		# 目的地机场
		try:
			point_airport=py_object.destination.friendlyName
		except:
			point_airport="unknown"
		# 计划起飞时间
		try:
			plan_off_time=py_object.takeoffTimes.scheduled
		except:
			plan_off_time="unknown"
		# 实际起飞时间
		try:
			act_off_time=py_object.takeoffTimes.estimated
		except:
			act_off_time="unknown"
		# 计划驶出停机坪时间
		try:
			plan_gate_off_time=py_object.gateDepartureTimes.scheduled
		except:
			plan_gate_off_time="unknown"
		# 计划着陆时间
		try:
			plan_land_time=py_object.landingTimes.scheduled
		except:
			plan_land_time="unknown"
		# 实际着陆时间
		try:
			act_land_time=py_object.landingTimes.estimated
		except:
			act_land_time="unknown"
		# 实际进入停机坪时间
		try:
			plan_gate_land_time=py_object.gateArrivalTimes.scheduled
		except:
			plan_gate_land_time="unknown"
		item = MyspiderItem()
		item['selfUrl'] = self_url
		item['airline'] = airline
		item['homeName'] = home_name
		item['homeAirport'] = home_airport
		item['pointName'] = point_name
		item['pointAirport'] = point_airport

		item['planOffTime'] = plan_off_time
		item['actOffTime'] = act_off_time
		item['planGateOffTime'] = plan_gate_off_time

		item['planLandTime'] = plan_land_time
		item['planGateLandTime'] = plan_gate_land_time
		item['actLandTime'] = act_land_time
		print("你看到的是：",self.count)
		self.count+=1
		yield item
