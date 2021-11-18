import os
from os.path import normpath, dirname, abspath, join, isfile
import json
from urllib.parse import urlparse
import pickle

from selenium import webdriver

from modules.selenium import join_cookies
from modules.selenium.amazon import SeleniumAmazon
from modules.selenium.bestbuy import SeleniumBestBuy

dir_script:str = abspath(join(normpath(dirname(__file__)), '..'))
dir_cookies:str = join(dir_script,"cache","cookies","_.pkl")

domain_meta = {
    "www.amazon.com": {
        "class":        SeleniumAmazon,
        "credentials":  join(dir_script,'credentials','amazon.json'),
    },
    "www.bestbuy.com": {
        "class":        SeleniumBestBuy,
        "credentials":  join(dir_script,'credentials','bestbuy.json'),
    },
}

def scrape_urls(args, driver = None):
    res = []
    
    driver = webdriver.Firefox()

    domain_instances = {domain: None for domain in domain_meta.keys()}

    # Read cookies from file at location 'dir_cookies'
    cookies:list = pickle.load(open(dir_cookies, "rb")) if isfile(dir_cookies)\
                   else []
    args.cookies = cookies

    # Iterate over each url specified
    for url in args.url:
        domain = urlparse(url).netloc
        
        # Throw error if domain is not in dict 'domain_meta'
        if domain not in domain_meta:
            raise ValueError("Unable to scrape domain: %s" % domain)

        credentials:dict = parse_domain_credentials(domain_meta[domain]["credentials"])

        if domain_instances[domain] == None:
            domain_instances[domain] = domain_meta[domain]["class"](driver, credentials, cookies)

        scrape_res = domain_instances[domain].scrape_url(url)
        
        res.append(scrape_res)
        
    # Save cookies to location 'dir_cookies'
    pickle.dump( join_cookies(driver.get_cookies(), cookies), open(dir_cookies,"wb"))

    driver.quit()
    
    return res

def parse_domain_credentials(path:str) -> dict[str]:
    with open(path, 'r') as f: data = json.load(f)
    return data