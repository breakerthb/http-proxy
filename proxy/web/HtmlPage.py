import re
import urllib, urllib2



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
        

    