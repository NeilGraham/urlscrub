from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def amazon_login(driver:webdriver.Firefox, credentials:dict, url:str='https://www.amazon.com/', stay_signed_in=True):
    wait = WebDriverWait(driver, 10)
    # Go to Amazon's main page if url is not 'None'
    if url: driver.get(url)
    # Click the 'Sign in' button on Amazon's main page
    wait.until(
        EC.presence_of_element_located((By.ID, "nav-link-accountList"))
    ).click()
    # Send the email provided
    wait.until(
        EC.presence_of_element_located((By.ID, 'ap_email'))
    ).send_keys(credentials['email'])
    driver.find_element_by_id('continue').click()
    # Send the password provided
    wait.until(
        EC.presence_of_element_located((By.ID,'ap_password'))
        ).send_keys(credentials['password'])
    # If 'stay_signed_in' is True, check the box keeping the user signed in
    if stay_signed_in:
        driver.find_element_by_xpath("//input[@name='rememberMe']").click()
    # Submit credentials
    driver.find_element_by_id('signInSubmit').click()
    
def amazon_parse_product(driver, url) -> dict:
    res:dict = {"type": "product"}
    
    # Go to the URL specified
    driver.get(url)
    
    res['productTitle'] = driver.find_element_by_id('productTitle').text
    res['availability'] = driver.find_element_by_xpath("//div[@id='availability']/span").text
    res['rating'] = driver.find_element_by_id("acrCustomerReviewText").text
    res['imageURL'] = driver.find_element_by_xpath("//img[@id='landingImage']").get_attribute('src')
    # If product is 'Currently unavailable', set specific values and return
    if res['availability'] == 'Currently unavailable.':
        res['sitePrice'] = None
        res['thirdPartyPrices'] = []
        return res
    
    try: res['sitePrice'] = driver.find_element_by_id("priceblock_ourprice").text
    except NoSuchElementException: pass
    try: res['sitePrice'] = driver.find_element_by_id("priceblock_dealprice").text
    except NoSuchElementException: pass
    try: res['sitePrice'] = driver.find_element_by_id("priceblock_saleprice").text
    except NoSuchElementException: pass
    
    return res