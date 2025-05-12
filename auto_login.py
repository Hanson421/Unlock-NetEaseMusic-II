# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0074033828D921AB94E7505985ED68D2CE8909C87E5B3440446278FDC147F718D24D08D402D38B3A29FC10CF34CF06FB0218183E16EB9837E8773BCEAC4E15DC4361716EF3FA8EE77C2319F72C48DC2BEDC3E04A3A4AD8AAD3A5042A7F8F930D89A137B94BA87EEF52B9E7755F192701AC5347FEC5C0936371810DAA336C0AE762007F0855C023564A25B49CEBF6C572D83D846C2F4EF61BAA3757DAA63E017A9CDFFC1CC4E0AAE3F2BAA0E5212ECD51A72CCFA7532A9DB6C0C2F103CA1BF2003220EF3D0788D86E87A0C2E8EAF63F9278EBA7B603B912C39BFDB35FCF020115EDCF69D69EDB26D3DF36B64098A6B0ED8105E6BAA388576D1AADEB1487100F40C9C26BB8471F472346F6BA71BBCC106538FA05E5FE1AC323F5185D3278AD208D4057993E61FE68213C2AFEAA2E814556021A46C26D21727324554533E79C92C5FE"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
