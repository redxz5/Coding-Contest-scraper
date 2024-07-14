import re
import requests
import logging
from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
from webdriver_manager.chrome import ChromeDriverManager
from pickle import dump
from os import makedirs, path, getcwd

temp_dir = path.join(getcwd(),"source\\temp")
makedirs(temp_dir, exist_ok=True)

gfg_url = "https://www.geeksforgeeks.org/events?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=contests"

def setup_selenium():
    seleniumLogger.setLevel(logging.INFO)

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    
    global driver
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
        )

logging.basicConfig(filename="./source/temp/log.log",
                    format='%(levelname)s - %(asctime)s - %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class ContestInfo:
    def __init__(self,name,date,time):
        self.name = name
        self.date = date
        self.time = time
      
def check_internet_connection():
    try:
        response = requests.get("https://www.google.com/", timeout=5)
        return True
    except requests.ConnectionError:
        return False  

def get_URL(URL):
    if (check_internet_connection == False):
        logger.critical("Internet is down")
    else:
        try:
            return requests.get(URL)
        except:
            logger.debug("Site may be down / URL is wrong / Net is slow")
            return False

def check_element(url,wait_time):
    driver.get(url)
    delay = wait_time
    txt = str(driver.page_source)
    element_name = ""    
    try:
        x = txt.find("eventsLanding_eachEventContainer")
        if(x==-1):
                raise Exception("Element could not be loaded. Perhaps the name/container has changed or Net is slow")
        
        while(txt[x]!='"'):
            element_name+=txt[x]
            x+=1
    
    except Exception as e:
        logger.debug(e)
        print(e)
        return False

    print(x,len(txt))
    
    return element_name

def create_list(contests):
    data = []
    for elements in contests:
        lst = elements.split('\n')
        if len(lst)==4:
            data.append(ContestInfo(name=lst[3],
                                    date=lst[1],
                                    time=lst[2]))
        else:
            data.append(ContestInfo(name=lst[2],
                                    date=lst[0],
                                    time=lst[1]))
    
    return data

def scrape_gfg(url):
    element_name = check_element(url,10)
    if(element_name == False):
        print("Check the log.log file")
        return
    print("\n\n\n")
    content = driver.find_elements("id",element_name)
    
    data = [item.text for item in content]
    data = create_list(data)
    return data

def add_contests(name,all):
    for contests in name:
        all.append(contests)
    # return all

def print_contests(List):
    for contest in List:
        print(f"Name : {contest.name}")
        print(f"Date : {contest.date}")
        print(f"Time : {contest.time}")
        print()   

def fetch():
    setup_selenium()
    all_contests = []
    gfg = get_URL(gfg_url)
    if(gfg != False):
        gfg_contests = scrape_gfg(gfg_url)
        add_contests(gfg_contests,all_contests)
    else:
        logger.log("Error Occured")

    with open("./source/temp/data.pkl",'wb') as f:
        dump(all_contests,f)

if __name__ == '__main__':
    fetch()
    print("---------------PROGRAM ENDED--------------")
