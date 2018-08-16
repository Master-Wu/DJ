# -*- coding: utf-8 -*-
'''
设定较简单的代理池
此处可根据需求放置购买的代理ip, 原则上越多越好
实际上,因需求数据量巨大, 需要访问的次数极多,
按访问量或时长计费的代理, 产生的费用较多
故在此我们使用的是网络搜集来的一些公司提供的试用免费代理, 有效率不甚高, 网站废弃这些免费ip也较快
故需要及时更新维护, 最后一次更新时间为: 2018/07/29
本网站, flightaware.com, 需要https代理而非http, 请注意
一个可用的代理网站提供部分可免费使用的代理ip, 地址如下:
http://www.xicidaili.com/
另, 免费代理不建议疯狂爬取, DOWNLOAD_DELAY = xx 处 建议设置延时
如更新代理之后无法运行, 请去掉代理, 本网站无代理也可运行, 只是遭ip封禁较快, 将67-69行禁用中间件
'''

IPPOOL = [
    {"ips": "101.37.79.125:3218"},
    {"ips": "171.37.140.218:9797"},
    {"ips": "58.247.127.145:53281"},
    {"ips": "114.215.95.188:3128"},
    {"ips": "101.236.18.101:8866"},
    {"ips": "106.75.71.122:80"},
    {"ips": "139.129.99.9:3128"},
    {"ips": "58.214.51.151:8070"},
    {"ips": "163.125.64.222:9797"},
    {"ips": "101.37.146.95:3128"},
    {"ips": "218.60.8.99:3129"},
    {"ips": "124.235.208.252:443"},
    {"ips": "180.101.205.253:8888"},
    {"ips": "218.60.8.83:3129"},
    {"ips": "58.48.193.180:3128"},
    {"ips": "115.46.72.117:8123"},
]

BOT_NAME = 'myspider'
SPIDER_MODULES = ['myspider.spiders']
NEWSPIDER_MODULE = 'myspider.spiders'
# 是否遵守爬虫协议
# ROBOTSTXT_OBEY = True

FEED_EXPORT_ENCODING = 'UTF-8'
CONCURRENT_REQUESTS = 200
CONCURRENT_ITEMS = 200
REACTOR_THREADPOOL_MAXSIZE = 20
# 设定全局访问request请求头
DEFAULT_REQUEST_HEADERS ={"Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
	"Cache-Control": "max-age=0",
	"Connection": "keep-alive",
	"DNT": "1",
	"Host": "uk.flightaware.com",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0"
	}
CONCURRENT_REQUESTS_PER_DOMAIN = 500000
CONCURRENT_REQUESTS_PER_IP = 0
# 设定下载网页延时, 可根据需要进行调整, 单位为秒
DOWNLOAD_DELAY = 3
# 将管道加入
ITEM_PIPELINES = {
	'myspider.pipelines.MysqlPipeline2':200,
}
# 将设置有访问代理的中间件加入
DOWNLOADER_MIDDLEWARES = {
   'myspider.middlewares.MyspiderDownloaderMiddleware': 543,
}


# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'myspider.middlewares.MyspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html


# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'myspider.pipelines.MyspiderPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
