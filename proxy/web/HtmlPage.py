import os
import re
import urllib, urllib2

class URL:
    srcURL = ''
    srcName = ''
    newURL = ''
    newName = ''
    extName = ''
    
    def __init__(self, url):
        self.srcURL = url
        
        url = url.split('?')[0]
        
        lstName = url.split('.')
        
        #self.extName = lstName[-1]
        self.extName = os.path.splitext(url)[1][1:]
        self.srcName = lstName[-2].split("/")[-1]
        self.newName = lstName[-2].replace("/", "1").replace("-", "a")
        
    def __str__(self):
        return u'URL : %s|%s' % (self.srcURL, self.newURL) 
        
    def getSrcURL(self):
        return self.srcURL
        
    def getSrcName(self):
        return self.srcName
    
    def getNewURL(self):
        return self.newURL
    
    def getNewName(self):
        return self.newName
        
    def getExtName(self):
        return self.extName


class HtmlPage:
    pageName = ''
    content = ''

    def __init__(self, url):
        print("HtmlPage Init...")
        try:
            u = urllib2.urlopen(url)
            self.content = u.read()
            
            #print(self.content)
            self.pageName = ''
            
            pattern = re.compile(r'<title>*<title>')  
            self.pageName = pattern.findall(self.content)
            
        except urllib2.HTTPError, e:
            print("Get url page failed")
            print(e.code)
            print(e.read())
        
    
    def getPageName(self):
        return self.pageName
        
    def getContent(self):
        return self.content
        

    