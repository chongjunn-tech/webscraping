from selenium import webdriver
from selenium.webdriver.common.alert import Alert

from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from datetime import date

def get_text_or_None(driver,xmlpath):
    '''
    Handling Exceptions for webscraping
    '''
    try:
        result = driver.find_element_by_xpath(xmlpath).text
    except Exception:
        result = None
    return result

if __name__=='__main__':
    path = "C:\Program Files (x86)\chromedriver.exe"
    driver=webdriver.Chrome(path)
    df_links = pd.read_csv('listoflinks.csv',)
    alldetails=[]


    for link in tqdm(df_links.values):
        driver.get(link[0])
        
        # getting thes required information 
        name=get_text_or_None(driver,'/html/body/div/div[2]/div/div/div[3]/h1')  
        tel=get_text_or_None(driver,'/html/body/div/div[2]/div/div/div[3]/table[1]/tbody/tr[1]/td[1]/span[1]/a')   
        fax=get_text_or_None(driver,'/html/body/div/div[2]/div/div/div[3]/table[1]/tbody/tr[2]/td[1]')
        l_name=get_text_or_None(driver,"/html/body/div/div[2]/div/div/div[3]/table[1]/tbody/tr[1]/td[3]")
        l_period=get_text_or_None(driver,"/html/body/div/div[2]/div/div/div[3]/table[1]/tbody/tr[2]/td[3]")
        HCI=get_text_or_None(driver,"/html/body/div/div[2]/div/div/div[3]/table[1]/tbody/tr[3]/td[3]")
        UEN=get_text_or_None(driver,"/html/body/div/div[2]/div/div/div[3]/table[1]/tbody/tr[4]/td[3]")
        dr=get_text_or_None(driver,"/html/body/div/div[2]/div/div/div[3]/table[2]/tbody/tr[2]/td[1]")
        dr_qual=get_text_or_None(driver,"/html/body/div/div[2]/div/div/div[3]/table[2]/tbody/tr[2]/td[2]/li")
        svc=get_text_or_None(driver,"/html/body/div/div[2]/div/div/div[3]/table[3]/tbody/tr/td")
        address=get_text_or_None(driver,"/html/body/div/div[2]/div/div/div[4]/div[1]/p")

        # saving information 
        temp={"nameofclinic":name,
            "telephone":tel,
            "fax":fax,
            "licensee_name":l_name,
            "Licence Period":l_period,
            "HCI Code":HCI,
            "UEN":UEN,
            "Doctor/Dentist":dr,
            "qualification":dr_qual,
            "detailsofservices":svc,
            "address":address,
            "hyperlink":link}
        
        alldetails.append(temp)

    today = date.today()


    df=pd.DataFrame(alldetails)
    filename = "Listing_of_Licensed_Clinic_"+str(today)+".csv"
    df.to_csv(filename)
    print(f'Data has been saved as {filename} into your local directory')
