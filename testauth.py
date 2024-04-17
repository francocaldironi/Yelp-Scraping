import requests
from bs4 import BeautifulSoup

url = 'https://ip.smartproxy.com/json'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

proxies = {'http': 'http://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:20001', # Your username, password for proxy authentication, and desired endpoint within punctuation marks ('')
          'https': 'https://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:20001'} 

soup = BeautifulSoup(requests.get(url, headers=headers, proxies=proxies).text, 'lxml')

ip_info = soup.find('body')

print(ip_info.get_text())
