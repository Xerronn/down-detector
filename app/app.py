import requests
import time
from collections import namedtuple

from credentials import token, users

baseURL = "https://slack.com/api/chat.postMessage?channel="
WebsiteStatus = namedtuple('WebsiteStatus', ['status_code', 'reason'])
names = ['vizbot.io', 'boulderinsightgroup.com']


def get_status(site):
    try:
        response = requests.head(site, timeout=5)
        status_code = response.status_code
        reason = response.reason
    except requests.exceptions.ConnectionError:
        status_code = '000'
        reason = 'ConnectionError'
    website_status = WebsiteStatus(status_code, reason)
    return website_status

while(True):
    for name in names:
        site = 'http://www.{}'.format(name)
        website_status = get_status(site)
        print("{0:30} {1:10} {2:10}"
            .format(site, website_status.status_code, website_status.reason))
        
        #SLACK MESSAGE
        if (int(website_status.status_code) != 000):
            for user in users:
                message = f"*IMMEDIATE ACTION REQUIRED*\n {site} is not responding!!"
                url = baseURL + user + "&token=" + token + "&text=" + message + "&pretty=1"

                requests.post(url)
                
    time.sleep(5)