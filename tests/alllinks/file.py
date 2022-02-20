import requests
from bs4 import BeautifulSoup
def extract_all_links(site):
    html = requests.get(site).text
    soup = BeautifulSoup(html, 'html.parser').find_all('a')
    links = [link.get('href') for link in soup]
    return links
#site_link = input('Enter URL of the site : ')
site_link = "https://www.epicgames.com/store/en-US/p/brothers-a-tale-of-two-sons"
all_links = extract_all_links(site_link)
print(all_links) 
