# -*- coding:utf-8 -*-
filename = 'tianyancha_detail.json'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import time

import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from scrapy import Selector


def get_zero(s):
    if s:
        return s
    else:
        return "0"


def get_none(s):
    if s:
        return s
    else:
        return ""


def get_list(type, jianjie):
    if type == 1:  # 专家
        zhuanjia_list = [u"中国科学院院士", u"中国工程院院士", u"教授", u"研究员", u"副教授", u"副研究员", u"博士生导师", u"长江学者", u"千人计划（海外高层次人才引进计划）", u"杰青（国家杰出青年科学基金获得者）", u"助理教授", u"青年千人计划", u"优青（国家优秀青年科学基金获得者）"]
        return [word for word in zhuanjia_list if word in jianjie]
    elif type == 2:  # 学历
        xueli_list = [u"博士后", u"博士", u"硕士", u"本科", u"大专", u"专科", u"高中"]
        for word in xueli_list:
            if word in jianjie:
                return word
        return ""
    elif type == 3:  # 名企
        mingqi_list = [u"谷歌", u"微软", u"facebook", u"IBM", u"苹果", u"亚马逊", u"百度", u"阿里", u"腾讯", u"京东", u"丰田", u"大众", u"三星", u"特斯拉", u"ABB", u"KUKA", u"高盛", u"Uber", u"英特尔", u"联想", u"滴滴出行", u"美团", u"今日头条", u"福特", u"思科", u"网易", u"搜狗u", u"华为", u"富士康", u"新松", u"小米", u"强生", u"宝洁", u"摩根大通", u"索尼", u"西门子"]
        return [word for word in mingqi_list if word in jianjie]
    elif type == 4:  # 名校
        mingxiao_list = [u"清华大学", u"北京大学", u"复旦中学", u"上海交通大学", u"哈佛大学", u"斯坦福大学", u"剑桥大学", u"麻省理工学院", u"加州理工大学", u"普林斯顿大学", u"武汉大学", u"浙江大学", u"南开大学", u"中国人民大学", u"哈尔滨工业大学", u"西安交通大学", u"耶鲁大学", u"香港大学", u"牛津大学", u"南洋理工大学", u"苏黎世联邦理工学院", u"南京大学", u"北京航空航天大学", u"东南大学", u"华中科技大学", u"北京理工大学", u"同济大学", u"四川大学", u"吉林大学", u"芝加哥大学", u"宾夕法尼亚大学", u"约翰霍普金斯大学", u"哥伦比亚大学", u"密歇根大学", u"中国农业大学", u"北京师范大学", u"厦门大学", u"大连理工大学", u"华南理工大学", u"山东大学", u"东南大学", u"北京交通大学", u"杜克大学", u"爱丁堡大学", u"帝国理工大学", u"西北大学", u"伦敦大学学院"]
        return [word for word in mingxiao_list if word in jianjie]


with open('detail_fail.txt') as f:
    fail = list(set([i.strip() for i in f.readlines()]))
with open('detail_done.txt') as f:
    done = list(set([i.strip() for i in f.readlines()]))
with open('detail_url.txt') as f:
    urls = list(set([i.strip() for i in f.readlines()]))
todo = [i for i in urls if i not in done + fail]

cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.settings.resourceTimeout"] = 1000
cap["phantomjs.page.settings.loadImages"] = True
cap["phantomjs.page.settings.disk-cache"] = True
cap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
path = '/Users/debrahe/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs'
driver = webdriver.PhantomJS(path, desired_capabilities=cap)
driver.get('https://www.tianyancha.com/login')
time.sleep(10)
driver.save_screenshot('screen.jpg')
element = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.CSS_SELECTOR, 'div.loginmodule')),
    'login fail'
)
driver.save_screenshot('screen.jpg')
username_str = '15010495608'
password_str = 'ruyiruyi111'
username = driver.find_element_by_css_selector('div.mobile_box input.contactphone')
username.clear()
username.send_keys(username_str)
password = driver.find_element_by_css_selector('div.mobile_box input.contactword')
password.clear()
password.send_keys(password_str)
driver.find_element_by_css_selector('div.mobile_box div.login_btn').click()


element = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.CSS_SELECTOR, 'input#home-main-search')),
    "login fail"
)
driver.save_screenshot('screen.jpg')
for search_url in todo:
    try:
        print 'crawl  ' + search_url
        driver.get(search_url)

        element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'div.company_header_width')),
            "search fail"
        )
        result = {
            'meta_version': 'v1.0',
            'meta_updated': datetime.datetime.now().isoformat()[:19],
            'download_config': {
                'url': search_url,
                'method': 'GET',
            },
            'download_data': {
                'parsed_data': {},
                'raw_data': {},
            }
        }
        font_dict = {
            '.': '0',
            '8': '1',
            '9': '2',
            '2': '3',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7',
            '0': '8',
            '3': '9',
        }
        item = {}
        response = Selector(text=driver.page_source)

        item[u'公司名称'] = get_none(
            response.xpath('//div[@class="company_header_width ie9Style"]/div[1]/span[1]//text()').extract_first())
        item[u'主营业务'] = get_none(
            response.xpath('//div[@id="nav-main-stockNum"]//table/tbody/tr[3]/td[4]//text()').extract_first())
        item[u'所属行业'] = get_none(
            response.xpath('//div[@id="nav-main-stockNum"]//table/tbody/tr[3]/td[2]//text()').extract_first())
        item[u'员工人数'] = get_none(
            response.xpath('//div[@id="nav-main-stockNum"]//table/tbody/tr[6]/td[4]//text()').extract_first())

        item[u'电话'] = get_none(response.xpath('//div[@class="f14 sec-c2 mt10"]/div[1]/span[2]//text()').extract_first())
        item[u'邮箱'] = get_none(response.xpath('//div[@class="f14 sec-c2 mt10"]/div[2]/span[2]//text()').extract_first())
        item[u'网址'] = get_none(response.xpath('//div[@class="f14 sec-c2"]/div[1]/a//text()').extract_first())
        item[u'地址'] = get_none(response.xpath('//div[@class="f14 sec-c2"]/div[2]/span[2]//text()').extract_first())
        # item[u'注册资本'] = get_none(
        #     response.xpath('//div[@class="baseInfo_model2017"]/table/tbody/tr[1]/td[2]//text[@class="tyc-num"]//text()').extract_first())
        item[u'工商注册号'] = get_none(
            response.xpath('//div[@class="base0910"]/table/tbody/tr[1]/td[2]//text()').extract_first())
        item[u'组织机构代码'] = get_none(
            response.xpath('//div[@class="base0910"]/table/tbody/tr[1]/td[4]//text()').extract_first())
        item[u'统一信用代码'] = get_none(
            response.xpath('//div[@class="base0910"]/table/tbody/tr[2]/td[2]//text()').extract_first())
        item[u'公司类型'] = get_none(
            response.xpath('//div[@class="base0910"]/table/tbody/tr[2]/td[4]//text()').extract_first())
        item[u'纳税人识别号'] = get_none(
            response.xpath('//div[@class="base0910"]/table/tbody/tr[3]/td[2]//text()').extract_first())
        item[u'行业'] = get_none(
            response.xpath('//div[@class="base0910"]/table/tbody/tr[3]/td[4]//text()').extract_first())
        item[u'营业期限'] = get_none(
            response.xpath('//div[@class="base0910"]/table/tbody/tr[4]/td[2]//text()').extract_first())

        check_date = get_none(
            response.xpath('//div[@class="base0910"]/table/tbody/tr[4]/td[4]//text()').extract_first())
        item[u'核准日期'] = ''.join([font_dict.get(num) if num in font_dict else num for num in check_date])
        item[u'登记机关'] = get_none(
            response.xpath('//div[@class="base0910"]/table/tbody/tr[5]/td[2]//text()').extract_first())
        item[u'英文名称'] = get_none(
            response.xpath('//div[@class="base0910"]/table/tbody/tr[5]/td[4]//text()').extract_first())
        item[u'注册地址'] = get_none(
            response.xpath('//div[@class="base0910"]/table/tbody/tr[6]/td[2]//text()').extract_first())
        item[u'经营范围'] = ''
        if response.xpath(
                '//div[@class="base0910"]/table/tbody/tr[7]//span[@class="js-full-container hidden"]//text()').extract_first():
            item[u'经营范围'] = response.xpath(
                '//div[@class="base0910"]/table/tbody/tr[7]//span[@class="js-full-container hidden"]//text()').extract_first().replace(
                u'...', '')
        elif response.xpath(
                '//div[@class="base0910"]/table/tbody/tr[7]//span[@class="js-split-container hidden"]//text()').extract_first():
            item[u'经营范围'] = response.xpath(
                '//div[@class="base0910"]/table/tbody/tr[7]//span[@class="js-split-container hidden"]//text()').extract_first().replace(
                u'...', '')
        item[u'评分'] = get_none(response.xpath('//div[@class="base0910"]/table/tbody/tr[1]/td[5]/img/@alt').extract_first())
        item[u'公司标签'] = response.css('span.company-tag::text').extract() + response.css('span.company-tag span').xpath('string(.)').extract()

        item[u'个数'] = {
            u'参股控股': get_zero(response.css('div#nav-main-holdingCompanyNum span.intro-count::text').extract_first()),
            u'自身风险': get_zero(response.css('span.selfRisk::text').extract_first()),
            u'周边风险': get_zero(response.css('span.roundRisk::text').extract_first()),
            u'对外投资': get_zero(response.css('div#nav-main-inverstCount span.intro-count::text').extract_first()),
            u'变更记录': get_zero(response.css('div#nav-main-changeCount span.intro-count::text').extract_first()),
            u'融资历史': get_zero(response.css('div#nav-main-companyRongzi span.intro-count::text').extract_first()),
            u'核心团队': get_zero(response.css('div#nav-main-companyTeammember span.intro-count::text').extract_first()),
            u'企业业务': get_zero(response.css('div#nav-main-companyProduct span.intro-count::text').extract_first()),
            u'投资事件': get_zero(response.css('div#nav-main-jigouTzanli span.intro-count::text').extract_first()),
            u'竞品信息': get_zero(response.css('div#nav-main-companyJingpin span.intro-count::text').extract_first()),
            u'法律诉讼': get_zero(response.css('div#nav-main-lawsuitCount span.intro-count::text').extract_first()),
            u'法院公告': get_zero(response.css('div#nav-main-courtCount span.intro-count::text').extract_first()),
            u'被执行人': get_zero(response.css('div#nav-main-zhixing span.intro-count::text').extract_first()),
            u'开庭公告': get_zero(response.css('div#nav-main-announcementCount span.intro-count::text').extract_first()),
            u'行政处罚': get_zero(response.css('div#nav-main-punishment span.intro-count::text').extract_first()),
            u'股权出质': get_zero(response.css('div#nav-main-equityCount span.intro-count::text').extract_first()),
            u'招投标': get_zero(response.css('div#nav-main-bidCount span.intro-count::text').extract_first()),
            u'招聘': get_zero(response.css('div#nav-main-recruitCount span.intro-count::text').extract_first()),
            u'税务评级': get_zero(response.css('div#nav-main-taxCreditCount span.intro-count::text').extract_first()),
            u'抽查检查': get_zero(response.css('div#nav-main-checkCount span.intro-count::text').extract_first()),
            u'产品信息': get_zero(response.css('div#nav-main-productinfo span.intro-count::text').extract_first()),
            u'资质证书': get_zero(response.css('div#nav-main-certificateCount span.intro-count::text').extract_first()),
            u'微信公众号信息': get_zero(response.css('div#nav-main-weChatCount span.intro-count::text').extract_first()),
            u'商标信息': get_zero(response.css('div#nav-main-tmCount span.intro-count::text').extract_first()),
            u'专利信息': get_zero(response.css('div#nav-main-patentCount span.intro-count::text').extract_first()),
            u'软件著作权': get_zero(response.css('div#nav-main-cpoyRCount span.intro-count::text').extract_first()),
            u'作品著作权': get_zero(response.css('div#nav-main-copyrightWorks span.intro-count::text').extract_first()),
            u'网站备案': get_zero(response.css('div#nav-main-icpCount span.intro-count::text').extract_first()),
        }

        seniorPeople_list = []
        for tr in response.css('div#_container_seniorPeople table.table tbody tr'):
            seniorPeople_dict = {
                u'姓名': get_none(tr.css('td:nth-child(1) a::text').extract_first()),
                u'学历': get_none(tr.css('td:nth-child(5)::text').extract_first()),
                u'职务': get_none(tr.css('td:nth-child(2)::text').extract_first())
            }
            seniorPeople_list.append(seniorPeople_dict)
        item[u'高管信息'] = seniorPeople_list[:]

        team_member_list = []
        team_member_num = int(response.css('div#_container_teamMember div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_teamMember div.company_pager div.total').re('[\d]+') else 1)
        for i in range(team_member_num):
            team_member_response = Selector(text=driver.page_source)
            team_member_info = team_member_response.css('div#_container_teamMember')
            for tr in team_member_info.css('div.team-item'):
                jianjie = get_none(' '.join(tr.css('div.team-right ul span::text').extract()))
                team_member_dict = {
                    u'姓名': get_none(tr.css('div.team-left div.team-name::text').extract_first()),
                    u'头像': get_none(tr.css('div.team-left div.img-outer img::attr(src)').extract_first()),
                    u'职位': get_none(tr.css('div.team-right div.team-title::text').extract_first()),
                    u'简介': jianjie,

                    u'专家': get_list(1, jianjie),
                    u'学历': get_list(2, jianjie),
                    u'名企': get_list(3, jianjie),
                    u'名校': get_list(4, jianjie),
                }
                team_member_list.append(team_member_dict)
            if i < (team_member_num - 1):
                driver.find_element_by_css_selector('div#_container_teamMember div.company_pager li.pagination-next a').click()
                time.sleep(10)
        item[u'核心团队'] = team_member_list[:]

        rongzi_list = []
        rongzi_num = int(response.css('div#_container_rongzi div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_rongzi div.company_pager div.total').re('[\d]+') else 1)
        for i in range(rongzi_num):
            rongzi_response = Selector(text=driver.page_source)
            rongzi_info = rongzi_response.css('div#_container_rongzi table.table')
            for tr in rongzi_info.css('tbody tr'):
                rongzi_dict = {
                    u'时间': get_none(tr.css('td:nth-child(1) span::text').extract_first()),
                    u'轮次': get_none(tr.css('td:nth-child(2) span::text').extract_first()),
                    u'估值': get_none(tr.css('td:nth-child(3) span::text').extract_first()),
                    u'金额': get_none(tr.css('td:nth-child(4) span::text').extract_first()),
                    u'比例': get_none(tr.css('td:nth-child(5) span a.text-dark-color::text').extract_first()),
                    u'投资方': get_none(tr.css('td:nth-child(6) span a.text-dark-color::text').extract()),
                    u'新闻来源': get_none(tr.css('td:nth-child(7) span a.text-dark-color::text').extract_first()),
                }
                rongzi_list.append(rongzi_dict)
            if i < (rongzi_num - 1):
                driver.find_element_by_css_selector('div#_container_rongzi div.company_pager li.pagination-next a').click()
                time.sleep(10)
        item[u'融资历史'] = rongzi_list[:]

        bid_list = []
        bid_num = int(response.css('div#_container_bid div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_bid div.company_pager div.total').re('[\d]+') else 1)
        for i in range(bid_num):
            bid_response = Selector(text=driver.page_source)
            bid_info = bid_response.css('div#_container_bid')
            for tr in bid_info.css('table.table tbody tr'):
                bid_dict = {
                    u'发布时间': get_none(tr.css('td:nth-child(1) span::text').extract_first()),
                    u'标题': get_none(tr.css('td:nth-child(2) a::text').extract_first()),
                    u'采购人': get_none(tr.css('td:nth-child(3) span::text').extract_first()),
                    u'url': get_none(
                        'https://www.tianyancha.com' + tr.css('td:nth-child(2) a::attr(href)').extract_first()),
                }
                bid_list.append(bid_dict)
            if i < (bid_num - 1):
                driver.find_element_by_css_selector(
                    'div#_container_bid div.company_pager li.pagination-next a').click()
                time.sleep(10)
        item[u'招投标'] = bid_list[:]

        taxcredit_list = []
        taxcredit_num = int(response.css('div#_container_taxcredit div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_taxcredit div.company_pager div.total').re('[\d]+') else 1)
        for i in range(taxcredit_num):
            taxcredit_response = Selector(text=driver.page_source)
            taxcredit_info = taxcredit_response.css('div#_container_taxcredit')
            for tr in taxcredit_info.css('table.table tbody tr'):
                taxcredit_dict = {
                    u'年份': get_none(tr.css('td:nth-child(1) span::text').extract_first()),
                    u'纳税评级': get_none(tr.css('td:nth-child(2) span::text').extract_first()),
                    u'类型': get_none(tr.css('td:nth-child(3) span::text').extract_first()),
                    u'纳税人识别号': get_none(tr.css('td:nth-child(4) span::text').extract_first()),
                    u'评价单位': get_none(tr.css('td:nth-child(5) span::text').extract_first()),
                }
                taxcredit_list.append(taxcredit_dict)
            if i < (taxcredit_num - 1):
                driver.find_element_by_css_selector(
                    'div#_container_taxcredit div.company_pager li.pagination-next a').click()
                time.sleep(10)
        item[u'税务评级'] = taxcredit_list[:]

        result['download_data']['parsed_data'] = item.copy()
        with open('{}'.format(filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)
        with open('detail_done.txt', 'a') as f:
            f.write(search_url + '\n')
    except:
        driver.save_screenshot('fail.jpg')
        with open('detail_fail.txt', 'a') as f:
            f.write(search_url + '\n')

