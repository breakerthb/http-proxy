# -*- coding: UTF-8 -*-  

import re
import urllib, urllib2
import uuid
import os

from django.conf import settings

class Filter:
    name = ""
    
    def __init__(self):
        self.name = "The base filter"
        
    def doFilt(self, content):
        return content
        
class FilterChain(Filter):
    filters = []
    
    def addFilter(self, f):
        self.filters.append(f)
        
    def getFilterCnt(self):
        return len(self.filters)
        
    def doFilts(self, content):
        for f in self.filters:
            print("---- ---- ---- ---- %s ---- ---- ---- ----" % f.name)
            content = f.doFilt(content)
            print("---- ---- ---- %s END ---- ---- ---- ----" % f.name)
        return content
        
class PicFilter(Filter):
    def __init__(self):
        self.name = "Pic Filter"
        
    def doFilt(self, content):
        
        if( len(content) != 0 ):  
            pattern = re.compile(r'<img[^>]*src[=\"\']+([^\"\']*)[\"\'][^>]*>', re.I) 
            pattern = re.compile(pattern)  
            lst = pattern.findall(content)
            
            for url in lst:
                print(lst)
                newName = GetPicPath(url)
                getAndSaveFile(url, newName)

                newPath = "/uploads/" + newName
                
                content = content.replace(url, newPath)
                
        return content
        
class CSSFilter(Filter):
    def __init__(self):
        self.name = "CSS Filter"
        
    def doFilt(self, content):
        if( len(content) != 0 ):  
            pattern = r'http://.{0,500}\.css'  
            pattern = re.compile(pattern)  
            lst = pattern.findall(content)
            
            #print(lst)
            
            for url in lst:
                newFileName = url.split(".")[-2].replace('/', 'a') + ".css"
                getAndSaveFile(url, newFileName)
                
                newPath = "/uploads/" + newFileName
                
                content = content.replace(url, newPath)
        
        return content
        
class JSFilter(Filter):
    def __init__(self):
        self.name = "JS Filter"
        
    def doFilt(self, content):
        if( len(content) != 0 ):  
            pattern = r'http://.{0,500}\.js'  
            pattern = re.compile(pattern)  
            lst = pattern.findall(content)
            
            print(lst)
            
            for url in lst:
                print(url)
                newFileName = url.split(".")[-2].replace('/', 'a') + ".js"
                
                if getAndSaveFile(url, newFileName):
                    newPath = "/uploads/" + newFileName
                    #print("--->")
                    content = content.replace(url, newFileName)
                    #print("<---")
                    
        return content
        
def GetPicPath(url):
    print("save url:%s" % url)

    newFileName = url.split('?')[0]

    # print(newFileName)

    lstName = newFileName.split('.')

    newFileName = lstName[-2].replace('/', 'a') + "." + lstName[-1]
    
    print("new file : %s" % newFileName)  
    
    return newFileName

def getAndSaveFile(fileURL, filename):
    print("%s 2 %s" % (fileURL, filename))
    
    try:
        request = urllib2.Request(fileURL)
        data = urllib2.urlopen(request).read()
    except urllib2.HTTPError, e:
        print("Get URL page error!")
        print(e)
        return False
        
    file_path = os.path.join(settings.UPLOADS_PATH, filename)
    
    #print("--->" + file_path)
    
    if os.path.isfile(file_path):
        print("----> file exist : %s" % file_path)
    else:
        try:
            with open(file_path, 'wb+') as f:
                #print("open: " + file_path)
                f.write(data)
        except:
            print("%s file open failed" % file_path)
        
    return True
        
        
#生成一个文件名字符串   
def generateFileName():
    string = str(uuid.uuid1())
    string = string.replace('-', 'x')
    return string