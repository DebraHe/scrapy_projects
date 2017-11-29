# -*- coding: utf-8 -*-
import scrapy
from tianyancha.items import TianyanchaDetailItem

_META_VERSION = 'v1.0'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class TycDetailSpider(scrapy.Spider):
    name = "tyc_detail"
    result_dir = './result'
    meta_version = _META_VERSION
    driver = None
    flag = False
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'ITEM_PIPELINES': {
            'tianyancha.pipelines.TianyanchaDetailPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'tianyancha.webdriver_middleware.TycLoginMiddleware': 530,
            'tianyancha.webdriver_middleware.TycDetailMiddleware': 543,
            'tianyancha.middlewares.AbuyunProxyMiddleware': 100,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        yield scrapy.Request('https://www.tianyancha.com/login', callback=self.parse_login, meta={'login': True})

    def parse_login(self, response):
        with open('doc/detail_fail.txt') as f:
            fail = list(set([i.strip() for i in f.readlines()]))
        with open('doc/detail_done.txt') as f:
            done = list(set([i.strip() for i in f.readlines()]))
        with open('doc/detail_url.txt') as f:
            urls = list(set([i.strip() for i in f.readlines()]))
        todo = [i for i in urls if i not in done+fail]
        print len(todo)
        for idx, url in enumerate(todo):
            yield scrapy.Request(url)

    def parse(self, response):
        if len(response.text) == 0:
            print response.url
            return
        item = TianyanchaDetailItem()
        item['source_url'] = response.url
        item['name'] = response.xpath('//div[@class="company_header_width ie9Style"]/div[1]/span[1]//text()').extract_first()
        item['phone'] = response.xpath('//div[@class="f14 sec-c2 mt10"]/div[1]/span[2]//text()').extract_first()
        item['email'] = response.xpath('//div[@class="f14 sec-c2 mt10"]/div[2]/span[2]//text()').extract_first()
        item['website'] = response.xpath('//div[@class="f14 sec-c2"]/div[1]/a//text()').extract_first()
        item['addr'] = response.xpath('//div[@class="f14 sec-c2"]/div[2]/span[2]//text()').extract_first()
        item['reg_id'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[1]/td[2]//text()').extract_first()
        item['org_id'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[1]/td[4]//text()').extract_first()
        item['credit_id'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[2]/td[2]//text()').extract_first()
        item['company_type'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[2]/td[4]//text()').extract_first()
        item['taxpayer_id'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[3]/td[2]//text()').extract_first()
        item['industry'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[3]/td[4]//text()').extract_first()
        item['expiry'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[4]/td[2]//text()').extract_first()
        item['check_date'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[4]/td[4]//text()').extract_first()
        item['reg_org'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[5]/td[2]//text()').extract_first()
        item['reg_addr'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[6]/td[2]//text()').extract_first()
        item['scope'] = ''
        if response.xpath(
                '//div[@class="base0910"]/table/tbody/tr[7]//span[@class="js-full-container hidden"]//text()').extract_first():
            item['scope'] = response.xpath(
                '//div[@class="base0910"]/table/tbody/tr[7]//span[@class="js-full-container hidden"]//text()').extract_first().replace(
                u'...', '')
        elif response.xpath(
                '//div[@class="base0910"]/table/tbody/tr[7]//span[@class="js-split-container hidden"]//text()').extract_first():
            item['scope'] = response.xpath(
                '//div[@class="base0910"]/table/tbody/tr[7]//span[@class="js-split-container hidden"]//text()').extract_first().replace(
                u'...', '')


        item['score'] = response.xpath('//div[@class="base0910"]/table/tbody/tr[1]/td[5]/img/@alt').extract_first()

        staff_list = []
        for staff in response.css('div#_container_staff div.staffinfo-module-container'):
            staff_dict = {
                u'职务': staff.css('span::text').extract_first() if staff.css('span::text').extract_first() else '',
                u'姓名': staff.css('a.overflow-width::text').extract_first() if staff.css(
                    'a.overflow-width::text').extract_first() else '',
            }
            staff_list.append(staff_dict)

        invest_list = []
        for tr in response.css('div#_container_invest table.table tbody tr'):
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

        gudong_info = response.css('div#_container_holder table.table')
        gudong_list = []
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

        # biangeng_info = response.css('div#_container_changeinfo table.table')
        # biangeng_list = []
        # for tr in biangeng_info.css('tbody tr'):
        #     biangeng_dict = {
        #         u'变更时间': tr.css('td:nth-child(1) div::text').extract_first() if tr.css(
        #             'td:nth-child(1) div::text').extract_first() else '',
        #         u'变更项目': tr.css('td:nth-child(2) div::text').extract_first() if tr.css(
        #             'td:nth-child(2) div::text').extract_first() else '',
        #         u'变更前': tr.css('td:nth-child(3) div.changeHoverText').xpath('string(.)').extract_first() if tr.css(
        #             'td:nth-child(3) div.changeHoverText').xpath('string(.)').extract_first() else '',
        #         u'变更后': tr.css('td:nth-child(4) div.changeHoverText').xpath('string(.)').extract_first() if tr.css(
        #             'td:nth-child(3) div.changeHoverText').xpath('string(.)').extract_first() else '',
        #     }
        #     biangeng_list.append(biangeng_dict)
        #
        # rongzi_info = response.css('div#_container_rongzi table.table')
        # rongzi_list = []
        # for tr in rongzi_info.css('tbody tr'):
        #     rongzi_dict = {
        #         u'时间': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'轮次': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'估值': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'金额': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #             'td:nth-child(4) span::text').extract_first() else '',
        #         u'比例': tr.css('td:nth-child(5) span a.text-dark-color::text').extract_first() if tr.css(
        #             'td:nth-child(5) span a.text-dark-color::text').extract_first() else '',
        #         u'投资方': tr.css('td:nth-child(6) span a.text-dark-color::text').extract() if tr.css(
        #             'td:nth-child(6) span a.text-dark-color::text').extract() else [],
        #         u'新闻来源': tr.css('td:nth-child(7) span a.text-dark-color::text').extract_first() if tr.css(
        #             'td:nth-child(7) span a.text-dark-color::text').extract_first() else '',
        #     }
        #     rongzi_list.append(rongzi_dict)
        #
        # team_member_info = response.css('div#_container_teamMember')
        # team_member_list = []
        # for tr in team_member_info.css('div.team-item'):
        #     team_member_dict = {
        #         u'姓名': tr.css('div.team-left div.team-name::text').extract_first() if tr.css(
        #             'div.team-left div.team-name::text').extract_first() else '',
        #         u'头像': tr.css('div.team-left div.img-outer img::attr(src)').extract_first() if tr.css(
        #             'div.team-left div.img-outer img::attr(src)').extract_first() else '',
        #         u'职位': tr.css('div.team-right div.team-title::text').extract_first() if tr.css(
        #             'div.team-right div.team-title::text').extract_first() else '',
        #         u'简介': ' '.join(tr.css('div.team-right ul span::text').extract()) if ' '.join(
        #             tr.css('div.team-right ul span::text').extract()) else '',
        #     }
        #     team_member_list.append(team_member_dict)
        #
        # firmProduct_info = response.css('div#_container_firmProduct')
        # firmProduct_list = []
        # for tr in firmProduct_info.css('div.product-item'):
        #     firmProduct_dict = {
        #         u'名称': tr.css('div.product-right span.title::text').extract_first() if tr.css(
        #             'div.product-right span.title::text').extract_first() else '',
        #         u'图标': tr.css('div.product-left img::attr(src)').extract_first() if tr.css(
        #             'div.product-left img::attr(src)').extract_first() else '',
        #         u'行业': tr.css('div.product-right div.hangye::text').extract_first() if tr.css(
        #             'div.product-right div.hangye::text').extract_first() else '',
        #         u'简介': ' '.join(tr.css('div.product-right div.yeweu::text').extract()) if ' '.join(
        #             tr.css('div.product-right div.yeweu::text').extract()) else '',
        #     }
        #     firmProduct_list.append(firmProduct_dict)
        #
        # touzi_event_info = response.css('div#_container_touzi')
        # touzi_event_list = []
        # for tr in touzi_event_info.css('table.table tbody tr'):
        #     touzi_event_dict = {
        #         u'时间': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'轮次': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'金额': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'投资方': tr.css('td:nth-child(4) a::text').extract() if tr.css(
        #             'td:nth-child(4) a::text').extract() else [],
        #         u'产品': tr.css('td:nth-child(5) a::text').extract_first() if tr.css(
        #             'td:nth-child(5) a::text').extract_first() else '',
        #         u'地区': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #             'td:nth-child(6) span::text').extract_first() else '',
        #         u'行业': tr.css('td:nth-child(7) span::text').extract_first() if tr.css(
        #             'td:nth-child(7) span::text').extract_first() else '',
        #         u'业务': tr.css('td:nth-child(8) span::text').extract_first() if tr.css(
        #             'td:nth-child(8) span::text').extract_first() else '',
        #     }
        #     touzi_event_list.append(touzi_event_dict)
        #
        # lawsuit_info = response.css('div#_container_lawsuit')
        # lawsuit_list = []
        # for tr in lawsuit_info.css('table.table tbody tr'):
        #     lawsuit_dict = {
        #         u'日期': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'裁判文书': tr.css('td:nth-child(2) a::text').extract_first() if tr.css(
        #             'td:nth-child(2) a::text').extract_first() else '',
        #         u'案由': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'案件身份': tr.css('td:nth-child(4) div::text').extract_first() if tr.css(
        #             'td:nth-child(4) div::text').extract_first() else '',
        #         u'案件号': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #             'td:nth-child(5) span::text').extract_first() else '',
        #     }
        #     lawsuit_list.append(lawsuit_dict)
        #
        # jingpin_info = response.css('div#_container_jingpin')
        # jingpin_list = []
        # for tr in jingpin_info.css('table.table tbody tr'):
        #     jingpin_dict = {
        #         u'产品': tr.css('td:nth-child(1) a::text').extract_first() if tr.css(
        #             'td:nth-child(1) a::text').extract_first() else '',
        #         u'地区': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'当前轮次': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'行业': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #             'td:nth-child(4) span::text').extract_first() else '',
        #         u'业务': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #             'td:nth-child(5) span::text').extract_first() else '',
        #         u'成立时间': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #             'td:nth-child(6) span::text').extract_first() else '',
        #         u'估值': tr.css('td:nth-child(7) span::text').extract_first() if tr.css(
        #             'td:nth-child(7) span::text').extract_first() else '',
        #     }
        #     jingpin_list.append(jingpin_dict)
        #
        # court_info = response.css('div#_container_court')
        # court_list = []
        # for tr in court_info.css('table.table tbody tr'):
        #     court_dict = {
        #         u'公告时间': tr.css('td:nth-child(1)::text').extract_first() if tr.css(
        #             'td:nth-child(1)::text').extract_first() else '',
        #         u'上诉方': tr.css('td:nth-child(2) span').xpath('string(.)').extract_first() if tr.css(
        #             'td:nth-child(2) span').xpath('string(.)').extract_first() else '',
        #         u'被诉方': tr.css('td:nth-child(3) span').xpath('string(.)').extract_first() if tr.css(
        #             'td:nth-child(3) span').xpath('string(.)').extract_first() else '',
        #         u'公告类型': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #             'td:nth-child(4) span::text').extract_first() else '',
        #         u'法院': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #             'td:nth-child(5) span::text').extract_first() else '',
        #     }
        #     court_list.append(court_dict)
        #
        # zhixing_info = response.css('div#_container_zhixing')
        # zhixing_list = []
        # for tr in zhixing_info.css('table.table tbody tr'):
        #     zhixing_dict = {
        #         u'立案日期': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'执行标的': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'案号': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'执行法院': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #             'td:nth-child(4) span::text').extract_first() else '',
        #     }
        #     zhixing_list.append(zhixing_dict)
        #
        # announcementcourt_info = response.css('div#_container_announcementcourt')
        # announcementcourt_list = []
        # for tr in announcementcourt_info.css('table.table tbody tr'):
        #     announcementcourt_dict = {
        #         u'开庭日期': tr.css('td:nth-child(1)::text').extract_first() if tr.css(
        #             'td:nth-child(1)::text').extract_first() else '',
        #         u'案由': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'原告/上诉人': tr.css('td:nth-child(3) div').xpath('string(.)').extract_first() if tr.css(
        #             'td:nth-child(3) div').xpath('string(.)').extract_first() else '',
        #         u'被告/被上诉人': tr.css('td:nth-child(4) div').xpath('string(.)').extract_first() if tr.css(
        #             'td:nth-child(4) div').xpath('string(.)').extract_first() else '',
        #     }
        #     announcementcourt_list.append(announcementcourt_dict)
        #
        # equity_info = response.css('div#_container_equity')
        # equity_list = []
        # for tr in equity_info.css('table.table tbody tr'):
        #     equity_dict = {
        #         u'公告时间': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'登记编号': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'出质人': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'质权人': tr.css('td:nth-child(4) span').xpath('string(.)').extract_first() if tr.css(
        #             'td:nth-child(4) span').xpath('string(.)').extract_first() else '',
        #         u'状态': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #             'td:nth-child(5) span::text').extract_first() else '',
        #     }
        #     equity_list.append(equity_dict)
        #
        # bid_info = response.css('div#_container_bid')
        # bid_list = []
        # for tr in bid_info.css('table.table tbody tr'):
        #     bid_dict = {
        #         u'发布时间': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'标题': tr.css('td:nth-child(2) a::text').extract_first() if tr.css(
        #             'td:nth-child(2) a::text').extract_first() else '',
        #         u'采购人': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #     }
        #     bid_list.append(bid_dict)
        #
        # recruit_info = response.css('div#_container_recruit')
        # recruit_list = []
        # for tr in recruit_info.css('table.table tbody tr'):
        #     recruit_dict = {
        #         u'发布时间': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'招聘职位': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'薪资': tr.css('td:nth-child(3)::text').extract_first() if tr.css(
        #             'td:nth-child(3)::text').extract_first() else '',
        #         u'工作经验': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #             'td:nth-child(4) span::text').extract_first() else '',
        #         u'招聘人数': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #             'td:nth-child(5) span::text').extract_first() else '',
        #         u'所在城市': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #             'td:nth-child(6) span::text').extract_first() else '',
        #     }
        #     recruit_list.append(recruit_dict)
        #
        # taxcredit_info = response.css('div#_container_taxcredit')
        # taxcredit_list = []
        # for tr in taxcredit_info.css('table.table tbody tr'):
        #     taxcredit_dict = {
        #         u'年份': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'纳税评级': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'类型': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'纳税人识别号': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #             'td:nth-child(4) span::text').extract_first() else '',
        #         u'评价单位': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #             'td:nth-child(5) span::text').extract_first() else '',
        #     }
        #     taxcredit_list.append(taxcredit_dict)
        #
        # check_info = response.css('div#_container_check')
        # check_list = []
        # for tr in check_info.css('table.table tbody tr'):
        #     check_dict = {
        #         u'日期': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'类型': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'结果': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'检查实施机关': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #             'td:nth-child(4) span::text').extract_first() else '',
        #     }
        #     check_list.append(check_dict)
        #
        # product_info_info = response.css('div#_container_product')
        # product_info_list = []
        # for tr in product_info_info.css('table.table tbody tr'):
        #     product_info_dict = {
        #         u'图标': tr.css('td:nth-child(1) img::attr(src)').extract_first() if tr.css(
        #             'td:nth-child(1) img::attr(src)').extract_first() else '',
        #         u'产品名称': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'产品简称': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'产品分类': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #             'td:nth-child(4) span::text').extract_first() else '',
        #         u'领域': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #             'td:nth-child(5) span::text').extract_first() else '',
        #     }
        #     product_info_list.append(product_info_dict)
        #
        # certificate_info = response.css('div#_container_certificate')
        # certificate_list = []
        # for tr in certificate_info.css('table.table tbody tr'):
        #     certificate_dict = {
        #         u'证书类型': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'证书编号': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'发证日期': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'截止日期': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #             'td:nth-child(4) span::text').extract_first() else '',
        #     }
        #     certificate_list.append(certificate_dict)
        #
        # wechat_info = response.css('div#_container_wechat')
        # wechat_list = []
        # for tr in wechat_info.css('div.wechat div.mb10'):
        #     wechat_dict = {
        #         u'图标': tr.css('div.wechatImg img::attr(src)').extract_first() if tr.css(
        #             'div.wechatImg img::attr(src)').extract_first() else '',
        #         u'名称': tr.css('div.itemRight div.mb5:nth-child(1)::text').extract_first() if tr.css(
        #             'div.itemRight div.mb5:nth-child(1)::text').extract_first() else '',
        #         u'微信号': tr.css('div.itemRight div.mb5:nth-child(2) span:nth-child(2)::text').extract_first() if tr.css(
        #             'div.itemRight div.mb5:nth-child(2) span:nth-child(2)::text').extract_first() else '',
        #         u'功能介绍': tr.css('div.itemRight div:nth-child(3) span:nth-child(2)::text').extract_first() if tr.css(
        #             'div.itemRight div:nth-child(3) span:nth-child(2)::text').extract_first() else '',
        #     }
        #     wechat_list.append(wechat_dict)
        #
        # tmInfo_info = response.css('div#_container_tmInfo')
        # tmInfo_list = []
        # for tr in tmInfo_info.css('table.table tbody tr'):
        #     tmInfo_dict = {
        #         u'申请日期': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'商标': tr.css('td:nth-child(2) img::attr(src)').extract_first() if tr.css(
        #             'td:nth-child(2) img::attr(src)').extract_first() else '',
        #         u'商标名称': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'注册号': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #             'td:nth-child(4) span::text').extract_first() else '',
        #         u'类别': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #             'td:nth-child(5) span::text').extract_first() else '',
        #         u'流程状态': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #             'td:nth-child(6) span::text').extract_first() else '',
        #     }
        #     tmInfo_list.append(tmInfo_dict)
        #
        # patent_info = response.css('div#_container_patent')
        # patent_list = []
        # for tr in patent_info.css('table.table tbody tr'):
        #     patent_dict = {
        #         u'申请公布日': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'专利名称': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'申请号': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'申请公布号': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #             'td:nth-child(4) span::text').extract_first() else '',
        #     }
        #     patent_list.append(patent_dict)
        #
        # copyright_info = response.css('div#_container_copyright')
        # copyright_list = []
        # for tr in copyright_info.css('table.table tbody tr'):
        #     copyright_dict = {
        #         u'批准日期': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'软件全称': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'软件简称': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'登记号': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #             'td:nth-child(4) span::text').extract_first() else '',
        #         u'分类号': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #             'td:nth-child(5) span::text').extract_first() else '',
        #         u'版本号': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #             'td:nth-child(6) span::text').extract_first() else '',
        #     }
        #     copyright_list.append(copyright_dict)
        #
        # copyrightWorks_info = response.css('div#_container_copyrightWorks')
        # copyrightWorks_list = []
        # for tr in copyrightWorks_info.css('table.table tbody tr'):
        #     copyrightWorks_dict = {
        #         u'作品名称': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'登记号': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'类别': tr.css('td:nth-child(3) span::text').extract_first() if tr.css(
        #             'td:nth-child(3) span::text').extract_first() else '',
        #         u'创作完成日期': tr.css('td:nth-child(4) span::text').extract_first() if tr.css(
        #             'td:nth-child(4) span::text').extract_first() else '',
        #         u'登记日期': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #             'td:nth-child(5) span::text').extract_first() else '',
        #         u'首次发布日期': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #             'td:nth-child(6) span::text').extract_first() else '',
        #     }
        #     copyrightWorks_list.append(copyrightWorks_dict)
        #
        # icp_info = response.css('div#_container_icp')
        # icp_list = []
        # for tr in icp_info.css('table.table tbody tr'):
        #     icp_dict = {
        #         u'审核时间': tr.css('td:nth-child(1) span::text').extract_first() if tr.css(
        #             'td:nth-child(1) span::text').extract_first() else '',
        #         u'网站名称': tr.css('td:nth-child(2) span::text').extract_first() if tr.css(
        #             'td:nth-child(2) span::text').extract_first() else '',
        #         u'网站首页': tr.css('td:nth-child(3) a::attr(href)').extract_first() if tr.css(
        #             'td:nth-child(3) a::attr(href)').extract_first() else '',
        #         u'域名': tr.css('td:nth-child(4)::text').extract_first() if tr.css(
        #             'td:nth-child(4)::text').extract_first() else '',
        #         u'备案号': tr.css('td:nth-child(5) span::text').extract_first() if tr.css(
        #             'td:nth-child(5) span::text').extract_first() else '',
        #         u'状态': tr.css('td:nth-child(6) span::text').extract_first() if tr.css(
        #             'td:nth-child(6) span::text').extract_first() else '',
        #         u'单位性质': tr.css('td:nth-child(7) span::text').extract_first() if tr.css(
        #             'td:nth-child(7) span::text').extract_first() else '',
        #     }
        #     icp_list.append(icp_dict)

        item['staff_people'] = staff_list[:]
        item['invest'] = invest_list[:]
        item['gudong'] = gudong_list[:]
        # item['biangeng'] = biangeng_list[:]
        # item['rongzi'] = rongzi_list[:]
        # item['team_member'] = team_member_list[:]
        # item['firmProduct'] = firmProduct_list[:]
        # item['touzi_event'] = touzi_event_list[:]
        # item['lawsuit'] = lawsuit_list[:]
        # item['jingpin'] = jingpin_list[:]
        # item['court'] = court_list[:]
        # item['zhixing'] = zhixing_list[:]
        # item['announcementcourt'] = announcementcourt_list[:]
        # item['equity'] = equity_list[:]
        # item['bid'] = bid_list[:]
        # item['recruit'] = recruit_list[:]
        # item['taxcredit'] = taxcredit_list[:]
        # item['check'] = check_list[:]
        # item['product_info'] = product_info_list[:]
        # item['certificate'] = certificate_list[:]
        # item['wechat'] = wechat_list[:]
        # item['tmInfo'] = tmInfo_list[:]
        # item['patent'] = patent_list[:]
        # item['copyright'] = copyright_list[:]
        # item['copyrightWorks'] = copyrightWorks_list[:]
        # item['icp'] = icp_list[:]

        if item['score']:
            item['score'] = item['score'][2:]
        else:
            item['score'] = ''
        for i in ['source_url','name','phone','email','website','addr','reg_id','org_id','credit_id','company_type','taxpayer_id','industry','expiry','check_date','reg_org','reg_addr','scope','score']:
            if item[i] == '':
                print i, response.url
                with open('doc/detail_fail.txt','a') as f:
                    f.write(response.url+'\n')
                return
        yield item
        with open('doc/detail_done.txt','a') as f:
            f.write(response.url+'\n')
