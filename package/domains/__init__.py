import json

from selenium.webdriver.remote.webdriver import WebDriver

from .SeleniumWebsite import SeleniumWebsite
from .airbnb import SeleniumAirbnb
from .amazon import SeleniumAmazon
from .bestbuy import SeleniumBestBuy
from .youtube import SeleniumYouTube

domain_map = {
    "www.airbnb.com": SeleniumAirbnb,
    "www.amazon.com": SeleniumAmazon,
    "www.bestbuy.com": SeleniumBestBuy,
    "www.youtube.com": SeleniumYouTube,
}


def join_cookies(cookies_a: list[dict], cookies_b: list[dict]) -> list[dict]:
    """Joins 2 lists of cookies together, duplicate objects are merged together.

    Args:
        cookies_a (list[dict]): List of cookies A
        cookies_b (list[dict]): List of cookies B

    Returns:
        list[dict]: Merged list of cookies
    """
    parsed = {}
    for cookie in [*cookies_a, *cookies_b]:
        parsed[json.dumps(cookie, sort_keys=True)] = cookie
    return list(parsed.values())


def get_domain_driver(
    domain: str,
    driver: WebDriver = None,
    credentials: dict = None,
    cookies: list[dict] = None,
) -> SeleniumWebsite:
    """Return a SeleniumWebsite object for the given domain.

    Args:
        domain (str): Domain URL (ex: www.amazon.com)
        driver (WebDriver, optional): Selenium WebDriver. Defaults to None.
        credentials (dict, optional): Credentials for domain login. Defaults to None.
        cookies (list[dict], optional): List of cookies. Defaults to None.

    Returns:
        Se: _description_
    """
    return domain_map[domain](driver, credentials, cookies)
