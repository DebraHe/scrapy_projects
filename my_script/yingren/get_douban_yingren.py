# -*- coding: utf-8 -*-

import json
import re

from scrapy.selector import Selector
from tool import get_uuid, drop_point_in_name
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

RESULT_FILE = 'douban_person.json'


husband = [u"前夫", u"丈夫", u"现夫", u"husband", u"亡夫", u"夫,2001已死", u"夫", u"ex-husband"]
wife = [u"前妻; 1957–85", u"妻，已去世", u"前妻; 1952–56", u"前妻; 1934–37", u"前妻; 1945–46", u"前妻; 1940", u"前妻", u"妻子", u"妻", u"前妻; 1942–43", u"wife"]
spouse = [u"前伴侣", u"伴侣", u"spouse", u"配偶", u"前夫", u"丈夫", u"现夫", u"husband", u"亡夫", u"夫,2001已死", u"夫", u"ex-husband", u"前妻; 1957–85", u"妻，已去世", u"前妻; 1952–56", u"前妻; 1934–37", u"前妻; 1945–46", u"前妻; 1940", u"前妻", u"妻子", u"妻", u"前妻; 1942–43", u"wife"]
father = [u"父亲", u"爸", u"爹", u"养父", u"爸爸", u"干爸", u"干爹", u"父"]
mother = [u"母亲", u"妈妈", u"继母"]
children = [u"娃", u"遗孀", u"儿子", u"son", u"幼子", u"前妻之子", u"次子", u"三子", u"父子", u"干儿子", u"子", u"儿", u"养子", u"长女", u"長女", u"女儿", u"daughter", u"前妻之女", u"干女儿", u"次女", u"养女", u"女"]
son = [u"儿子", u"son", u"幼子", u"前妻之子", u"次子", u"三子", u"父子", u"干儿子", u"子", u"儿", u"养子"]
daughter = [u"长女", u"長女", u"女儿", u"daughter", u"前妻之女", u"干女儿", u"次女", u"养女", u"女"]
olderBrother = [u"二哥", u"胞兄", u"长子", u"堂兄", u"兄", u"哥", u"哥哥", u"表哥"]
elderBrother = [u"胞弟", u"表弟", u"义弟", u"弟弟", u"同母异父之弟", u"二弟"]
olderSister = [u"姐", u"姐姐", u"大姐", u"二姐", u"表姐"]
elderSister = [u"妹妹", u"堂妹", u"妺", u"表妹"]
granddaughter = [u"外孙女", u"孙女", u"外甥孙女"]
grandmother = [u"祖母", u"奶", u"外祖母", u"奶奶"]
grandson = [u"外孙", u"孙子"]
grandfather = [u"外曾祖父", u"爷", u"姥爷", u"外祖父", u"祖父", u"曾祖父", u"爷爷"]
unmarriedPartner = [u"男友", u"伴侣", u"未婚妻", u"Partner", u"女友"]

