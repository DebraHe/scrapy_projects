# -*- coding: utf-8 -*-
from scrapy.mail import MailSender

mailer = MailSender()
mailer = MailSender(smtphost='smtp.exmail.qq.com', mailfrom='crawler@ruyi.ai', smtpuser='crawler@ruyi.ai', smtppass='Shu12349', smtpport=25)
body = '快去看\nubuntu@120.132.66.115:/home/ubuntu/ruyi-scrapy/xmly/xmly_to_delete.json'
mailer.send(to=["heh@ruyi.ai"], subject="XMLY 下架资源列表", body=body)
