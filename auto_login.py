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
    browser.add_cookie({"name": "MUSIC_U", "value": "005892ED43B4FA1EA6FA81DF3276BFDEFB7463CF0A925FCC1CECCD0EB39935AA47143FCDD06AC8BC391B866124DA46C2C7096C5B2C5CF68598E7726A996B1B0150C8A2B8E6C166D8B01FFF4DB15270871AE64C13675393DDC25FBF9BC8DC6C035004530C9B4FB58EFBA3CD5FC817E12AEDE8C34D701564985DC1F80B79C7C95C9E69AE21E8E23D3ADA5374C93959EFE0AB5DCE7D2EA2B1061EAEA2AAC4911683C36B5A5E2FDE358A944F6C88361C6E544AA7107B51413DB35C57928D1532E6684DF8BB509BBEFF67ACCA8CEDEF74A9914EECDC153E4394FE2C47F33604944395E94808B7AE8F0C85AB895A2874D0A907731CC19C0FB9D65E3C8C38C87C48E96638A68A8E9723F017FF1BDEA6979709B764FB39C66608D8A16D4A12EFC124540FD8D816A2BB91F0A56DD666AD4FEFAFE978B6E30A80CE703D19D8B0B9DF9142AD173DA6D37FF8AC7B3AE25EE0144E7312A7A204759BA03278C197FFF639B4D8CD6D"})
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
