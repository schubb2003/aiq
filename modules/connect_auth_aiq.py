#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.7 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import time
import sys
import requests
from selenium import webdriver

AIQ_URL = "https://activeiq.solidfire.com/json-rpc/2.0"
BASE_AIQ = "https://activeiq.solidfire.com/#/dashboard"

def web_login(user, user_pass):
    """
    Open browser via selenium, walks through Firefox, then Edge (chromium),
    then Chrome
    """
    try:
        driver = webdriver.Firefox()
        driver.get(BASE_AIQ)
    except Exception as ff_except:
        try:
            driver = webdriver.Edge()
            driver.get(BASE_AIQ)
        except Exception as edge_except:
            try:
                driver = webdriver.Chrome()
                driver.get(BASE_AIQ)
            except Exception as chrome_except:
                print(f"No suitable drivers found, script will exit."
                      f"\n\n{ff_except}\n\n{edge_except}\n\n{chrome_except}")
                sys.exit(1)
    time.sleep(5)
    username = driver.find_element_by_name("user")
    username.clear()
    username.send_keys(user)
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(user_pass)
    driver.find_element_by_class_name("button").click()
    time.sleep(3)
    my_cookies = driver.get_cookies()
    for cookie in my_cookies:
        if cookie['name'] == "activeiq.session":
            auth_cookie = "activeiq.session=" + cookie['value']
            driver.close()
            return auth_cookie
        else:
            print(f"\nInvalid credentials, please try again")
            driver.close()
            sys.exit(1)


def build_headers(auth_cookie):
    """
    Build the headers for authorization
    """
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'cookie': auth_cookie
        }
    return headers


def build_connect(headers, payload):
    """
    Connect to AIQ
    """
    try:
        response = requests.post(url=AIQ_URL, headers=headers, json=payload)
        response_json = response.json()
        return response_json
    except MemoryError:
        print(f"Data size returned is too large, please select an "
              f"individual cluster to search on.")

def main():
    """
    Nothing here as this is a module
    """
    print(f"This is a support module and has no output of its own")

if __name__ == "__main__":
    main()
