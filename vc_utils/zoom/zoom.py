# coding: utf-8
# Initiate preparatory work for livestreaming
# Send over PATCH requests to Zoom's server
# Created by James Raphael Tiovalen (2020)

# Import libraries
import sys
import time
import base64
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import requests
import settings

# Get user authorization code and access token
auth_code_url = f"https://zoom.us/oauth/authorize?response_type=code&client_id={settings.client_id}&redirect_uri={settings.redirect_uri}"
webdriver_exists = False

for WEB_DRIVER in (webdriver.Firefox, webdriver.Chrome):
    try:
        driver = WEB_DRIVER()
        driver.quit()
        webdriver_exists = True
        break
    except WebDriverException as e:
        pass

if not webdriver_exists:
    print("No webdriver found! Quitting...")
    sys.exit(1)

if isinstance(driver, webdriver.firefox.webdriver.WebDriver):
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
elif isinstance(driver, webdriver.chrome.webdriver.WebDriver):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

driver.get(auth_code_url)
invalid_msg = ""
while invalid_msg == "":
    try:
        invalid_msg = driver.find_element_by_css_selector("span.error-message").text
    except NoSuchElementException as e:
        print("Waiting for a successful login...")
        time.sleep(1)
    except WebDriverException as e:
        if str(e) == "Message: Failed to decode response from marionette\n":
            print("The webdriver browser has been closed. Quitting...")
        elif str(e) == "Message: Browsing context has been discarded\n":
            print("The monitored Zoom login page tab has been closed. Quitting...")
        else:
            print(str(e))
        driver.quit()
        sys.exit(1)

print("")

try:
    assert invalid_msg == "Invalid client_id: (4,700)"
except AssertionError as e:
    print("Something went wrong after logging in! Quitting...")
    driver.quit()
    sys.exit(1)

auth_code = driver.current_url[37:]
driver.quit()

oauth_url = f"https://zoom.us/oauth/token?code={auth_code}&grant_type=authorization_code&redirect_uri={settings.redirect_uri}"
base64_client = base64.b64encode(
    f"{settings.client_id}:{settings.client_secret}".encode("ascii")
).decode("ascii")
oauth_header = {"Authorization": f"Basic {base64_client}"}
response = requests.request("POST", oauth_url, headers=oauth_header)

try:
    assert response.status_code == 200
except AssertionError as e:
    print(
        "Something went wrong when requesting for the OAuth Access Token! Quitting..."
    )
    sys.exit(1)

result = response.json()
access_token = result["access_token"]
refresh_token = result["refresh_token"]

# Send PATCH requests
update_url = f"https://api.zoom.us/v2/meetings/{settings.meeting_id}/livestream"
status_url = f"https://api.zoom.us/v2/meetings/{settings.meeting_id}/livestream/status"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}

update_payload = {
    "stream_url": f"{settings.stream_url}",
    "stream_key": f"{settings.stream_key}",
    "page_url": f"{settings.page_url}",
}
start_live_payload = {
    "action": "start",
    "settings": {"active_speaker_name": True, "display_name": "inc"},
}

response = requests.request("PATCH", update_url, json=update_payload, headers=headers)
try:
    assert response.status_code == 204
except AssertionError as e:
    print("Something went wrong when updating the livestream details on Zoom!\n")
    print("Please ensure that the Zoom Meeting has been started! Quitting...")
    sys.exit(1)

response = requests.request(
    "PATCH", status_url, json=start_live_payload, headers=headers
)
try:
    assert response.status_code == 204
except AssertionError as e:
    print("Something went wrong when trying to start the livestream!\n")
    print(
        "Please ensure that the details specified in settings.py are valid and that all the steps so far have been closely and correctly followed! Quitting..."
    )
    sys.exit(1)

print("The livestream has been successfully started! Yay!")
print("Processing of the livestream data can begin accordingly.")
print("To end the livestream, simply end the Zoom Meeting.\n")
print("Have fun! :D")