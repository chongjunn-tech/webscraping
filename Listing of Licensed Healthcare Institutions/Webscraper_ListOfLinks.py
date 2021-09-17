from selenium import webdriver
from selenium.webdriver.common.alert import Alert

from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

 ## Getting the link of URLs

## webdriver saved in this path (you may alter the path based on where it is saved in your system)
## download chromedriver to match your own google chrome version in https://chromedriver.chromium.org/downloads
path="C:\Program Files (x86)\chromedriver.exe"
driver=webdriver.Chrome(path)
driver.get("http://www.hcidirectory.gov.sg/hcidirectory/")

listoflinks=[]

dummy=driver.find_element_by_id("search_btn")
dummy.click()

condition=True

while condition:
    results=driver.find_elements_by_class_name("name")
    for result in results:
        link=result.find_element_by_tag_name("a").get_property('href')
        listoflinks.append(link)
    try:
        next_button=driver.find_element_by_class_name("r_arrow")
        next_button.click()
    except:
        condition=False

# Saving the list of hyperlinks as a csv file 
df_links=pd.DataFrame(listoflinks)
df_links.to_csv('listoflinks.csv',index=False)
