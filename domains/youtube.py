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


class SeleniumYouTube(SeleniumWebsite):

    domain = "www.youtube.com"
    domain_mainpage = "https://www.youtube.com"

    def login(
        self,
        email: str,
        password: str,
        stay_signed_in=True,
        url: str = "https://www.youtube.com",
    ):
        return True

        # wait = WebDriverWait(self.driver, 10)

        # # If URL specified, go to URL
        # if url: self.driver.get(url)

        # self.driver.find_element_by_xpath("//yt-formatted-string[text()='Sign in']").click()

        # email_element = self.driver.find_element_by_id("identifierId")
        # email_element.send_keys(email)

        # self.driver.find_element_by_xpath("//span[text()='Next']").click()

    def scrape_url(self, url: str = None) -> dict:
        res: dict = {"type": "video"}

        # Go to the URL specified
        if url:
            self.driver.get(url)

        res["url"] = self.driver.current_url

        res["title"] = (
            WebDriverWait(self.driver, 10)
            .until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//h1[contains(@class,'title')]/yt-formatted-string")
                )
            )
            .text
        )

        res["views"] = int(
            self.driver.find_element_by_class_name("view-count")
            .text.replace(" views", "")
            .replace(",", "")
        )

        res["rating"] = {
            "likes": int(
                self.driver.find_element_by_xpath(
                    "//yt-formatted-string[contains(@aria-label, 'likes')]"
                )
                .get_attribute("aria-label")
                .replace(" likes", "")
                .replace(",", "")
            )
        }

        res["duration"] = self.driver.find_element_by_class_name(
            "ytp-time-duration"
        ).text

        res["author"] = self.driver.find_element_by_xpath(
            "//yt-formatted-string[contains(@class, 'ytd-channel-name')]/a"
        ).get_attribute("href")

        res["date"] = self.driver.find_element_by_xpath(
            "//div[@id='info-strings']/yt-formatted-string"
        ).text

        description_child_elements = self.driver.find_elements_by_xpath(
            "//div[@id='description']/yt-formatted-string/*"
        )
        res["description"] = []
        for element in description_child_elements:
            if element.tag_name == "span":
                res["description"].append(element.get_attribute("innerText"))
            elif element.tag_name == "a":
                res["description"].append(
                    {
                        "type": "link",
                        "url": element.get_attribute("href"),
                        "text": element.get_attribute("innerText"),
                    }
                )
            else:
                raise ValueError(
                    "Unknown description element tag: %s" % element.tag_name
                )
        res["description"] = res["description"][: int(len(res["description"]) / 2)]

        return res
