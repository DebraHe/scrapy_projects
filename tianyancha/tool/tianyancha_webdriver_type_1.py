# -*- coding:utf-8 -*-
filename = 'tianyancha_detail.json'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import time

import re

import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from scrapy import Selector

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
username_str = '18020878508'
password_str = 'ruyi1234'
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
        item = {}
        response = Selector(text=driver.page_source)
        item[u'名称'] = response.xpath('//div[@class="company_header_width ie9Style"]/div[1]/span[1]//text()').extract_first()
        item[u'电话'] = response.xpath('//div[@class="f14 sec-c2 mt10"]/div[1]/span[2]//text()').extract_first()
        item[u'邮箱'] = response.xpath('//div[@class="f14 sec-c2 mt10"]/div[2]/span[2]//text()').extract_first()
        item[u'网址'] = response.xpath('//div[@class="f14 sec-c2"]/div[1]/a//text()').extract_first()
        item[u'地址'] = response.xpath('//div[@class="f14 sec-c2"]/div[2]/span[2]//text()').extract_first()
        item[u'工商注册号'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[1]/td[2]//text()').extract_first()
        item[u'组织机构代码'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[1]/td[4]//text()').extract_first()
        item[u'统一信用代码'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[2]/td[2]//text()').extract_first()
        item[u'企业类型'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[2]/td[4]//text()').extract_first()
        item[u'纳税人识别号'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[3]/td[2]//text()').extract_first()
        item[u'行业'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[3]/td[4]//text()').extract_first()
        item[u'营业期限'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[4]/td[2]//text()').extract_first()
        item[u'核准日期'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[4]/td[4]//text()').extract_first()
        item[u'登记机关'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[5]/td[2]//text()').extract_first()
        item[u'注册地址'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[6]/td[2]//text()').extract_first()
        if response.xpath('//div[@class="base0910"]/table/tbody/tr[7]//span[@class="js-full-container hidden"]//text()').extract_first():
            item[u'经营范围'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[7]//span[@class="js-full-container hidden"]//text()').extract_first().replace(u'...', '')
        elif response.xpath('//div[@class="base0910"]/table/tbody/tr[7]//span[@class="js-split-container hidden"]//text()').extract_first():
            item[u'经营范围'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[7]//span[@class="js-split-container hidden"]//text()').extract_first().replace(u'...', '')
        item[u'评分'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[1]/td[5]/img/@alt').extract_first()

        staff_list = []
        for staff in response.css('div#_container_staff div.staffinfo-module-container'):
            staff_dict = {
                u'职务': staff.css('span::text').extract_first() if staff.css('span::text').extract_first() else '',
                u'姓名': staff.css('a.overflow-width::text').extract_first() if staff.css(
                    'a.overflow-width::text').extract_first() else '',
            }
            staff_list.append(staff_dict)
        item[u'主要人员'] = staff_list[:]


        gudong_list = []
        gudong_num = int(response.css('div#_container_holder div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_holder div.company_pager div.total').re('[\d]+') else 1)
        for i in range(gudong_num):
            gudong_response = Selector(text=driver.page_source)
            gudong_info = gudong_response.css('div#_container_holder table.table')
            for tr in gudong_info.css('tbody tr'):
                gudong_dict = {
                    u'股东': tr.css('td:nth-child(1) a::attr(title)').extract_first() if tr.css(
                        'td:nth-child(1) a::attr(title)').extract_first() else '',
                    u'出资比例': tr.css('td:nth-child(2) span.c-money-y::text').extract_first() if tr.css(
                        'td:nth-child(2) span.c-money-y::text').extract_first() else '',
                    u'认缴出资': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
                        'td:nth-child(3) span::text').extract_first() else '',
                }
                gudong_list.append(gudong_dict)
            if i < (gudong_num - 1):
                driver.find_element_by_css_selector('div#_container_holder div.company_pager li.pagination-next a').click()
                time.sleep(10)
        item[u'股东信息'] = gudong_list[:]

        invest_list = []
        invest_num = int(response.css('div#_container_invest div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_invest div.company_pager div.total').re('[\d]+') else 1)
        for i in range(invest_num):
            invest_response = Selector(text=driver.page_source)
            invest_info = invest_response.css('div#_container_invest')
            for tr in invest_info.css('table.table tbody tr'):
                invest_dict = {
                    u'被投资企业名称': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
                        'td:nth-child(1) span::text').extract_first() else '',
                    u'被投资法定代表人': tr.css('td:nth-child(2) a.new-c4::text').extract_first() if tr.css(
                        'td:nth-child(2) a.new-c4::text').extract_first() else '',
                    u'注册资本': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
                        'td:nth-child(3) span::text').extract_first() else '',
                    u'投资数额': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
                        'td:nth-child(4) span::text').extract_first() else '',
                    u'投资占比': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
                        'td:nth-child(5) span::text').extract_first() else '',
                    u'注册时间': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
                        'td:nth-child(6) span::text').extract_first() else '',
                    u'状态': tr.css('td:nth-child(7) span::text').extract_first() if tr.css(
                        'td:nth-child(7) span::text').extract_first() else '',
                }
                invest_list.append(invest_dict)
            if i < (invest_num - 1):
                driver.find_element_by_css_selector('div#_container_invest div.company_pager li.pagination-next a').click()
                time.sleep(10)
        item[u'对外投资'] = invest_list[:]


        # biangeng_list = []
        # biangeng_num = int(response.css('div#_container_changeinfo div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_changeinfo div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(biangeng_num):
        #     biangeng_response = Selector(text=driver.page_source)
        #     biangeng_info = biangeng_response.css('div#_container_changeinfo table.table')
        #     for tr in biangeng_info.css('tbody tr'):
        #         biangeng_dict = {
        #             u'变更时间': tr.css('td:nth-child(1) div::text').extract_first() if tr.css(
        #                 'td:nth-child(1) div::text').extract_first() else '',
        #             u'变更项目': tr.css('td:nth-child(2) div::text').extract_first() if tr.css(
        #                 'td:nth-child(2) div::text').extract_first() else '',
        #             u'变更前': tr.css('td:nth-child(3) div.changeHoverText').xpath('string(.)').extract_first() if tr.css(
        #                 'td:nth-child(3) div.changeHoverText').xpath('string(.)').extract_first() else '',
        #             u'变更后': tr.css('td:nth-child(4) div.changeHoverText').xpath('string(.)').extract_first() if tr.css(
        #                 'td:nth-child(3) div.changeHoverText').xpath('string(.)').extract_first() else '',
        #         }
        #         biangeng_list.append(biangeng_dict)
        #     if i < (biangeng_num - 1):
        #         driver.find_element_by_css_selector('div#_container_changeinfo div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'变更记录'] = biangeng_list[:]
        #
        # rongzi_list = []
        # rongzi_num = int(response.css('div#_container_rongzi div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_rongzi div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(rongzi_num):
        #     rongzi_response = Selector(text=driver.page_source)
        #     rongzi_info = rongzi_response.css('div#_container_rongzi table.table')
        #     for tr in rongzi_info.css('tbody tr'):
        #         rongzi_dict = {
        #             u'时间': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'轮次': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'估值': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'金额': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #                 'td:nth-child(4) span::text').extract_first() else '',
        #             u'比例': tr.css('td:nth-child(5) span a.text-dark-color::text').extract_first() if tr.css(
        #                 'td:nth-child(5) span a.text-dark-color::text').extract_first() else '',
        #             u'投资方': tr.css('td:nth-child(6) span a.text-dark-color::text').extract() if tr.css(
        #                 'td:nth-child(6) span a.text-dark-color::text').extract() else [],
        #             u'新闻来源': tr.css('td:nth-child(7) span a.text-dark-color::text').extract_first() if tr.css(
        #                 'td:nth-child(7) span a.text-dark-color::text').extract_first() else '',
        #         }
        #         rongzi_list.append(rongzi_dict)
        #     if i < (rongzi_num - 1):
        #         driver.find_element_by_css_selector('div#_container_rongzi div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'融资历史'] = rongzi_list[:]
        #
        #
        # team_member_list = []
        # team_member_num = int(response.css('div#_container_teamMember div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_teamMember div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(team_member_num):
        #     team_member_response = Selector(text=driver.page_source)
        #     team_member_info = team_member_response.css('div#_container_teamMember')
        #     for tr in team_member_info.css('div.team-item'):
        #         team_member_dict = {
        #             u'姓名': tr.css('div.team-left div.team-name::text').extract_first() if tr.css(
        #                 'div.team-left div.team-name::text').extract_first() else '',
        #             u'头像': tr.css('div.team-left div.img-outer img::attr(src)').extract_first() if tr.css(
        #                 'div.team-left div.img-outer img::attr(src)').extract_first() else '',
        #             u'职位': tr.css('div.team-right div.team-title::text').extract_first() if tr.css(
        #                 'div.team-right div.team-title::text').extract_first() else '',
        #             u'简介': ' '.join(tr.css('div.team-right ul span::text').extract()) if ' '.join(
        #                 tr.css('div.team-right ul span::text').extract()) else '',
        #         }
        #         team_member_list.append(team_member_dict)
        #     if i < (team_member_num - 1):
        #         driver.find_element_by_css_selector('div#_container_teamMember div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'核心团队'] = team_member_list[:]
        #
        #
        # firmProduct_list = []
        # firmProduct_num = int(response.css('div#_container_firmProduct div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_firmProduct div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(firmProduct_num):
        #     firmProduct_response = Selector(text=driver.page_source)
        #     firmProduct_info = firmProduct_response.css('div#_container_firmProduct')
        #     for tr in firmProduct_info.css('div.product-item'):
        #         firmProduct_dict = {
        #             u'名称': tr.css('div.product-right span.title::text').extract_first() if tr.css(
        #                 'div.product-right span.title::text').extract_first() else '',
        #             u'图标': tr.css('div.product-left img::attr(src)').extract_first() if tr.css(
        #                 'div.product-left img::attr(src)').extract_first() else '',
        #             u'行业': tr.css('div.product-right div.hangye::text').extract_first() if tr.css(
        #                 'div.product-right div.hangye::text').extract_first() else '',
        #             u'简介': ' '.join(tr.css('div.product-right div.yeweu::text').extract()) if ' '.join(
        #                 tr.css('div.product-right div.yeweu::text').extract()) else '',
        #         }
        #         firmProduct_list.append(firmProduct_dict)
        #     if i < (firmProduct_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_firmProduct div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'企业业务'] = firmProduct_list[:]
        #
        #
        # touzi_event_list = []
        # touzi_event_num = int(response.css('div#_container_touzi div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_touzi div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(touzi_event_num):
        #     touzi_event_response = Selector(text=driver.page_source)
        #     touzi_event_info = touzi_event_response.css('div#_container_touzi')
        #     for tr in touzi_event_info.css('table.table tbody tr'):
        #         touzi_event_dict = {
        #             u'时间': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'轮次': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'金额': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'投资方': tr.css('td:nth-child(4) a::text').extract() if tr.css(
        #                 'td:nth-child(4) a::text').extract() else [],
        #             u'产品': tr.css('td:nth-child(5) a::text').extract_first() if tr.css(
        #                 'td:nth-child(5) a::text').extract_first() else '',
        #             u'地区': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #                 'td:nth-child(6) span::text').extract_first() else '',
        #             u'行业': tr.css('td:nth-child(7) span::text').extract_first() if tr.css(
        #                 'td:nth-child(7) span::text').extract_first() else '',
        #             u'业务': tr.css('td:nth-child(8) span::text').extract_first() if tr.css(
        #                 'td:nth-child(8) span::text').extract_first() else '',
        #         }
        #         touzi_event_list.append(touzi_event_dict)
        #     if i < (touzi_event_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_touzi div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'投资事件'] = touzi_event_list[:]
        #
        # jingpin_list = []
        # jingpin_num = int(response.css('div#_container_jingpin div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_jingpin div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(jingpin_num):
        #     jingpin_response = Selector(text=driver.page_source)
        #     jingpin_info = jingpin_response.css('div#_container_jingpin')
        #     for tr in jingpin_info.css('table.table tbody tr'):
        #         jingpin_dict = {
        #             u'产品': tr.css('td:nth-child(1) a::text').extract_first() if tr.css(
        #                 'td:nth-child(1) a::text').extract_first() else '',
        #             u'地区': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'当前轮次': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'行业': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #                 'td:nth-child(4) span::text').extract_first() else '',
        #             u'业务': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #                 'td:nth-child(5) span::text').extract_first() else '',
        #             u'成立时间': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #                 'td:nth-child(6) span::text').extract_first() else '',
        #             u'估值': tr.css('td:nth-child(7) span::text').extract_first() if tr.css(
        #                 'td:nth-child(7) span::text').extract_first() else '',
        #         }
        #         jingpin_list.append(jingpin_dict)
        #     if i < (jingpin_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_jingpin div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'竞品信息'] = jingpin_list[:]
        #
        # lawsuit_list = []
        # lawsuit_num = int(response.css('div#_container_lawsuit div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_lawsuit div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(lawsuit_num):
        #     lawsuit_response = Selector(text=driver.page_source)
        #     lawsuit_info = lawsuit_response.css('div#_container_lawsuit')
        #     for tr in lawsuit_info.css('table.table tbody tr'):
        #         lawsuit_dict = {
        #             u'日期': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'裁判文书': tr.css('td:nth-child(2) a::text').extract_first() if tr.css(
        #                 'td:nth-child(2) a::text').extract_first() else '',
        #             u'案由': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'案件身份': tr.css('td:nth-child(4) div::text').extract_first() if tr.css(
        #                 'td:nth-child(4) div::text').extract_first() else '',
        #             u'案件号': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #                 'td:nth-child(5) span::text').extract_first() else '',
        #         }
        #         lawsuit_list.append(lawsuit_dict)
        #     if i < (lawsuit_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_lawsuit div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'法律诉讼'] = lawsuit_list[:]
        #
        # court_list = []
        # court_num = int(response.css('div#_container_court div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_court div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(court_num):
        #     court_response = Selector(text=driver.page_source)
        #     court_info = court_response.css('div#_container_court')
        #     for tr in court_info.css('table.table tbody tr'):
        #         court_dict = {
        #             u'公告时间': tr.css('td:nth-child(1)::text').extract_first() if tr.css(
        #                 'td:nth-child(1)::text').extract_first() else '',
        #             u'上诉方': tr.css('td:nth-child(2) span').xpath('string(.)').extract_first() if tr.css(
        #                 'td:nth-child(2) span').xpath('string(.)').extract_first() else '',
        #             u'被诉方': tr.css('td:nth-child(3) span').xpath('string(.)').extract_first() if tr.css(
        #                 'td:nth-child(3) span').xpath('string(.)').extract_first() else '',
        #             u'公告类型': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #                 'td:nth-child(4) span::text').extract_first() else '',
        #             u'法院': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #                 'td:nth-child(5) span::text').extract_first() else '',
        #         }
        #         court_list.append(court_dict)
        #     if i < (court_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_court div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'法院公告'] = court_list[:]
        #
        # zhixing_list = []
        # zhixing_num = int(response.css('div#_container_zhixing div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_zhixing div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(zhixing_num):
        #     zhixing_response = Selector(text=driver.page_source)
        #     zhixing_info = zhixing_response.css('div#_container_zhixing')
        #     for tr in zhixing_info.css('table.table tbody tr'):
        #         zhixing_dict = {
        #             u'立案日期': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'执行标的': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'案号': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'执行法院': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #                 'td:nth-child(4) span::text').extract_first() else '',
        #         }
        #         zhixing_list.append(zhixing_dict)
        #     if i < (zhixing_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_zhixing div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'被执行人'] = zhixing_list[:]
        #
        # announcementcourt_list = []
        # announcementcourt_num = int(response.css('div#_container_announcementcourt div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_announcementcourt div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(announcementcourt_num):
        #     announcementcourt_response = Selector(text=driver.page_source)
        #     announcementcourt_info = response.css('div#_container_announcementcourt')
        #     for tr in announcementcourt_info.css('table.table tbody tr'):
        #         announcementcourt_dict = {
        #             u'开庭日期': tr.css('td:nth-child(1)::text').extract_first() if tr.css(
        #                 'td:nth-child(1)::text').extract_first() else '',
        #             u'案由': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'原告/上诉人': tr.css('td:nth-child(3) div').xpath('string(.)').extract_first() if tr.css(
        #                 'td:nth-child(3) div').xpath('string(.)').extract_first() else '',
        #             u'被告/被上诉人': tr.css('td:nth-child(4) div').xpath('string(.)').extract_first() if tr.css(
        #                 'td:nth-child(4) div').xpath('string(.)').extract_first() else '',
        #         }
        #         announcementcourt_list.append(announcementcourt_dict)
        #     if i < (announcementcourt_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_announcementcourt div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'开庭公告'] = announcementcourt_list[:]
        #
        # punish_list = []
        # punish_num = int(response.css('div#_container_punish div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_punish div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(punish_num):
        #     punish_response = Selector(text=driver.page_source)
        #     punish_info = punish_response.css('div#_container_punish')
        #     for tr in punish_info.css('table.table tbody tr'):
        #         punish_dict = {
        #             u'决定日期': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'决定书文号': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'类型': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'决定机关': tr.css('td:nth-child(4) div').xpath('string(.)').extract_first() if tr.css(
        #                 'td:nth-child(4) div').xpath('string(.)').extract_first() else ''
        #         }
        #         punish_list.append(punish_dict)
        #     if i < (punish_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_punish div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'行政处罚'] = punish_list[:]
        #
        # equity_list = []
        # equity_num = int(response.css('div#_container_equity div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_equity div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(equity_num):
        #     equity_response = Selector(text=driver.page_source)
        #     equity_info = equity_response.css('div#_container_equity')
        #     for tr in equity_info.css('table.table tbody tr'):
        #         equity_dict = {
        #             u'公告时间': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'登记编号': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'出质人': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'质权人': tr.css('td:nth-child(4) span').xpath('string(.)').extract_first() if tr.css(
        #                 'td:nth-child(4) span').xpath('string(.)').extract_first() else '',
        #             u'状态': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #                 'td:nth-child(5) span::text').extract_first() else '',
        #         }
        #         equity_list.append(equity_dict)
        #     if i < (equity_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_equity div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'股权出质'] = equity_list[:]
        #
        # bid_list = []
        # bid_num = int(response.css('div#_container_bid div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_bid div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(bid_num):
        #     bid_response = Selector(text=driver.page_source)
        #     bid_info = bid_response.css('div#_container_bid')
        #     for tr in bid_info.css('table.table tbody tr'):
        #         bid_dict = {
        #             u'发布时间': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'标题': tr.css('td:nth-child(2) a::text').extract_first() if tr.css(
        #                 'td:nth-child(2) a::text').extract_first() else '',
        #             u'采购人': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #         }
        #         bid_list.append(bid_dict)
        #     if i < (bid_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_bid div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'招投标'] = bid_list[:]
        #
        # recruit_list = []
        # recruit_num = int(response.css('div#_container_recruit div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_recruit div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(recruit_num):
        #     recruit_response = Selector(text=driver.page_source)
        #     recruit_info = recruit_response.css('div#_container_recruit')
        #     for tr in recruit_info.css('table.table tbody tr'):
        #         recruit_dict = {
        #             u'发布时间': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'招聘职位': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'薪资': tr.css('td:nth-child(3)::text').extract_first() if tr.css(
        #                 'td:nth-child(3)::text').extract_first() else '',
        #             u'工作经验': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #                 'td:nth-child(4) span::text').extract_first() else '',
        #             u'招聘人数': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #                 'td:nth-child(5) span::text').extract_first() else '',
        #             u'所在城市': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #                 'td:nth-child(6) span::text').extract_first() else '',
        #         }
        #         recruit_list.append(recruit_dict)
        #     if i < (recruit_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_recruit div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'招聘'] = recruit_list[:]
        #
        # taxcredit_list = []
        # taxcredit_num = int(response.css('div#_container_taxcredit div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_taxcredit div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(taxcredit_num):
        #     taxcredit_response = Selector(text=driver.page_source)
        #     taxcredit_info = taxcredit_response.css('div#_container_taxcredit')
        #     for tr in taxcredit_info.css('table.table tbody tr'):
        #         taxcredit_dict = {
        #             u'年份': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'纳税评级': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'类型': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'纳税人识别号': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #                 'td:nth-child(4) span::text').extract_first() else '',
        #             u'评价单位': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #                 'td:nth-child(5) span::text').extract_first() else '',
        #         }
        #         taxcredit_list.append(taxcredit_dict)
        #     if i < (taxcredit_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_taxcredit div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'税务评级'] = taxcredit_list[:]
        #
        # check_list = []
        # check_num = int(response.css('div#_container_check div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_check div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(check_num):
        #     check_response = Selector(text=driver.page_source)
        #     check_info = check_response.css('div#_container_check')
        #     for tr in check_info.css('table.table tbody tr'):
        #         check_dict = {
        #             u'日期': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'类型': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'结果': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'检查实施机关': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #                 'td:nth-child(4) span::text').extract_first() else '',
        #         }
        #         check_list.append(check_dict)
        #     if i < (check_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_check div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'抽查检查'] = check_list[:]
        #
        # product_info_list = []
        # product_info_num = int(response.css('div#_container_product div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_product div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(product_info_num):
        #     product_info_response = Selector(text=driver.page_source)
        #     product_info_info = product_info_response.css('div#_container_product')
        #     for tr in product_info_info.css('table.table tbody tr'):
        #         product_info_dict = {
        #             u'图标': tr.css('td:nth-child(1) img::attr(src)').extract_first() if tr.css(
        #                 'td:nth-child(1) img::attr(src)').extract_first() else '',
        #             u'产品名称': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'产品简称': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'产品分类': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #                 'td:nth-child(4) span::text').extract_first() else '',
        #             u'领域': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #                 'td:nth-child(5) span::text').extract_first() else '',
        #         }
        #         product_info_list.append(product_info_dict)
        #     if i < (product_info_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_product div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'产品信息'] = product_info_list[:]
        #
        # certificate_list = []
        # certificate_num = int(response.css('div#_container_certificate div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_certificate div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(certificate_num):
        #     certificate_response = Selector(text=driver.page_source)
        #     certificate_info = certificate_response.css('div#_container_certificate')
        #     for tr in certificate_info.css('table.table tbody tr'):
        #         certificate_dict = {
        #             u'证书类型': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'证书编号': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'发证日期': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'截止日期': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #                 'td:nth-child(4) span::text').extract_first() else '',
        #         }
        #         certificate_list.append(certificate_dict)
        #     if i < (certificate_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_certificate div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'资质证书'] = certificate_list[:]
        #
        # wechat_list = []
        # wechat_num = int(response.css('div#_container_wechat div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_wechat div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(wechat_num):
        #     wechat_response = Selector(text=driver.page_source)
        #     wechat_info = wechat_response.css('div#_container_wechat')
        #     for tr in wechat_info.css('div.wechat div.mb10'):
        #         wechat_dict = {
        #             u'图标': tr.css('div.wechatImg img::attr(src)').extract_first() if tr.css(
        #                 'div.wechatImg img::attr(src)').extract_first() else '',
        #             u'名称': tr.css('div.itemRight div.mb5:nth-child(1)::text').extract_first() if tr.css(
        #                 'div.itemRight div.mb5:nth-child(1)::text').extract_first() else '',
        #             u'微信号': tr.css('div.itemRight div.mb5:nth-child(2) span:nth-child(2)::text').extract_first() if tr.css(
        #                 'div.itemRight div.mb5:nth-child(2) span:nth-child(2)::text').extract_first() else '',
        #             u'功能介绍': tr.css('div.itemRight div:nth-child(3) span:nth-child(2)::text').extract_first() if tr.css(
        #                 'div.itemRight div:nth-child(3) span:nth-child(2)::text').extract_first() else '',
        #         }
        #         wechat_list.append(wechat_dict)
        #     if i < (wechat_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_wechat div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'微信公众号信息'] = wechat_list[:]
        #
        # tmInfo_list = []
        # tmInfo_num = int(response.css('div#_container_tmInfo div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_tmInfo div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(tmInfo_num):
        #     tmInfo_response = Selector(text=driver.page_source)
        #     tmInfo_info = tmInfo_response.css('div#_container_tmInfo')
        #     for tr in tmInfo_info.css('table.table tbody tr'):
        #         tmInfo_dict = {
        #             u'申请日期': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'商标': tr.css('td:nth-child(2) img::attr(src)').extract_first() if tr.css(
        #                 'td:nth-child(2) img::attr(src)').extract_first() else '',
        #             u'商标名称': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'注册号': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #                 'td:nth-child(4) span::text').extract_first() else '',
        #             u'类别': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #                 'td:nth-child(5) span::text').extract_first() else '',
        #             u'流程状态': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #                 'td:nth-child(6) span::text').extract_first() else '',
        #         }
        #         tmInfo_list.append(tmInfo_dict)
        #     if i < (tmInfo_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_tmInfo div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'商标信息'] = tmInfo_list[:]
        #
        # patent_list = []
        # patent_num = int(response.css('div#_container_patent div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_patent div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(patent_num):
        #     patent_response = Selector(text=driver.page_source)
        #     patent_info = patent_response.css('div#_container_patent')
        #     for tr in patent_info.css('table.table tbody tr'):
        #         patent_dict = {
        #             u'申请公布日': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'专利名称': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'申请号': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'申请公布号': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #                 'td:nth-child(4) span::text').extract_first() else '',
        #         }
        #         patent_list.append(patent_dict)
        #     if i < (patent_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_patent div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'专利信息'] = patent_list[:]
        #
        # copyright_list = []
        # copyright_num = int(response.css('div#_container_copyright div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_copyright div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(copyright_num):
        #     copyright_response = Selector(text=driver.page_source)
        #     copyright_info = copyright_response.css('div#_container_copyright')
        #     for tr in copyright_info.css('table.table tbody tr'):
        #         copyright_dict = {
        #             u'批准日期': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'软件全称': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'软件简称': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'登记号': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #                 'td:nth-child(4) span::text').extract_first() else '',
        #             u'分类号': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #                 'td:nth-child(5) span::text').extract_first() else '',
        #             u'版本号': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #                 'td:nth-child(6) span::text').extract_first() else '',
        #         }
        #         copyright_list.append(copyright_dict)
        #     if i < (copyright_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_copyright div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'软件著作权'] = copyright_list[:]
        #
        # copyrightWorks_list = []
        # copyrightWorks_num = int(response.css('div#_container_copyrightWorks div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_copyrightWorks div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(copyrightWorks_num):
        #     copyrightWorks_response = Selector(text=driver.page_source)
        #     copyrightWorks_info = copyrightWorks_response.css('div#_container_copyrightWorks')
        #     for tr in copyrightWorks_info.css('table.table tbody tr'):
        #         copyrightWorks_dict = {
        #             u'作品名称': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'登记号': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'类别': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #                 'td:nth-child(3) span::text').extract_first() else '',
        #             u'创作完成日期': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #                 'td:nth-child(4) span::text').extract_first() else '',
        #             u'登记日期': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #                 'td:nth-child(5) span::text').extract_first() else '',
        #             u'首次发布日期': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #                 'td:nth-child(6) span::text').extract_first() else '',
        #         }
        #         copyrightWorks_list.append(copyrightWorks_dict)
        #     if i < (copyrightWorks_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_copyrightWorks div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'作品著作权'] = copyrightWorks_list[:]
        #
        # icp_list = []
        # icp_num = int(response.css('div#_container_icp div.company_pager div.total').re('[\d]+')[0] if response.css('div#_container_icp div.company_pager div.total').re('[\d]+') else 1)
        # for i in range(icp_num):
        #     icp_response = Selector(text=driver.page_source)
        #     icp_info = icp_response.css('div#_container_icp')
        #     for tr in icp_info.css('table.table tbody tr'):
        #         icp_dict = {
        #             u'审核时间': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #                 'td:nth-child(1) span::text').extract_first() else '',
        #             u'网站名称': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #                 'td:nth-child(2) span::text').extract_first() else '',
        #             u'网站首页': tr.css('td:nth-child(3) a::attr(href)').extract_first() if tr.css(
        #                 'td:nth-child(3) a::attr(href)').extract_first() else '',
        #             u'域名': tr.css('td:nth-child(4)::text').extract_first() if tr.css(
        #                 'td:nth-child(4)::text').extract_first() else '',
        #             u'备案号': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #                 'td:nth-child(5) span::text').extract_first() else '',
        #             u'状态': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #                 'td:nth-child(6) span::text').extract_first() else '',
        #             u'单位性质': tr.css('td:nth-child(7) span::text').extract_first() if tr.css(
        #                 'td:nth-child(7) span::text').extract_first() else '',
        #         }
        #         icp_list.append(icp_dict)
        #     if i < (icp_num - 1):
        #         driver.find_element_by_css_selector(
        #             'div#_container_icp div.company_pager li.pagination-next a').click()
        #         time.sleep(10)
        # item[u'网站备案'] = icp_list[:]

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

