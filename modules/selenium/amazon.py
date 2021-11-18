from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from . import SeleniumWebsite

class SeleniumAmazon(SeleniumWebsite):

    domain = "www.amazon.com"
    domain_mainpage = "https://www.amazon.com"

    def login(
        self,
        email:str,
        password:str,
        stay_signed_in:bool=True,
        url:str='https://www.amazon.com/',
        ):
        wait = WebDriverWait(self.driver, 5)
        # Go to Amazon's main page if url is not 'None'
        if url: self.driver.get(url)

        # Return if already logged in
        try:
            self.driver.find_element_by_id("nav-item-signout")
            return
        except: pass

        # Click the 'Sign in' button on Amazon's main page
        wait.until(
            EC.presence_of_element_located((By.ID, "nav-link-accountList"))
        ).click()

        # If password field is shown, skip inputting email
        try:
            self.driver.find_element_by_id("ap_password")
        except:
            # Send the email provided
            wait.until(
                EC.presence_of_element_located((By.ID, 'ap_email'))
            ).send_keys(email)
            # Continue to password
            self.driver.find_element_by_id('continue').click()

        # Send the password provided
        wait.until(
            EC.presence_of_element_located((By.ID,'ap_password'))
            ).send_keys(password)

        # If 'stay_signed_in' is True, check the box keeping the user signed in
        if stay_signed_in:
            self.driver.find_element_by_xpath(
                "//input[@name='rememberMe']"
            ).click()

        # Submit credentials
        self.driver.find_element_by_id('signInSubmit').click()
        
    def scrape_url(self, url:str=None) -> dict:
        # Go to the URL specified
        if url: self.driver.get(url)

        # parse values from 
        res:dict = {
            "type": "product",
            "productTitle": self.driver.find_element_by_id('productTitle').text,
            "availability": self.driver.find_element_by_xpath(
                "//div[@id='availability']/span").text,
            "rating": self.driver.find_element_by_id("acrCustomerReviewText").text,
            "imageURL": self.driver.find_element_by_xpath(
                "//img[@id='landingImage']").get_attribute('src'),
        }
        
        # If product is 'Currently unavailable', set specific values and return
        if res['availability'] == 'Currently unavailable.':
            res['sitePrice'] = None
            res['thirdPartyPrices'] = []
            return res
        
        try: res['sitePrice'] = self.driver.find_element_by_id("priceblock_ourprice").text
        except NoSuchElementException: pass
        try: res['sitePrice'] = self.driver.find_element_by_id("priceblock_dealprice").text
        except NoSuchElementException: pass
        try: res['sitePrice'] = self.driver.find_element_by_id("priceblock_saleprice").text
        except NoSuchElementException: pass
        
        return res