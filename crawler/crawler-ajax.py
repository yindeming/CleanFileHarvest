# coding = utf8
import time
from bs4 import BeautifulSoup
import urllib, urllib2
from urlparse import urlparse, urljoin
import robotexclusionrulesparser
import jabba_webkit as jw


def crawl_web(seed, max_pages, max_depth): # returns index, graph of inlinks
    tocrawl = []
    for url in crawl_list:
        tocrawl.append([url, 0])
    crawled = []
    index = {} 
    while tocrawl: 
        page, depth = tocrawl.pop()
        print "[crawl_web()] Depth: ", depth
        print "[crawl_web()] Pages crawled: ", len(crawled)
        if page not in crawled and len(crawled) < max_pages and depth <= max_depth:
            polite(page)
	    soup, url = get_page(page)
	    soup.append(jw.get_page(page))
	    cache[url] = soup
            add_page_to_index(index, page, soup)
            outlinks = get_all_links(soup, url)
            get_file(outlinks)
            add_new_links(tocrawl, outlinks, depth)
            crawled.append(page)
    index = undupe_index(index)
    return index

def get_all_links(page, url):
    links = []
    page_url = urlparse(url)
    if page_url[0]:
        base = page_url[0] + '://' + page_url[1]
        robots_url = urljoin(base, '/robots.txt')
    else:
    	robots_url = ""
    rp = robotexclusionrulesparser.RobotFileParserLookalike()
    rp.set_url(robots_url)
    try:
        rp.read()
    except:
        pass
    for link in page.find_all('a'):
    	link_url = link.get('href')
    	print "[get_all_links()] Found a link: ", link_url
        #Ignore links that are 'None'
        if link_url == None:
            pass
        elif not rp.can_fetch('*', link_url):
            print "Page off limits!"
	    pass
        #Ignore links that are internal page anchors.
        #Urlparse considers internal anchors 'fragment identifiers', at index 5.
	elif urlparse(link_url)[5] and not urlparse(link_url)[2]:#If a link has a network location
            pass
        elif urlparse(link_url)[1]:
	    links.append(link_url)
	#elif urlparse(link_url)[2] and not urlparse(link_url)[1]:
	else:
	    network = urljoin(base, link_url) #Join it with the path
	    links.append(network)
    return links

def add_new_links(tocrawl, outlinks, depth):
    for link in outlinks:
        if link not in tocrawl:
	    tocrawl.append([link, depth+1])

def add_page_to_index(index, url, content):
    try:
	text = content.get_text()
    except:
        return
    words = text.split()
    for word in words:
	add_to_index(index, word, url)
        
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def get_page(url):
    page_url = urlparse(url)
    base = page_url[0] + '://' + page_url[1]
    robots_url = base + '/robots.txt'
    rp = robotexclusionrulesparser.RobotFileParserLookalike()
    rp.set_url(robots_url)
    try:
        rp.read()
    except:
        pass
    if not rp.can_fetch('*', url):
        print "[get_page()] page off limits!"
        return BeautifulSoup(""), ""        
    if url in cache:
        return cache[url]
    else:
        print "[get_page()] Page not in cache: " + url
        try: 
            content = urllib.urlopen(url).read()
            return BeautifulSoup(content), url
        except:
            return BeautifulSoup(""), ""
            
def polite(url): #Get depay time from robots.txt
    page_url = urlparse(url)
    base = page_url[0] + '://' + page_url[1]
    robots_url = urljoin(base, '/robots.txt')
    rp = robotexclusionrulesparser.RobotExclusionRulesParser()
    try:
        rp.fetch(robots_url)
    except:
        pass
    if rp.get_crawl_delay(robots_url):
    	time.sleep(rp.get_crawl_delay(robots_url))
    else:
    	time.sleep(1)

def get_file(outlinks): #Download file
    for url in outlinks:
        page_url = urlparse(url)
        try:
            print "Download from: ", url
            response = urllib2.urlopen(url)
	    content_type = response.info().get('Content-Type')
            if 'application' in content_type:
    	        filename = str(page_url[2].split('/')[-1])
    	        with open(filename, "wb") as code:
    	            code.write(response.read())
        except:
            pass

def undupe_index(index):
    for key in index.keys():
        index[key] = list(set(index[key]))
    print "[undupe_index()] Index un-duped"
    return index

cache = {}
max_pages = 100
max_depth = 4
crawl_list = ['http://www.download.com','http://www.python.org']

index = crawl_web(crawl_list, max_pages, max_depth)

print "INDEX: ", index
print ""
