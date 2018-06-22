import urllib,requests
import os,sys
import re
import tomd
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("[*] Please download and install Beautiful Soup first!")
    sys.exit()

def getVols():
    vols = [] 
    target = "http://scienceblogs.com/evolgen/"
    html = requests.get(url=target)
    bs = BeautifulSoup(html.content,'html.parser')
    siderBar = bs.find('div', {'class' : 'widget clearfix widget_archive'}).find_all("a")   
    for a in siderBar:
        vols.append(a.get('href'))
    
    return vols

def getBlogList(vols):
    blogs = []
    list.reverse(vols)  #from oldest to newest, YEAR and MONTH
    for vol in vols:
        html = requests.get(url = vol)
        bs = BeautifulSoup(html.content,'html.parser')
        title = bs.find_all('h1',{'class':'title entry-title'})
        temp = []
        for h1 in title:
            temp.append(h1.a.get('href'))
        list.reverse(temp)  # from oldest to newest, DATE
        blogs.extend(temp)
    
    return blogs

def getContent(url):
    page = []
    (year,month) = re.search('http://scienceblogs.com/evolgen/(\d+)/(\d+)',url).groups()
    print("processing %s %s"%(month,year),end='\r')
    out = open('evolgen.md','wt')
    html = requests.get(url = url)
    bs = BeautifulSoup(html.content,'html.parser')
    header = bs.find('h1',{'class':'title entry-title'})
    page.append("#" + header.text)
    abbr = bs.find('abbr',{'class':'published'})
    page.append("Date: %s"%abbr.text)
    content = bs.find('div',{'class':'content entry-content'})
    for tag in content:
        if tag == "\n":
            continue
        page.append(tomd.convert(str(tag)))
    return page

blogs = getBlogList(getVols())

try:
    os.remove("evolgen.md")
except OSError:
    pass

out = open("evolgen.md",'w')

for blog in blogs:
    page = getContent(blog)
    print("\n".join(page), file = out)
    
