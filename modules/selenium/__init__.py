import json

from selenium import webdriver

def add_domain_cookies(
    driver:webdriver.Firefox, 
    cookies:list[dict]=[], 
    domain:str=None, 
    url:str=None
    ):
    """Adds cookies to driver. Makes sure that cookies are only added for
    the currently selected domain URL.

    Args:
        driver (webdriver.Firefox): Selenium Webdriver
        cookies (list[dict], optional): List of cookies. Defaults to [].
        domain (str, optional): Domain URL. Defaults to None.
        url (str, optional): URL to go to before adding cookies. Defaults to None.
    """
    if url: driver.get(url)
    for cookie in cookies:
        if domain == None:
            try: driver.add_cookie(cookie)
            except: pass
        elif domain:
            # 'www.bestbuy.com'.endswith('.bestbuy.com')
            # 'www.bestbuy.com.'.endswith('.bestbuy.com.') 
            if domain.endswith(cookie['domain']) or (domain+'.').endswith(cookie['domain']):
                driver.add_cookie(cookie)

def join_cookies(cookies_a:list[dict], cookies_b:list[dict]) -> list[dict]:
    """Joins 2 lists of cookies together, duplicate objects are merged together

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
            

class SeleniumWebsite:

    domain:str = None
    domain_mainpage:str = None

    def __init__(
        self, 
        driver:webdriver.Firefox=None, 
        credentials:dict={}, 
        cookies:list[dict]=[],
        ):
        """Initialize a SeleniumWebsite instance

        Args:
            driver (webdriver.Firefox, optional): 
                Selenium Webdriver. Defaults to None.

            credentials (dict, optional):
                Credential arguments. Defaults to {}.
                Ex: ```
                    {
                        "email" (str),
                        "password" (str),
                        ? "stay_signed_in" (bool),
                    }
                    ```

            cookies (list[dict], optional):
                List of web browser cookies. Defaults to [].
                Ex: ```
                    [
                        {
                            "domain" (str),
                            ...
                        }
                    ]
                    ```

        Raises:
            ValueError: If initializing a object without a domain
        """

        # If SeleniumWebsite is 
        if type(self) == SeleniumWebsite:
            raise ValueError(
                "You should not initialize any instances of SeleniumWebsite. "
                "Use objects that extend SeleniumWebsite."
            )

        if driver == None: driver = webdriver.Firefox()
        self.driver = driver

        # Add cookies if given
        if len(cookies) > 0:
            add_domain_cookies(self.driver, cookies, domain=self.domain, url=self.domain_mainpage)
        
        # If credentials given, login
        if credentials:
            self.login(**credentials)


    # def login(
    #     self,
    #     username:dict,
    #     password:bool,
    #     stay_signed_in:bool = True,
    #     url:str = domain,
    #     ):
    #     raise ValueError("Must define ")