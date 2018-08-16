#coding:utf-8
import scrapy
import pymysql
from bs4 import BeautifulSoup


# cookies最近更新2018/06/27
cookies={
'w_sid':'fb4541e11f80effe7bee215a2edae7ded07f779c6f01b94f30580a9b9654d50e',
'update_time':'1524795947',
'd7s_uid':'jghc2wi54c2w99',
'__qca':'P0-172568615-1530085007061',
'__rtgt_sid':'jiwt5ttj9kt0s9',
'd7s_spc':'2',
'_ceg.s':'paz18k',
'_ceg.u':'paz18k'
	}


class FlightidSpider(scrapy.Spider):
    name = "flightid"
    allowed_domain = ["flightaware.com"]
    start_urls = []

    def start_requests(self):
        db = pymysql.connect(host="122.114.69.20", port=3306, user="chutianbo", passwd="GYD161@hnlyzyxy", db="flight",
                             charset="utf8")
        cursor = db.cursor()
        cursor.execute("""select ICAO from test_icao""")
        db.commit()
        results = cursor.fetchall()
        start_urls1 = []
        for icao in results:
            url1 = ("https://flightaware.com/live/airport/%s/departures?;offset=0;order=actualarrivaltime;sort=DESC"
                    % (icao[0]))
            url2 = ("https://flightaware.com/live/airport/%s/arrivals?;offset=0;order=actualarrivaltime;sort=DESC"
                    % (icao[0]))
            start_urls1.append(url1)
            start_urls1.append(url2)

        for url in start_urls1:
            yield scrapy.Request(url, cookies=cookies)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        aqq=response.xpath("//a/text()").extract_first()
        hh=response.xpath("//span[@style='font-size: x-small']/a[1]/text()").extract_first()
        db = pymysql.connect(host="122.114.69.20", port=3306, user="chutianbo", passwd="GYD161@hnlyzyxy", db="flight",
                             charset="utf8")
        cursor = db.cursor()
        if hh=="后40条":
            url= response.xpath("//span[@style='font-size: x-small']/a[1]/@href").extract_first()
            for b in soup.select('a[href^="/live/flight/id/"]'):
                sql_str="insert into test_flightnum(flightid) value(%s)"
                # try:
                cursor.execute(sql_str,(b.text))
                db.commit()
                print("999999")
                # except:
                #     # 如果发生错误则回滚
                #     db.rollback()
            yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

