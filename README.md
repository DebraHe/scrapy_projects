# scrapy_projects 某AI公司 爬虫实习生  三个月  项目  
## 词语
### [词语接龙]
- 策略：遍历沪江网上所有词语，在中华诗词网上查找相关拼音，由于数量庞大，服务器采用Redis做存储下载并上传s3。
- 使用情况    
  webdriver：无  
  redis：有  
  代理：无  
  反爬：无 

### [每日英语]
- 策略：抓取API数据，爬取四小时后对数据进行筛选，选出不重复数据，下载并上传s3。
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无  

### [名人名言]
- 策略：抓取网页数据，下载并上传s3。
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 


## 化工  
### [盖德化工网]
**使用abuyun代理，需要及时续费或更换其他代理。**
- 策略：通过notyet.txt获取需要爬取的数据，将爬取成功的数据保存在done.txt中。
- 使用情况    
  webdriver：无  
  redis：无  
  代理：阿布云  
  反爬：有，需要代理。 

## 儿童百科 
### [十万个为什么]
- 代码：[http://gitlab.ruyi.ai/heh/ruyi-scrapy/tree/master/tom61](http://gitlab.ruyi.ai/heh/ruyi-scrapy/tree/master/tom61)
- 策略：通过target_utl.txt进入每一个需要爬取的页面，遍历所有词条进行爬取。   
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 

## 食物
### [香哈网]
- 策略：进入list，进入detail 
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 


## 天气
### [和风天气]
- 策略：从城市txt中读取城市列表，调用和风天气API，获取相关数据，保存到MongoDB中。
- 数据：MongoDB  
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 

# 工商
### [天眼查]
- 策略: 广度优先，先爬完所有list，再爬detail。登录使用selenium.webdriver，当爬取量大时进list和detail前要先login。
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 

# 有声
### [喜马拉雅]
- 策略: 深度优先，进入list页面后再进detail，list和detail均要翻页，全程通过网页爬取，无api
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 

### [网易云音乐-歌词]
- 策略: 全程通过api抓取 
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 

### [网易云音乐-评论]
- 策略: 全程通过api抓取 
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 


## 新闻  
### [环保保护部污染源监控中心—信息发布]
- 策略: 深度优先，进入list页面后再进detail，list和detail均要翻页，全程通过网页爬取，无api
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 

### [环保保护部污染源监控中心—工作动态]
- 策略: 深度优先，进入list页面后再进detail，list和detail均要翻页，全程通过网页爬取，无api
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 

### [中药材天地网-产地快讯]
- 策略: 深度优先，进入list页面后再进detail，list和detail均要翻页，全程通过网页爬取，无api
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 


### [药通网-天天行情]
- 策略: 深度优先，进入list页面后再进detail，list和detail均要翻页，全程通过网页爬取，无api
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 


### [中国禽病网-动态]
- 策略: 深度优先，进入list页面后再进detail，list和detail均要翻页，全程通过网页爬取，无api
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 

### [吾爱化学城]
- 策略: 深度优先，进入list页面后再进detail，list和detail均要翻页，全程通过网页爬取，无api
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 

### [中国产业信息网-包装频道]
- 策略: 深度优先，进入list页面后再进detail，list和detail均要翻页，全程通过网页爬取，无api
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 

### [中华人民共和国中央政府网-新闻、政策、数据]
- 代码： [http://gitlab.ruyi.ai/heh/ruyi-scrapy/tree/master/gov_cn](http://gitlab.ruyi.ai/heh/ruyi-scrapy/tree/master/gov_cn)
- 策略: 深度优先，进入list页面后再进detail，list和detail均要翻页，全程通过网页爬取，无api
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 

## 国家公网  
### [裁决文书网]
- 代码： [https://github.com/DebraHe/scrapy_projects/tree/master/can_rk](https://github.com/DebraHe/scrapy_projects/tree/master/can_rk)
- 策略: 深度优先，进入list页面后再进detail，list和detail均要翻页，全程通过网页爬取，无api
- 使用情况    
  webdriver：有  
  redis：有  
  代理：无  
  反爬：无 

### [失信]
- 代码： [https://github.com/DebraHe/scrapy_projects/tree/master/can_rk](https://github.com/DebraHe/scrapy_projects/tree/master/can_rk)
- 策略: 深度优先，进入list页面后再进detail，list和detail均要翻页，全程通过网页爬取，无api
- 使用情况    
  webdriver：无  
  redis：有  
  代理：无  
  反爬：无 

### [执行]
- 代码： [https://github.com/DebraHe/scrapy_projects/tree/master/can_rk](https://github.com/DebraHe/scrapy_projects/tree/master/can_rk)
- 策略: 深度优先，进入list页面后再进detail，list和detail均要翻页，全程通过网页爬取，无api
- 使用情况    
  webdriver：无  
  redis：有  
  代理：无  
  反爬：无 
 
### [蜻蜓]
- 策略: 添加position字段 
- 使用情况    
  webdriver：无  
  redis：无  
  代理：无  
  反爬：无 
