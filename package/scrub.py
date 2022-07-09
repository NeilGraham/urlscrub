import sys
from os.path import normpath, dirname, abspath, join, isfile
import json
from urllib.parse import urlparse
import pickle
import traceback

from selenium import webdriver
from onepassword import OnePassword

from .domains import join_cookies, get_domain_driver, SeleniumWebsite

dir_script: str = abspath(join(normpath(dirname(__file__))))
file_cookies: str = join(dir_script, "cookies", "_.pkl")

with open(join(dir_script, "config.json"), "r") as f:
    config = json.load(f)

driver_types = {"firefox": webdriver.Firefox, "chrome": webdriver.Chrome}

domain_names = {
    "amazon": "www.amazon.com",
    "bestbuy": "www.bestbuy.com",
    "youtube": "www.youtube.com",
    "airbnb": "www.airbnb.com",
}


domain_instances = {}

onepw = None


def pop_silent(l: list, i: int = -1):
    """Pops item from list, returns None if list is empty or
    item doesn't exist at indice.

    Args:
        l (list): List to pop from.
        i (int, optional): Index to pop item from list. Defaults to -1.

    Returns:
        _type_: Item from list at index 'i'.
    """
    try:
        return l.pop(i)
    except IndexError:
        return None


def get_domain_instance(
    domain: str, driver, cookies: list[dict], args
) -> SeleniumWebsite:
    """Instantiates domain driver if doesn't exist, otherwise returns
    existing instance.

    Args:
        domain (str): Domain (e.g. 'www.amazon.com').
        driver (_type_): Selenium WebDriver.
        cookies (list[dict]): List of cookies.
        args (_type_): ArgParse arguments.

    Returns:
        SeleniumWebsite: Domain driver instance.
    """
    # Reference global variables 'domain_instances', 'config'.
    global domain_instances
    global config

    # Instantiate domain instance if not already defined.
    if domain not in domain_instances:
        # Get credentials from 1Password if specified in 'config.json'.
        credentials: dict = (
            None if args.skip_login else get_domain_credentials_1pw(domain)
        )

        # Instantiate the domain instance.
        domain_instances[domain] = get_domain_driver(
            domain, driver, credentials, cookies
        )

    return domain_instances[domain]


def scrub_urls(args):

    response = {"results": [], "errors": []}

    driver = driver_types[args.driver]()

    # Read cookies from file at location 'file_cookies'
    cookies: list = (
        None
        if args.skip_cookies or not isfile(file_cookies)
        else pickle.load(open(file_cookies, "rb"))
    )

    if args.manual_mode:
        input("\nEntering manual mode. Once complete, press enter...\n")

    # Iterate over list of urls specified.
    for url in args.url:
        try:
            # Get base domain URL.
            domain = urlparse(url).netloc

            domain_driver = get_domain_instance(domain, driver, cookies, args)

            # Scrape URL and append results to 'response' dictionary.
            response["results"].append(domain_driver.scrape_url(url))

        # If failed, do not stop program. Append message to 'response' dictionary.
        except ValueError as error:
            response["errors"].append(traceback.print_exc(error))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    # Iterate over list of search commands specified.
    for search in args.search:
        try:
            search_args = [s.strip() for s in search.split(";")]

            url = pop_silent(search_args, 0)
            search_string = pop_silent(search_args, 0)
            limit = pop_silent(search_args, 0) or 10

            if search_string == None:
                response["errors"].append(
                    "Expected search string after ';' "
                    "(e.g. '<domain>;<search_string>(;<limit>)'. "
                    f"Got '{search}'."
                )
                continue

            domain = domain_names.get(url.lower()) or urlparse(url).netloc

            domain_driver = get_domain_instance(domain, driver, cookies, args)

            # If 'domain_driver' does not have method 'search', append error.
            if not getattr(domain_driver, "search", False):
                response["errors"].append(
                    f"Domain '{domain}' does not have method 'search'."
                )
                continue

            response["results"].extend(domain_driver.search(search_string, limit))

        # If failed, do not stop program. Append message to 'response' dictionary.
        except ValueError as error:
            response["errors"].append(traceback.print_exc(error))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    # Save cookies to location 'file_cookies' if 'args.skip_cookies' not specified.
    if not args.skip_cookies:
        pickle.dump(
            join_cookies(driver.get_cookies(), cookies or []), open(file_cookies, "wb")
        )

    # Close web browser after parsing each url.
    driver.quit()

    # If no errors, delete property from response.
    if len(response["errors"]) == 0:
        del response["errors"]

    return response


def get_domain_credentials_1pw(domain):
    if domain not in config["credentials"] or config["credentials"][domain] == None:
        return None

    global onepw

    if onepw == None:
        onepw = OnePassword()

    return onepw.get_item(uuid="Amazon", fields=["username", "password"])
