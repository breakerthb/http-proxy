# -*- coding: UTF-8 -*-  

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import os
import urllib, urllib2
import re
import uuid

# Create your views here.
def global_setting(request):
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    return locals()
    
def home(request):
    return render(request, "home.html")
    
    
    
def search(request):
    url = request.GET['weburl']
    
    content = urllib2.urlopen(url).read()
    #print(content)
    content = operate(content)
    #print(content)
    return HttpResponse(content)
    
    
def operate(content):
    lst = getUrlList(content)
    
    for url in lst:
        newFileName = generateFileName()
        
        print("save url:%s" % url)
        
        getAndSaveImg(url, newFileName + ".jpg")
        
        newPath = "/uploads/" + newFileName + ".jpg/"
        
        content = content.replace(url, newPath)
        
        print("--->")
        print(url)
        print(newPath)
    return content
    
#从一个网页url中获取图片的地址，保存在一个list中返回  
def getUrlList(htmlString):  
    imUrlList = []
    if( len(htmlString) != 0 ):  
        patternString = r'http://.{0,50}\.jpg'  
        searchPattern = re.compile(patternString)  
        imgUrlList = searchPattern.findall(htmlString)
    return imgUrlList 
        
def getAndSaveImg(imgURL, filename):
    request = urllib2.Request(imgURL)
    data = urllib2.urlopen(request).read()

    img_path = os.path.join(settings.UPLOADS_PATH, filename)
    
    try:
        with open(img_path, 'wb+') as f:
            f.write(data)
    except:
        print("%s file open failed" % img_path)
        
    return
        
        
#生成一个文件名字符串   
def generateFileName():
    string = str(uuid.uuid1())
    string = string.replace('-', 'x')
    return string
    
         
#根据文件名创建文件    
def createFileWithFileName(localPathParam,fileName):  
    totalPath=localPathParam+'\\'+fileName  
    if not os.path.exists(totalPath):  
        file=open(totalPath,'a+')  
        file.close()  
        return totalPath  
      
  
  
  