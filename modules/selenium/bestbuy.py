from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from time import sleep

def bestbuy_login(driver:webdriver.Firefox, credentials:dict, 
                  url:str='https://www.bestbuy.com',
                #   url:str="https://www.bestbuy.com/site/oculus-quest-2-advanced-all-in-one-virtual-reality-headset-128gb/6473553.p?skuId=6473553", 
                  stay_signed_in=True):
    wait = WebDriverWait(driver, 10)
    
    # If URL specified, go to URL
    if url: driver.get(url)
    
    # Exit popup from initial visit to website
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"c-close-icon"))).click()
    
    # Wait for form to dissapear
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME,"form-body-copy")))
    sleep(.5)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@class,'account-button')]/../.."))).click()
    
    # Input email and password then submit.
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sign-in-btn'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys(credentials['email'])
    driver.find_element_by_xpath("//input[@type='password']").send_keys(credentials['password'])
    # If 'stay_signed_in' specified, check the box to stay signed in
    if stay_signed_in: driver.find_element_by_class_name('c-checkbox-input').click()
    driver.find_element_by_xpath("//button[@type='submit']").click()
    
    # Skip prompt to update recovery phone
    wait.until(EC.presence_of_element_located((By.ID,'recoveryPhone')))
    driver.find_element_by_xpath("//button[contains(@class,'cia-cancel')]").click()
    
def bestbuy_parse_product(driver, url) -> dict:
    res:dict = {"type": "product"}
    
    # Go to the URL specified
    driver.get(url)
    
    res['productTitle'] = driver.find_element_by_xpath("//div[contains(@class,'sku-title')]/h1").text
    res['sitePrice'] = driver.find_element_by_class_name('priceView-customer-price').text
    # res['availability']
    # res['rating']
    # res['imageURL']
    
    return res