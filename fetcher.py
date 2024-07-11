import re
import requests
import logging
from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
from webdriver_manager.chrome import ChromeDriverManager

seleniumLogger.setLevel(logging.INFO)

chrome_options = Options()
chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=chrome_options
    )


logging.basicConfig(filename="log.log",
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
            logger.debug("Site may be down / URL is wrong")
            return False

def check_element(url):
    driver.get(url)
    delay = 5
    txt = str(driver.page_source)
    element_name = ""    
    try:
        x = txt.find("eventsLanding_eachEventContainer")
        if(x==-1):
                raise Exception("Element could not be loaded. Perhaps the name/container has changed")
        
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
        data.append(ContestInfo(lst[2],lst[0],lst[1]))
    
    return data

def scrape_gfg(url):
    element_name = check_element(url)
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
    

gfg_url = "https://www.geeksforgeeks.org/events?itm_source=geeksforgeeks&itm_medium=main_header&itm_campaign=contests"

all_contests = []
gfg = get_URL(gfg_url)
if(gfg != False):
    gfg_contests = scrape_gfg(gfg_url)
    add_contests(gfg_contests,all_contests)
else:
    logger.log("Error Occured")

print_contests(all_contests)
print("---------------PROGRAM ENDED--------------")
