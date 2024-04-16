import requests
from requests.auth import HTTPProxyAuth

# Proxy configuration
proxy_host = 'gate.dc.smartproxy.com'
proxy_port = 27503
username = 'sp43xuny7n'
password = 'i1NRxNR_66x+xO6A4'
proxies = {
    'http': f'http://{username}:{password}@{proxy_host}:{proxy_port}',
    'https': f'https://{username}:{password}@{proxy_host}:{proxy_port}'
}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

proxies = {'http': f'http://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:{proxy_port}',  # Your username, password for proxy authentication, and desired endpoint within punctuation marks ('')
        'https': f'https://sp43xuny7n:i1NRxNR_66x+xO6A4@gate.dc.smartproxy.com:{proxy_port}'}
# Add proxy authentication if needed
auth = HTTPProxyAuth(username, password)

# Example request using proxy
try:
    r = requests.get("https://www.yelp.com", headers=headers, proxies=proxies)
    # response = requests.get('https://www.yelp.com', proxies=proxies)
    print(r.status_code)
except requests.exceptions.ProxyError as e:
    print(f"Proxy error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
