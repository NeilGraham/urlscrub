from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from .SeleniumWebsite import SeleniumWebsite


class SeleniumBestBuy(SeleniumWebsite):

    domain = "www.bestbuy.com"
    domain_mainpage = "https://www.bestbuy.com"

    def login(
        self,
        email: str,
        password: str,
        stay_signed_in=True,
        url: str = "https://www.bestbuy.com",
    ):
        wait = WebDriverWait(self.driver, 10)

        # If URL specified, go to URL
        if url:
            self.driver.get(url)

        # Exit popup from initial visit to website
        try:
            wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "c-close-icon"))
            ).click()
        except:
            pass

        # Wait for form to dissapear
        wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "form-body-copy"))
        )
        sleep(0.5)
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[contains(@class,'account-button')]/../..")
            )
        ).click()
        wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'account-header') or contains(@class,'header-guest-user')]",
                )
            )
        )
        sleep(0.5)

        # Return if already logged in
        try:
            self.driver.find_element_by_id("logout-button")
            return
        except:
            pass

        # Input email and password then submit.
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "sign-in-btn"))
        ).click()
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
        ).send_keys(email)
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys(
            password
        )
        # If 'stay_signed_in' specified, check the box to stay signed in
        if stay_signed_in:
            self.driver.find_element_by_class_name("c-checkbox-input").click()
        self.driver.find_element_by_xpath("//button[@type='submit']").click()

        # Skip prompt to update recovery phone
        wait.until(EC.presence_of_element_located((By.ID, "recoveryPhone")))
        self.driver.find_element_by_xpath(
            "//button[contains(@class,'cia-cancel')]"
        ).click()

    def scrape_url(self, url: str = None) -> dict:
        res: dict = {"type": "product"}

        # Go to the URL specified
        if url:
            self.driver.get(url)

        res["productTitle"] = self.driver.find_element_by_xpath(
            "//div[contains(@class,'sku-title')]/h1"
        ).text
        res["sitePrice"] = self.driver.find_element_by_class_name(
            "priceView-customer-price"
        ).text
        # res['availability']
        # res['rating']
        # res['imageURL']

        return res
