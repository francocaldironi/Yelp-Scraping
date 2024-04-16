# Scraping https://www.yelp.com/biz/the-smile-center-san-francisco-3?osq=dentist

## Installation

Use this command to install dependencies.

```bash
pip install -r requirement.txt
```

## Usage

For scraping using proxy:

```bash  
-python main.py -url "https://www.yelp.com/search?find_desc=Dentist&find_loc=San+Francisco%2C+CA" -p "proxies.txt" -a "user_agents.txt" -o "output.xlsx" -m 10
```
or For scraping not using proxy:
```bash
-python main1.py -url "https://www.yelp.com/search?find_desc=Dentist&find_loc=San+Francisco%2C+CA" -p "proxies.txt" -a "user_agents.txt" -o "output.xlsx" -m 10
```

- With `-url` , The target Page url
- With `-p` , You can choose your proxy type. Supported proxy types are: \*\*HTTP - HTTPS - Socks (Both 4 and 5) - Socks4 -
- With `-a` , User_agents
- With `-o` , create and write to a .csv file. (Default is **output.csv**)
- With `-m` , max scraped listings
