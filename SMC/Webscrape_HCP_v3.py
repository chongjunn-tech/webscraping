import time
import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def find_xpath(xpath):
    return driver.find_element_by_xpath(xpath).text


def generate_dict(index):
    """ Generate a python dictionary with the required information extracted from each doctor's profile

    Args:
        index ([int]): index from Initial List of Names And Licence Number where the dictionary needs to be generated from

    Returns:
        hcp_dict[dict]: Python dictionary with the required information extracted from each doctor's profile
    """
    WebDriverWait(driver, waittime).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='table-head']"))
    )
    hcp_dict = {}
    hcp_dict["index"] = index
    hcp_dict["name"] = find_xpath('//*[@id="profDetails"]/div[1]')
    hcp_dict["reg_number"] = find_xpath(
        '//*[@id="profDetails"]/table/tbody/tr[1]/td[2]'
    )
    try:
        hcp_dict["qualification"] = find_xpath(
            '//*[@id="profDetails"]/table/tbody/tr[2]/td[2]'
        )
    except:
        hcp_dict["qualification"] = None

    try:
        hcp_dict["first_reg_date"] = find_xpath(
            '//*[@id="profDetails"]/table/tbody/tr[3]/td[2]'
        )
    except:
        hcp_dict["first_reg_date"] = None
    try:
        hcp_dict["current_reg"] = find_xpath(
            '//*[@id="profDetails"]/table/tbody/tr[4]/td[2]'
        )
    except:
        hcp_dict["current_reg"] = None
    try:
        hcp_dict["cert_start_date"] = find_xpath(
            '//*[@id="profDetails"]/table/tbody/tr[5]/td[2]'
        )
    except:
        hcp_dict["cert_start_date"] = None
    try:
        hcp_dict["cert_end_date"] = find_xpath(
            '//*[@id="profDetails"]/table/tbody/tr[5]/td[4]'
        )
    except:
        hcp_dict["cert_end_date"] = None

    try:
        hcp_dict["Specialty"] = find_xpath(
            '//*[@id="profDetails"]/div[3]/table/tbody/tr[2]/td[2]'
        )
    except:
        hcp_dict["Specialty"] = None

    try:
        hcp_dict["Family_Physicians"] = find_xpath(
            '//*[@id="profDetails"]/div[3]/table/tbody/tr[4]/td[2]'
        )

    except:
        try:
            hcp_dict["Family_Physicians"] = find_xpath(
                '//*[@id="profDetails"]/div[3]/table/tbody/tr[3]/td[2]'
            )
        except:
            hcp_dict["Family_Physicians"] = None

    try:
        hcp_dict["practice_place_name"] = find_xpath(
            '//*[@id="profDetails"]/div[5]/table/tbody/tr[1]/td[2]'
        )
    except:
        hcp_dict["practice_place_name"] = None
    try:
        text = find_xpath('//*[@id="profDetails"]/div[5]/table/tbody/tr[2]/td[2]')
        address = " ".join(text.split("\n"))
        hcp_dict["practice_place_address"] = address
    except:
        hcp_dict["practice_place_address"] = None

    try:
        hcp_dict["practice_place_phone"] = find_xpath(
            '//*[@id="profDetails"]/div[5]/table/tbody/tr[3]/td[2]'
        )
    except:
        hcp_dict["practice_place_phone"] = None

    return hcp_dict


