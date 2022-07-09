from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class SeleniumWebsite:

    domain: str = None
    domain_mainpage: str = None

    def __init__(
        self,
        driver: WebDriver = None,
        credentials: dict = None,
        cookies: list[dict] = None,
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

        # Throw error if trying to initialize SeleniumWebsite.
        if type(self) == SeleniumWebsite:
            raise ValueError(
                "You should not initialize any instances of SeleniumWebsite. "
                "Use objects that extend SeleniumWebsite."
            )

        # If no webdriver specified, instantiate Firefox webdriver.
        if driver == None:
            self.driver = webdriver.Firefox()
        else:
            self.driver = driver

        # Add cookies if given.
        if cookies:
            self.add_cookies(cookies)

        # If credentials given, login.
        if credentials:
            self.login(**credentials)

    def add_cookies(self, cookies):
        if self.domain_mainpage:
            self.driver.get(self.domain_mainpage)
        for cookie in cookies:
            if self.domain == None:
                try:
                    self.driver.add_cookie(cookie)
                except:
                    pass
            elif self.domain:
                # 'www.bestbuy.com'.endswith('.bestbuy.com')
                # 'www.bestbuy.com.'.endswith('.bestbuy.com.')
                if self.domain.endswith(cookie["domain"]) or (
                    self.domain + "."
                ).endswith(cookie["domain"]):
                    self.driver.add_cookie(cookie)
        # Reload current URL after adding cookies
        self.driver.get(self.driver.current_url)

    # def login(
    #     self,
    #     username:dict,
    #     password:bool,
    #     stay_signed_in:bool = True,
    #     url:str = domain,
    #     ):
    #     raise ValueError("Must define ")
