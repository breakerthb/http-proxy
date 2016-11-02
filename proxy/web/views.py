# -*- coding: UTF-8 -*-  

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import os
import re
import uuid
import urllib, urllib2

import logging
logger = logging.getLogger("django") # 为loggers中定义的名称

from HtmlPage import HtmlPage
from Filters import *

# Create your views here.
def global_setting(request):
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    
    return locals()
    
def home(request):
    return render(request, "home.html")
    
    
    
def search(request):
    url = request.GET['weburl']
    
    content = getContent(url)
    
    return HttpResponse(content)
    
def page(request, url):
    print(url)
    content = getContent(url)
    
    return HttpResponse(content)
    
def getContent(url):
    logger.info("\n\n---- ---- ---- ---- ---- New Post ---- ---- ----- ---- ---- ----")
    logger.info("URL : %s" % url)
    logger.info("----------------------------------------------------------------")
    
    filters = FilterChain()
    
    if filters.getFilterCnt() <= 0 :
        filters.addFilter(PicFilter())
        filters.addFilter(CSS_JSFilter())
        filters.addFilter(LinkFilter())
    
    html = HtmlPage(url)
    
    content = filters.doFilts(html.getContent())
    
    logger.info("---- ---- ---- ---- ---- Request End ---- ---- ---- ----- ----\n\n")
    
    return content