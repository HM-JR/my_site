# -*- coding: utf-8 -*-

import requests
from article.models import Article
from article.constants import BlogStatus, DOMAIN
from celery import shared_task
from utils.libs.logger.syslogger import SysLogger


@shared_task
def submit_urls_to_baidu():
    articles = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by('-id')
    urls = [DOMAIN + article.get_absolute_url() for article in articles]
    api = 'http://data.zz.baidu.com/urls?site=yangsihan.com&token=7tNlHmCq6GVPoYfb'
    response = requests.post(api, data='\n'.join(urls))
    SysLogger.info(response.content.decode())
    print (response.content.decode())
