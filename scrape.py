import sys
from os.path import normpath, dirname, abspath, join, isfile
import json
from urllib.parse import urlparse
import pickle
import traceback

from selenium import webdriver

from domains import join_cookies, get_domain_driver


dir_script:str = abspath(join(normpath(dirname(__file__))))
dir_cookies:str = join(dir_script,"cache","cookies","_.pkl")

with open(join(dir_script,'config.json'), 'r') as f: config = json.load(f)



def scrape_urls(args, driver = None):
    
    driver_types = {
        'firefox': webdriver.Firefox,
        'chrome': webdriver.Chrome
    }
    
    response = {'results':[], 'errors':[]}
    
    driver = driver_types[args.driver]()

    domain_instances = {}

    # Read cookies from file at location 'dir_cookies'
    cookies:list = pickle.load(open(dir_cookies, "rb")) if isfile(dir_cookies)\
                   else []
    args.cookies = cookies

    # Iterate over each url specified
    for url in args.url:
        try:
            print(url)
            # Get base domain URL.
            domain = urlparse(url).netloc
            print(domain)
            
            # Instantiate domain instance if not already defined.
            if domain not in domain_instances:
                # Get credentials from 1Password if specified in 'config.json'.
                credentials:dict = get_domain_credentials_1pw(domain)
                domain_instances[domain] = get_domain_driver(domain, driver, credentials, cookies)

            # Scrape specific URL.
            scrape_res = domain_instances[domain].scrape_url(url)
            
            # Append results to 'response' dictionary.
            response['results'].append(scrape_res)
            
        # If failed, do not stop program. Append message to 'response' dictionary.
        except ValueError as error:
            response['errors'].append(traceback.print_exc(error))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    # Save cookies to location 'dir_cookies'
    pickle.dump( join_cookies(driver.get_cookies(), cookies), open(dir_cookies,"wb"))

    # Close web browser after parsing each url.
    driver.quit()
    
    # If no errors, delete property from response.
    if len(response['errors']) == 0:
        del response['errors']
    
    return response

def get_domain_credentials_1pw(domain):
    if domain not in config['credentials'] or config['credentials'][domain] == None:
        return None
    
    
    