with open(RESULT_FILE) as f:
    lines = f.readlines()
    for line in lines:
        try:

            mother_list = []
            father_list = []
            children_list = []
            son_list = []
            daughter_list = []
            olderBrother_list = []
            elderBrother_list = []
            olderSister_list = []
            elderSister_list = []
            granddaughter_list = []
            grandmother_list = []
            grandson_list = []
            grandfather_list = []
            spouse_list = []
            husband_list = []
            wife_list = []
            unmarriedPartner_list = []
            award_list = []
            award_hasPart_list = []
            authorOf_list = []
            authorOf_dict = {}
            birthPlace = ""
            birthDate = ""
            deathDate = ""
            constellation = ""
            gender = ""
            name = ""
            name_re_str = ""
            name_not_re_str = ""
            occupation_list = []
            alternateName_list = []

            url = json.loads(line.strip()).get(
                'download_config').get('url')
            basic_infos = json.loads(line.strip()).get(
                'download_data').get('raw_data').get('raw_info')
            award_infos = json.loads(line.strip()).get(
                'download_data').get('raw_data').get('raw_awards')

            subject_id = json.loads(line.strip()).get(
                'download_data').get('parsed_data').get('subject_id')  # 读取豆瓣ID
            image = json.loads(line.strip()).get(
                'download_data').get('parsed_data').get('pic')[0]
            description = json.loads(line.strip()).get(
                'download_data').get('parsed_data').get('description')
            partners = json.loads(line.strip()).get(
                'download_data').get('parsed_data').get('partner')  # url  pic name

            partner_list = []
            for partner in partners:
                partner_subject_id = re.search(r'([0-9]+)', partner['url'])
                partner_list.append({
                    "url": partner['url'],
                    "image": partner['pic'],
                    "name": partner['name'],
                    "@id": get_uuid(partner_subject_id.group(0)),
                    "@type": ["Person", "Thing"],
                }
                )

            name_original = json.loads(line.strip()).get(
                'download_data').get('parsed_data').get('name').strip()
            name_re = re.search(ur'[\u4e00-\u9fa5·•]+', name_original)
            name_not_re = re.search(ur'[^\u4e00-\u9fa5·•]+', name_original)
            try:
                name_re_str = name_re.group(0).strip()
                name = name_re_str
            except:
                name = name_original
            if name_not_re:
                name_not_re_str = name_not_re.group(0).strip()

            try:
                alternateName_list.append(name_original)
                alternateName_list.append(name_not_re_str)
                alternateName_list.append(drop_point_in_name(name_re_str.group(0)))
                alternateName_list.append(name.split(u'·')[-1])

            except:
                name = name_original

            if award_infos:
                for item in Selector(text=award_infos).css('div.awards'):
                    award_year = item.css('div.hd h2::text').extract_first()
                    award_name_item = item.css('ul.award li')[0].xpath('string(.)').extract_first().strip()
                    re_award_name = re.sub(ur'第[0-9]+届', '', award_name_item)
                    try:
                        award_name = re_award_name.strip()
                    except:
                        award_name = ""
                    re_award_session = re.search(ur'([0-9]+)', award_name_item)
                    try:
                        award_session = re_award_session.group(0).strip()
                    except:
                        award_session = ""

                    award_value = item.css('ul.award li')[1].xpath('string(.)').extract_first().strip()

                    if u'提名' in award_value:
                        award_hasPart_list.append({
                            'name': re.sub(ur'\(提名\)', '', award_value).strip(),
                            'label': 'nominated'
                        })
                    else:
                        award_hasPart_list.append({
                            'name': award_value.strip(),
                            'label': 'won'
                        })
                    award_list.append({
                        "name": award_name,
                        "session": award_session,
                        "byYear": award_year,
                        "hasPart": award_hasPart_list,
                    })
                    try:
                        authorOf_values = item.css('ul.award li')[2].xpath('string(.)').extract_first().strip().split(u'/')
                        for authorOf_value in authorOf_values:
                            authorOf_dict[authorOf_value.strip()] = 1
                    except:
                        pass
            authorOf_list = list(set(authorOf_dict.keys()))
            if '' in authorOf_list:
                authorOf_list.remove('')

            for item in Selector(text=basic_infos).css('div.info ul li'):
                basic_info_name = item.css('span::text').extract_first()
                basic_info_value = item.xpath('string(.)').extract_first()

                if basic_info_name == u'家庭成员':
                    for family in basic_info_value.replace(u'家庭成员:', '').strip().split(u'/'):
                        family_member = re.search(r'(.*?)\((.*?)\)', family.strip())
                        family_name = family.strip()
                        if not family_member:
                            continue
                        family_rela = family_member.group(2).strip()

                        if family_rela in spouse:
                            spouse_list.append(family_name)
                        if family_rela in children:
                            children_list.append(family_name)

                        if family_rela in mother:
                            mother_list.append(family_name)
                        elif family_rela in father:
                            father_list.append(family_name)
                        elif family_rela in son:
                            son_list.append(family_name)
                        elif family_rela in daughter:
                            daughter_list.append(family_name)
                        elif family_rela in olderBrother:
                            olderBrother_list.append(family_name)
                        elif family_rela in elderBrother:
                            elderBrother_list.append(family_name)
                        elif family_rela in olderSister:
                            olderSister_list.append(family_name)
                        elif family_rela in elderSister:
                            elderSister_list.append(family_name)
                        elif family_rela in granddaughter:
                            granddaughter_list.append(family_name)
                        elif family_rela in grandmother:
                            grandmother_list.append(family_name)
                        elif family_rela in grandson:
                            grandson_list.append(family_name)
                        elif family_rela in grandfather:
                            grandfather_list.append(family_name)
                        elif family_rela in unmarriedPartner:
                            unmarriedPartner_list.append(family_name)
                        elif family_rela in husband:
                            husband_list.append(family_name)
                        elif family_rela in wife:
                            wife_list.append(family_name)
                if basic_info_name == u'职业':
                    for occupation in basic_info_value.replace(u'职业:', '').strip().split(u'/'):
                        occupation_list.append(occupation.strip())
                if basic_info_name == u'星座':
                    constellation = basic_info_value.replace(u'星座:', '').strip()
                if basic_info_name == u'更多中文名':
                    for alternateName in basic_info_value.replace(u'更多中文名:', '').strip().split(u'/'):
                        alternateName_list.append(drop_point_in_name(alternateName))

                if basic_info_name == u'更多外文名':
                    for alternateName in basic_info_value.replace(u'更多外文名:', '').strip().split(u'/'):
                        alternateName_list.append(drop_point_in_name(alternateName))
                if basic_info_name == u'出生日期':
                    birthDate = basic_info_value.replace(u'出生日期:', '').strip()

                if basic_info_name == u'生卒日期':
                    birth_death_Date = basic_info_value.replace(u'生卒日期:', '').strip().split(u'至')
                    birthDate = birth_death_Date[0].strip()
                    deathDate = birth_death_Date[1].strip()
                if basic_info_name == u'出生地':
                    birthPlace = basic_info_value.replace(u'出生地:', '').strip()
            alternateName_list = list(set(alternateName_list))
            if '' in alternateName_list:
                alternateName_list.remove('')
            schema = {
                "statedIn": "movie.douban.com",
                "referenceUrl": url,
                "@id": get_uuid(subject_id),
                "@type": ["Person", "Thing"],
                "name": name,
                "image": image,
                "alternateName": alternateName_list,
                "description": description,
                "occupation": occupation_list,
                "birthPlace": birthPlace,
                "birthDate": birthDate,
                "deathDate": deathDate,
                "gender": gender,
                "constellation": constellation,
                "unmarriedPartner": unmarriedPartner_list,  # 情侣
                "colleague": partner_list,
                "husband": husband_list,
                "wife": wife_list,
                "spouse": spouse_list,
                "father": father_list,
                "mother": mother_list,
                "children": children_list,
                "son": son_list,
                "daughter": daughter_list,
                "olderBrother": olderBrother_list,
                "elderBrother": elderBrother_list,
                "olderSister": olderSister_list,
                "elderSister": elderSister_list,
                "grandson": grandson_list,
                "grandfather": grandfather_list,
                "award": award_list,
                "authorOf": authorOf_list

            }
            with open('{}'.format('douban_people_parsed.json'), 'a') as f:
                line = '{}\n'.format(json.dumps(schema, ensure_ascii=False))
                f.write(line)

        except:
            with open('{}'.format('notyet.json'), 'a') as f:
                f.write(line+'\n')
            print 'Json parsing error: {}'.format(line)
            continue


