# -*- coding: UTF-8 -*-  

import re
import urllib, urllib2
import uuid
import os

from django.conf import settings
from HtmlPage import URL

import logging
logger = logging.getLogger("django") # 为loggers中定义的名称

class Filter:
    name = ""
    
    def __init__(self):
        self.name = "The base filter"
        
    def doFilt(self, dictURLs):
        return dictURLs
        
class FilterChain(Filter):
    filters = []
    
    def addFilter(self, f):
        self.filters.append(f)
        
    def getFilterCnt(self):
        return len(self.filters)
        
    def doFilts(self, content):
        pattern = r'http://.{0,500}\"'
        pattern = re.compile(pattern)
        lstURL = pattern.findall(content)
        
        pattern = r'href=\"/.{0,500}?\"'
        pattern = re.compile(pattern)
        lstURL1 = pattern.findall(content)
        lstURL1 = [url[6:] for url in lstURL1]

        lstURL.extend(lstURL1)
        
        dictURLs = {}
        
        logger.info("All URls:");
        for url in lstURL:
            url = url.split('\"')[0].split('&')[0]
            
            #logger.info(url)
            
            dictURLs[url] = URL(url)
        
        for f in self.filters:
            logger.info("---- ---- ---- ---- %s ---- ---- ---- ----" % f.name)
            logger.info("--->url count : %d" % len(dictURLs))
            dictURLs = f.doFilt(dictURLs)
            logger.info("--->url count : %d" % len(dictURLs))
            logger.info("---- ---- ---- %s END ---- ---- ---- ----\n" % f.name)
        
        logger.info("")
        logger.info("Source URL check:")
        logger.info("--->url count : %d" % len(dictURLs))
        for k in dictURLs.keys():
            if dictURLs[k].getNewURL() == '':
                continue
            
            url = dictURLs[k]
            
            if content.find(url.getSrcURL()) == -1:
                logger.info("not find:" + url.getSrcURL())
                
            #logger.info("replace : %s - %s" % (url.getSrcURL(), url.getNewURL()))
            content = content.replace(url.getSrcURL(), url.getNewURL())

        # path
        content = content.replace("/page?url=/page?url=", "/page?url=")
        
        #logger.info(content)
        
        return content
        
class PicFilter(Filter):
    def __init__(self):
        self.name = "Pic Filter"
        
    def doFilt(self, dictURLs):
        
        #logger.info(dictURLs.keys())
        
        for k in dictURLs.keys():
            if dictURLs[k].getNewURL() != '':
                continue
            
            url = dictURLs[k]
            
            #logger.info(str(url))
            
            ext = url.getExtName()
            if ext == 'jpg' or ext == 'png' or ext == 'gif' or ext == 'icon':
                getAndSaveFile(url.getSrcURL(), url.getNewName() + "." + url.getExtName())
                
                url.newURL = "/uploads/" + url.getNewName() + "." + url.getExtName()
                logger.info(url.srcURL + "-" + url.newURL)
                
                
                #logger.info(str(url))
                dictURLs[k] = url
                #logger.info(str(dictURLs[k]))
            else:
                pass

        return dictURLs
        
class CSS_JSFilter(Filter):
    def __init__(self):
        self.name = "CSS_JS Filter"
        
    def doFilt(self, dictURLs):
        for k in dictURLs.keys():
            if dictURLs[k].getNewURL() != '':
                continue
            
            url = dictURLs[k]
            
            ext = url.getExtName()
            
            if ext == 'css' or ext == 'js':
                getAndSaveFile(url.getSrcURL(), url.getNewName() + "." + url.getExtName())
                url.newURL = "/uploads/" + url.getNewName() + "." + url.getExtName()
                
                dictURLs[k] = url
            else:
                pass
            
        return dictURLs
        
class LinkFilter(Filter):
    def __init__(self):
        self.name = "Link Filter"
        
    def doFilt(self, dictURLs):
        for k in dictURLs.keys():
            if dictURLs[k].getNewURL() != '':
                continue
            
            url = dictURLs[k]
            
            if url.getExtName() == '' or url.getExtName() == 'shtml':
                
                #logger.info("%s | %s" % (url.getSrcURL(), url.getExtName()))
                
                #print(url.getSrcURL())
                url.newURL = "/page?url=" + url.getSrcURL()
                #url.newURL = url.newURL.replace('//', '/')

                #print(url.newURL)
                
                dictURLs[k] = url
            else:
                pass
            
        return dictURLs

def getAndSaveFile(fileURL, filename):
    #print("%s 2 %s" % (fileURL, filename))
    
    try:
        request = urllib2.Request(fileURL)
        data = urllib2.urlopen(request).read()
    except urllib2.HTTPError, e:
        logger.warning("Get URL page error! - %s" % fileURL)
        logger.warning(e)
        return False
        
    file_path = os.path.join(settings.UPLOADS_PATH, filename)
    
    if os.path.isfile(file_path):
        logger.info("file exist : %s" % file_path)
    else:
        try:
            with open(file_path, 'wb+') as f:
                #print("open: " + file_path)
                f.write(data)
        except:
            logger.warning("%s file open failed" % file_path)
        
    return True
        
        
#生成一个文件名字符串   
def generateFileName():
    string = str(uuid.uuid1())
    string = string.replace('-', 'x')
    return string