def search(licence_no, waittime):
    """Remove any input from search field and then input the provided licence number and press 'search'

    Args:
        licence_no ([str]): Licence number of the doctor
        waittime ([int]): Waiting time
    """

    # click More search options
    WebDriverWait(driver, waittime).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="searchProf"]/div[2]/table/tbody/tr[4]/td/a')
        )
    ).click()
    time.sleep(1)
    # clear output if any and input the licence number
    WebDriverWait(driver, waittime).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="getSearchSummary_psearchParamVO_regNo"]')
        )
    ).send_keys(Keys.CONTROL + "a")
    WebDriverWait(driver, waittime).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="getSearchSummary_psearchParamVO_regNo"]')
        )
    ).send_keys(Keys.DELETE)

    WebDriverWait(driver, waittime).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="getSearchSummary_psearchParamVO_regNo"]')
        )
    )
    driver.find_element_by_xpath(
        '//*[@id="getSearchSummary_psearchParamVO_regNo"]'
    ).send_keys(licence_no)

    # press search button
    WebDriverWait(driver, waittime).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="searchProf"]/div[2]/table/tbody/tr[3]/td/input[4]')
        )
    ).click()

    # click view more details to enter to the particular doctor's profile
    WebDriverWait(driver, waittime).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="searchResultHead"]/table[1]/tbody/tr/td/div[2]/a')
        )
    ).click()
    return


def back_to_search():
    """ Return user back to the webpage that allows for Search
    """
    ## trying multiple xpaths to return back to search as it can vary according to the website configuration
    try:
        driver.find_element_by_xpath('//*[@id="profDetails"]/div[6]/a[2]').click()
        return
    except:
        pass
    try:
        driver.find_element_by_xpath('//*[@id="profDetails"]/div[4]/a[2]').click()
        return
    except:
        pass
    try:
        driver.find_element_by_xpath('//*[@id="profDetails"]/div[8]/a[2]').click()
        return
    except:
        pass

    return


def Webscrape_from_saved_file(Initial_List, saved_filename, start_index, waittime):
    """Run webscraping by inputting Licence Number in the search field

    Args:
        Initial_List ([str]): filename of the Initial List of Names And Licence Number
        saved_filename ([str]): filename of the saved file
        start_index ([int]): starting index where webscrape from Initial_List
        waittime ([int]): waiting time 
    """
    df = pd.read_csv(Initial_List)
    total_rows = df.shape[0]
    for idx, series in tqdm(df.iterrows()):
        licence_no = series["licence_number"]
        index = idx + 1  # to start index from 1 instead of 0
        if index >= start_index and licence_no != "End":
            search(licence_no, waittime)
            hcp_dict = generate_dict(index)
            df_hcp_dict = pd.DataFrame(hcp_dict, index=[1])
            df_hcp_dict.to_csv(
                f"{saved_filename}", mode="a", header=False, index_label=["index"]
            )
            print(f" Webscapped Row {index}/{total_rows} of {Initial_List}")
            back_to_search()
    return


if __name__ == "__main__":
    desired_index = int(input("Input desired Row Number:"))
    hcp_body = "SMC"
    saved_filename = input("Input desired filename to be saved:") + ".csv"
    waittime = 60
    InitialListofNamesAndLicenceNo = "SMCList_saved_2021_11_18_v2.csv"
    hyperlink = (
        f"https://prs.moh.gov.sg/prs/internet/profSearch/main.action?hpe={hcp_body}"
    )

    software_names = [SoftwareName.CHROME.value]
    operating_systems = [
        OperatingSystem.WINDOWS.value,
        OperatingSystem.LINUX.value,
    ]
    user_agent_rotator = UserAgent(
        software_names=software_names, operating_systems=operating_systems, limit=100,
    )
    user_agent = user_agent_rotator.get_random_user_agent()
    # Set webdriver options
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("ignore-certificate-errors")
    options.add_argument("--window-size=1420,1080")
    options.add_argument("--disable-gpu")
    options.add_argument(f"user-agent={user_agent}")

    path = "C:\Program Files (x86)\chromedriver.exe"
    # Initiate webdriver
    driver = webdriver.Chrome(path, options=options,)

    # Get driver to retrieve homepage
    driver.get(hyperlink)

    driver.switch_to.frame(driver.find_element_by_name("msg_main"))
    # Click Search button to load all results
    WebDriverWait(driver, waittime).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='btnSearch']"))
    ).click()

    WebDriverWait(driver, waittime).until(
        EC.presence_of_element_located((By.XPATH, "//a[@class='pagination']"))
    )
    Webscrape_from_saved_file(
        InitialListofNamesAndLicenceNo, saved_filename, desired_index, waittime
    )

