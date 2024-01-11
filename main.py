import requests
from bs4 import BeautifulSoup
import time
from plyer import notification
from datetime import datetime
import pytz
import threading

def get_time():
  tokyo_timezone = pytz.timezone('Asia/Tokyo')
  return datetime.now(tz=tokyo_timezone).strftime("%H:%M:%S")

def display_loading():
  animation = "|/-\\"
  i = 0
  while True:
    print(get_time() + " " + animation[i % len(animation)], end="\r", flush=True)
    i += 1
    time.sleep(0.1)

def findKey():
  response = requests.get("https://www.peopleperhour.com/freelance-jobs/technology-programming")
  soup = BeautifulSoup(response.text, "html.parser")
  return soup.find("div", {'class': "list⤍List⤚3R-r9"}).find('a', {'class': 'item__url⤍ListItem⤚20ULx'}).get("href").strip()

def check_page():
  global pre
  pre = findKey()
  while True:
    if findKey() != pre:
      notification.notify(
        title='PeoplePerHour',
        message= "The page has been updated! " + get_time(),
        app_name='Py Bot',
        timeout=0
      )
      pre = findKey()
      print("\n")
      print(get_time() + " <--------> " + pre)
    time.sleep(30) 

loading_thread = threading.Thread(target=display_loading)
check_page_thread = threading.Thread(target=check_page)

loading_thread.start()
check_page_thread.start()