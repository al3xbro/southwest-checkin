import time
import re
import json
import requests

import configparser

from apscheduler.schedulers.background import BackgroundScheduler

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


config = configparser.ConfigParser()
config.read('config.ini')
DATABASE_HOST = config.get('Database', 'database_host')
DATABASE_PORT = config.get('Database', 'database_port')
DATABASE_NAME = config.get('Database', 'database_name')
DATABASE_USER = config.get('Database', 'database_user')
DATABASE_PASSWORD = config.get('Database', 'database_password')
TIMEZONE = config.get('App', 'timezone')

scheduler = BackgroundScheduler({
    'apscheduler.jobstores.default': {
        'type': 'sqlalchemy',
        'url': f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}',
    },
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '20',
    },
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '5',
    },
    'apscheduler.timezone': TIMEZONE,
})

# southwest API endpoint and URL; may change
HEADER_FETCH_URL = 'https://mobile.southwest.com/check-in'
CHECKIN_URL = 'https://mobile.southwest.com/api/mobile-air-operations/v1/mobile-air-operations/page/check-in'
# stolen from @byalextran at https://github.com/byalextran/southwest-headers
HEADER_REGEX = 'x-api-key|x-user-experience-id|x-channel-id|^[\w]+?-\w{1,2}$'

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get(HEADER_FETCH_URL)


@scheduler.scheduled_job('interval', hours=12)
def get_headers():

    print('Fetching headers...')

    # start broswer

    # wait for page load
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_element_located((By.NAME, 'recordLocator')) and
        EC.presence_of_element_located((By.NAME, 'firstName')) and
        EC.presence_of_element_located((By.NAME, 'lastName'))
    )

    # fill out form
    confirmation_input = driver.find_element(By.NAME, 'recordLocator')
    first_name_input = driver.find_element(By.NAME, 'firstName')
    last_name_input = driver.find_element(By.NAME, 'lastName')

    confirmation_input.clear()
    confirmation_input.send_keys('RANDRA')

    first_name_input.clear()
    first_name_input.send_keys('Raj')

    last_name_input.clear()
    last_name_input.send_keys('Andra')

    confirmation_input.submit()

    # wait for server response
    time.sleep(1)

    # grab headers
    headers = {}
    for request in driver.requests:
        if request.response and request.url.startswith(CHECKIN_URL):
            for key in request.headers:
                if re.match(HEADER_REGEX, key, re.I):
                    headers[key] = request.headers[key]

    # write to file
    if headers != {}:
        f = open('headers.json', 'w')
        json.dump(headers, f)
        driver.quit()
        f.close()
        driver.quit()
    else:
        print('Error fetching headers. Retrying...')
        get_headers()

    print('Done fetching headers!')


def process_reservation(first_name, last_name, confirmation_number, email):
    with open('headers.json') as f:
        headers = json.load(f)
        headers['Content-Type'] = 'application/json'
        res = requests.post(f'{CHECKIN_URL}/{confirmation_number}', headers=headers, json={
            'firstName': first_name,
            'lastName': last_name,
            'recordLocator': confirmation_number,
        })
        print(headers)
        print(res.json())
