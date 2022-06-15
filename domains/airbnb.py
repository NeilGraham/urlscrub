from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from domains.SeleniumWebsite import SeleniumWebsite


class SeleniumAirbnb(SeleniumWebsite):

    domain = "www.airbnb.com"
    domain_mainpage = "https://www.airbnb.com"

    def login(
        self,
        email: str,
        password: str,
        stay_signed_in=True,
        url: str = "https://www.airbnb.com",
    ):
        # If URL specified, go to URL
        if url:
            self.driver.get(url)

        # If already logged in, return True
        try:
            self.driver.find_element_by_id("field-guide-toggle").click()
            WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//button[@data-testid='cypress-headernav-logout']")
                )
            )
            return True
        except:
            pass

        self.driver.get(self.domain_mainpage + "/login")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@data-testid='social-auth-button-email']")
            )
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "email-login-email"))
        ).send_keys(email)
        self.driver.find_element_by_xpath(
            "//button[@data-testid='signup-login-submit-btn']"
        ).click()
        sleep(1)
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        ActionChains(self.driver).send_keys(password).perform()
        self.driver.find_element_by_xpath(
            "//button[@data-testid='signup-login-submit-btn']"
        ).click()
        sleep(10)

        return True

    def scrape_url(self, url: str = None) -> dict:
        # Go to the URL specified
        if url:
            self.driver.get(url)

        sleep(2)

        res: dict = {
            "type": "rental",
            "title": self.driver.find_element_by_xpath(
                "//div[@data-section-id='TITLE_DEFAULT']/section/div/span/h1"
            ).text,
            "subtitle": {
                "main": self.driver.find_element_by_xpath(
                    "//div[@data-section-id='OVERVIEW_DEFAULT']/section/div/div/div/div/div/h2"
                ).text,
            },
        }

        return res
