import sys
from os.path import normpath, dirname, abspath, join, isfile
import json
from urllib.parse import urlparse
import pickle
import traceback

from selenium import webdriver
from onepassword import OnePassword

from domains import join_cookies, get_domain_driver

dir_script:str = abspath(join(normpath(dirname(__file__))))
file_cookies:str = join(dir_script,"cache","cookies","_.pkl")

with open(join(dir_script,'config.json'), 'r') as f: config = json.load(f)

driver_types = {
    'firefox': webdriver.Firefox,
    'chrome': webdriver.Chrome
}

onepw = None


def scrape_urls(args):
    
    response = {'results':[], 'errors':[]}
    
    driver = driver_types[args.driver]()

    domain_instances = {}

    # Read cookies from file at location 'file_cookies'
    cookies:list = \
        None if args.skip_cookies or not isfile(file_cookies) \
        else pickle.load(open(file_cookies, "rb"))
        
    if args.manual_mode:
        input("\nEntering manual mode. Once complete, press enter...\n")

    # Iterate over each url specified
    for url in args.url:
        try:
            # Get base domain URL.
            domain = urlparse(url).netloc
            
            # Instantiate domain instance if not already defined.
            if domain not in domain_instances:
                # Get credentials from 1Password if specified in 'config.json'.
                credentials:dict = \
                    None if args.skip_login \
                    else get_domain_credentials_1pw(domain)
                    
                # Instantiate the domain instance.
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

    # Save cookies to location 'file_cookies' if 'args.skip_cookies' specified.
    if not args.skip_cookies:
        pickle.dump(
            join_cookies(driver.get_cookies(), cookies or []), 
            open(file_cookies,"wb")
            )

    # Close web browser after parsing each url.
    driver.quit()
    
    # If no errors, delete property from response.
    if len(response['errors']) == 0:
        del response['errors']
    
    return response

def get_domain_credentials_1pw(domain):
    if domain not in config['credentials'] or config['credentials'][domain] == None:
        return None
    
    global onepw
    
    if onepw == None:
        onepw = OnePassword()
        
    return onepw.get_item(uuid="Amazon", fields=["username", "password"])
    
    
    