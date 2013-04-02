# coding = utf8
from bs4 import BeautifulSoup
import urllib, urllib2
from urlparse import urlparse, urljoin
import robotexclusionrulesparser

def crawl_web(seed, max_pages, max_depth): # returns index, graph of inlinks
    tocrawl = [[seed, 0]]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl: 
        page, depth = tocrawl.pop()
        print "CURRENT DEPTH: ", depth
        print "PAGES CRAWLED: ", len(crawled)
        if page not in crawled and len(crawled) < max_pages and depth <= max_depth:
            soup, url = get_page(page)
            polite(page)
            get_file(page)
            add_page_to_index(index, page, soup)
            outlinks = get_all_links(soup, url)
            graph[page] = outlinks
            add_new_links(tocrawl, outlinks, depth)
            crawled.append(page)
    return index, graph

def get_all_links(page, url):
    links = []
    page_url = urlparse(url)
    base = page_url[0] + '://' + page_url[1]
    robots_url = urljoin(base, '/robots.txt')
    rp = robotexclusionrulesparser.RobotFileParserLookalike()
    rp.set_url(robots_url)
    rp.read()
    #print rp
    for link in page.find_all('a'):
    	link_url = link.get('href')
        print "Found a link: ", link_url
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
	else:
	    network = urljoin(base, link_url) #Join it with the path
	    links.append(network)
    return links

def add_new_links(tocrawl, outlinks):
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
    rp.read()
    if not rp.can_fetch('*', url):
        print "page off limits!"
        return BeautifulSoup(""), ""        
    if url in cache:
        return cache[url]
    else:
        print "Page not in cache: " + url
        try: 
            content = urllib.urlopen(url).read()
            return BeautifulSoup(content), url
        except:
            return BeautifulSoup(""), ""
            
def polite(url): #GEt depay time from robots.txt
    page_url = urlparse(url)
    base = page_url[0] + '://' + page_url[1]
    robots_url = urljoin(base, '/robots.txt')
    rp = robotexclusionrulesparser.RobotExclusionRulesParser()
    rp.fetch(robot_url)
    if rp.getc_crawl_delay(robots_url):
    	time.sleep(rp.get_crawl_delay(robots_url))
    else:
    	time.sleep(1)

def get_file(url): #Download file
    response = urllib2.urlopen(url)
    content_type = response.info().get('Content-Type')
    if 'application' in content_type:
    	filename = str(page_url[2].split('/')[-1]
    	f = urllib2.urlopen(url)
    	with open(filename, "wb") as code:
    	    code.write(f.read())
        	
cache = {}
max_pages = 100
max_depth = 4
index, graph = crawl_web('http://www.python.org/', max_pages, max_depth)

print "INDEX: ", index
print ""
print "GRAPH: ", graph
print ""
