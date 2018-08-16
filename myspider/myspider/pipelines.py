# -*- coding: utf-8 -*-
# __author__ = "吴道子mr.worth@qq.com"

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class MyspiderPipeline(object):
    '''
    useless
    '''
    def process_item(self, item, spider):
        return item

class MysqlPipeline2(object):
	def process_item(self,item,spider):
		if spider.name=="detail":
			self.connect = pymysql.connect(
				host='127.0.0.1',
				port=3306,
				user='hahaha',
				passwd='741741',
				db='flight',
				charset="utf8",
				use_unicode=True
			)
			self.cursor = self.connect.cursor()

			self.sql_update = """update `test_flight` set airline=%s, homeName=%s,
			 homeAirport=%s, pointName=%s, pointAirport=%s,
			planOffTime=%s, actOffTime=%s, planGateOffTime=%s,planLandTime=%s, actLandTime=%s, 
			planGateLandTime=%s,inserted=1 WHERE datehref=%s;
							"""
			# self.connect.open()
			# 数据库更新
			self.cursor.execute(self.sql_update,(item["airline"], item["homeName"], item["homeAirport"], \
												 item["pointName"] \
											   , item["pointAirport"], item["planOffTime"], item["actOffTime"], \
					item["planGateOffTime"],item["planLandTime"], \
												 item["actLandTime"],item["planGateLandTime"],item["selfUrl"]))
			self.connect.commit()
			print("更新成功"*9)
			self.connect.close()
			return  item


		if spider.name=="hangbans":
			self.connect = pymysql.connect(
				host='',
				port=3306,
				user='',
				passwd='',
				db='flight',
				charset="utf8",
				use_unicode=True
			)
			self.cursor = self.connect.cursor()
			self.sqls = '''insert into `test_flight` (`flight`, `date`, `planeType`,`offTime`,`landTime`,
			`homeIcao`,`pointIcao`,`time`,`dateHref`,`inserted`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,5 )'''
			self.cursor.execute(self.sqls, (item["flight"], item["date"], item["planeType"], item["offTime"] \
												, item["landTime"], item["homeIcao"], item["pointIcao"], \
											item["time"], item["dateHref"]))
			self.connect.commit()
			print("更新成功"*9)
			return item


		if spider.name=="zb":
			print("缺失坐标爬取")
			self.connect = pymysql.connect(
				host='',
				port=3306,
				user='',
				passwd='',
				db='flight',
				charset="utf8",
				use_unicode=True
			)
			self.cursor = self.connect.cursor()
			self.sql_update = """update `test_icao` set Latitude=%s, Longtitude=%s WHERE icao=%s;"""
			self.cursor.execute(self.sql_update, (item["wd"], item["jd"], item["icao"]))
			self.connect.commit()
			self.connect.close()
			print("数据库存储成功"*6)
			return item
