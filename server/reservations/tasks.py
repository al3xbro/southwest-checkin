import time
import re
import json

from django.core.mail import send_mail

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# southwest API endpoint and URL; may change
CHECKIN_URL = "https://mobile.southwest.com/check-in"
API_ENDPOINT = "https://mobile.southwest.com/api/mobile-air-operations/v1/mobile-air-operations/page/check-in"
# stolen from @byalextran at https://github.com/byalextran/southwest-headers
HEADER_REGEX = "x-api-key|x-user-experience-id|x-channel-id|^[\w]+?-\w{1,2}$"

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get(CHECKIN_URL)


def get_headers():

    print("Fetching headers...")

    # start broswer

    # wait for page load
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_element_located((By.NAME, "recordLocator")) and
        EC.presence_of_element_located((By.NAME, "firstName")) and
        EC.presence_of_element_located((By.NAME, "lastName"))
    )

    # fill out form
    confirmation_input = driver.find_element(By.NAME, "recordLocator")
    first_name_input = driver.find_element(By.NAME, "firstName")
    last_name_input = driver.find_element(By.NAME, "lastName")

    confirmation_input.clear()
    confirmation_input.send_keys("RANDRA")

    first_name_input.clear()
    first_name_input.send_keys("Raj")

    last_name_input.clear()
    last_name_input.send_keys("Andra")

    confirmation_input.submit()

    # wait for server response
    time.sleep(1)

    # grab headers
    headers = {}
    for request in driver.requests:
        if request.response and request.url.startswith(API_ENDPOINT):
            for key in request.headers:
                if re.match(HEADER_REGEX, key, re.I):
                    headers[key] = request.headers[key]

    # write to file
    f = open("headers.json", "w")
    json.dump(headers, f)
    driver.quit()
    f.close()

    print("Done fetching headers!")


def process_reservation(first_name, last_name, confirmation_number, email):
    print(first_name, last_name, confirmation_number, email)
