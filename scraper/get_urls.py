from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

from urllib.parse import urljoin
import common.logging as logging
import time
import datetime
from datetime import timedelta
from typing import List


if __name__ == "__main__":
    try:
        time.sleep(5)

        options = Options()
        options.headless = True
        options.add_argument("window-size=1200x600")
        scroll_pause_time = 5

        driver = webdriver.Remote(
            "http://selenium-chrome:4444/wd/hub", options=options)

        screen_height = driver.execute_script("return window.screen.height;")
        i = 1

        driver.get("https://factba.se/trump/transcripts/")

        logging.log("At trump endpoint")

        time.sleep(3)

        while True:
            logging.log(f"Scrolling {i}")

            # scroll one screen height each time
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = driver.execute_script("return document.body.scrollHeight;")  
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                break
            
            if i > 2300:
                break
        
        logging.log("Collecting urls")
        urls = []
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for a in soup.find_all('a', href=True):
            link = a["href"]
            base = r"https://factba.se/"
            url = urljoin(base, link)
            urls.append(url)

        logging.log("Writing to df")
        df = pd.DataFrame(list(set(urls)))
        df.to_csv("/app/common/trump_urls.csv")

        logging.log("Done!")


        # login_elements = driver.find_elements(
        #     By.XPATH, "//div[text()='Login/Sign Up']")

        # WebDriverWait(driver, 20).until(
        #     EC.element_to_be_clickable(login_elements[0])).click()

        # time.sleep(3)

        # logging.log("About to login")

        # sign_in_username = driver.find_elements(By.ID, "signInFormUsername")[1]
        # sign_in_password = driver.find_elements(By.ID, "signInFormPassword")[1]
        # sign_in_submit = driver.find_elements(By.NAME, "signInSubmitButton")[1]

        # sign_in_username.send_keys(secrets.CHATTERQUANT_USERNAME)
        # sign_in_password.send_keys(secrets.CHATTERQUANT_PASSWORD)
        # WebDriverWait(driver, 20).until(
        #     EC.element_to_be_clickable(sign_in_submit)).click()

        # logging.log("Logging in")

        # time.sleep(3)

        # driver.get("https://chatterquant.com/popout/alerts")

        # logging.log("At popout alerts")

        # time.sleep(3)

        # overall_alert_objects = []
        # first_run = True

        # while True:
        #     divs = driver.find_elements(By.XPATH, "//div")

        #     next_one = False
        #     alerts_are_in_here = []
        #     for div in divs:
        #         if next_one:
        #             alerts_are_in_here.append(div)
        #         if "STOCKS ONLY" in div.text:
        #             next_one = True

        #     logging.log("Found alerts")

        #     next_one = False
        #     alerts = []
        #     alerts_class_number = 0
        #     for div in alerts_are_in_here:
        #         if next_one:
        #             if alerts_class_number > 0:
        #                 if alerts_class_number == get_class_int(div.get_attribute("class")):
        #                     alerts.append(div)
        #             else:
        #                 alerts_class_number = get_class_int(
        #                     div.get_attribute("class")) + 1
        #         elif "MuiSelect-root MuiSelect-select" in div.get_attribute("class"):
        #             next_one = True

        #     alert_objects = []
        #     for alert in alerts:
        #         p_tags = alert.find_elements(By.TAG_NAME, "p")
        #         span_tags = alert.find_elements(By.TAG_NAME, "span")
        #         alert_object = create_alert_object(
        #             p_tags[0].text, p_tags[1].text, span_tags[-1].text)
        #         alert_objects.append(alert_object)
        #         if first_run:
        #             overall_alert_objects.append(alert_object)

        #     if not first_run:
        #         for alert_obj in alert_objects:
        #             if not is_repeated_alert(alert_obj, overall_alert_objects):
        #                 print("NEW! ", alert_obj.symbol, alert_obj.alert_type,
        #                     alert_obj.company_name, alert_obj.alert_datetime)
        #                 # TODO: Add to db
        #                 overall_alert_objects.append(alert_obj)
        #     else:
        #         first_run = False
        #         for alert_obj in alert_objects:
        #             print("FIRST RUN! ", alert_obj.symbol, alert_obj.alert_type,
        #                 alert_obj.company_name, alert_obj.alert_datetime)
        #         # TODO: Add to db

        #     logging.log("Waiting 60 seconds to scrape again...")
        #     time.sleep(60)
    except Exception as e:
        logging.error(e)
