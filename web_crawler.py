from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from multiprocessing import Process, Manager
import requests
import sys
from urllib.parse import urlparse, urljoin


# Crawls 3 unique urls from the shared url queue.
def crawlUrls(url_queue, url_set):
    sites_visited = 0
    while True:
        # Retrieve a URL from queue
        url = url_queue.get()
        url_set.append(url)
        result = [url]
        
        # Get all URLs embedded on the page and add them
        # to our queue.
        embedded_urls = getAllUrlsOnPage(url)
        for embedded_url in embedded_urls:
            result.append("\t"+ embedded_url)
            if embedded_url not in url_set:
                url_queue.put(embedded_url)
                url_set.append(embedded_url)
        
        # Print out results and increment visits.
        print("\n".join(result))
        sites_visited += 1
        if sites_visited > 2:
            break
    return

# Takes in a URL, fetches all html from the page and retrieves
# all absolute URLs embedded in href tags.
def getAllUrlsOnPage(url):
    # Attempt to retrieve html from a webpage, log an error
    # on failure.
    parser = 'html.parser'
    embedded_urls = set()
    try:
        resp = requests.get(url)
    except:
        print("Error fetching URL: %s. Ensure that the URLs on the page are valid." % url)
        return embedded_urls
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(resp.content, parser, from_encoding=encoding)
    
    # Only retrieve absolute URLs embedded in hrefs
    for link in soup.find_all('a', href=True):
        href_link = link['href']
        if isAbsoluteUrl(href_link):
            normalize_url = urljoin(href_link, urlparse(href_link).path.replace('//','/'))
            normalize_url = urljoin(normalize_url,urlparse(href_link).query)
            normalize_url = normalize_url.strip("/")
            if normalize_url.startswith("http"):
                embedded_urls.add(normalize_url)

    return sorted(embedded_urls)

# Checks if a url is absolute or not
def isAbsoluteUrl(url):
    return bool(urlparse(url).netloc)

# Driver code for webcrawler script
with Manager() as manager:
    # Set up shared queue and set
    shared_url_queue = manager.Queue()
    # Starting URL is the one passed into the script
    shared_url_queue.put(sys.argv[1])
    shared_url_set = manager.list([sys.argv[1]])
    processes = []
    # Start multiple processes, each crawling URLs
    for i in range(2):
        p = Process(target=crawlUrls, args =(shared_url_queue, shared_url_set))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()

