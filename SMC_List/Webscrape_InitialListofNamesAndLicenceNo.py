import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def click(page_number):
    """ Click the hyperlink of provided page_number 
    """
    driver.find_element_by_xpath(
        f'//a[@href="javascript:gotoPageDEFAULT({page_number})"]'
    ).click()
    return


def find_result(i):
    """ Finding result for each row/record
    """
    result = driver.find_element_by_xpath(
        f'//*[@id="searchResultHead"]/table[1]/tbody/tr[{i}]/td/div[1]'
    ).text
    return result


def save_names_and_smc(index):
    """ Saved the names and SMC number for each page to a CSV file
    """
    HCP_names_dict = {"name": [], "licence_no": [], "index": [], "real_index": []}
    searchResult = driver.find_element_by_xpath('//*[@id="searchResultHead"]').text
    range_of_record = re.search(r"\d*\s-\s\d*", searchResult)[0]
    i = 1
    try:
        result = find_result(i)
        while result:
            licence_no = re.findall(r"[A-Z]*\d{4,5}[A-Z]", result)[0]
            name = result.replace(licence_no, "").strip("()").strip()

            HCP_names_dict["name"].append(name.strip())
            HCP_names_dict["licence_no"].append(licence_no.strip())
            HCP_names_dict["index"].append(range_of_record)
            HCP_names_dict["real_index"].append(i + (index * 10))
            i += 1
            result = find_result(i)
    except:
        pass

    df = pd.DataFrame(data=HCP_names_dict)
    df.to_csv(f"{FILENAME}", mode="a", header=False, index=True)


def get_last_page():
    """ Get last page of the records
    """
    WebDriverWait(driver, waittime).until(
        EC.presence_of_element_located((By.XPATH, "//a[@class='pagination']"))
    )
    all_pages = driver.find_elements_by_xpath("//a[@class='pagination']")

    # Get 'Last' hyperlink
    last_item = all_pages[-1].get_attribute("href")

    # Keep only the number of last page
    last_page = int(re.sub("[^0-9]", "", last_item))
    return last_page


if __name__ == "__main__":
    hcp_body = "SMC"
    FILENAME = input("Please enter your desired filename:") + ".csv"
    URL = f"https://prs.moh.gov.sg/prs/internet/profSearch/main.action?hpe={hcp_body}"

    waittime = 20
    sleeptime = 1
    page_number = 48

    options = webdriver.ChromeOptions()

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
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("ignore-certificate-errors")
    options.add_argument("--window-size=1420,1080")
    options.add_argument("--disable-gpu")
    options.add_argument(f"user-agent={user_agent}")

    # path to the chromedriver in your computer
    path = "C:\Program Files (x86)\chromedriver.exe"

    driver = webdriver.Chrome(path, options=options)
    driver.get(URL)

    # Switch to frame which contains the HTML for the search section
    driver.switch_to.frame(driver.find_element_by_name("msg_main"))

    # Click Search button to load all results
    WebDriverWait(driver, waittime).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='btnSearch']"))
    ).click()
    WebDriverWait(driver, waittime).until(
        EC.presence_of_element_located((By.XPATH, "//a[@class='pagination']"))
    )

    last_page = get_last_page()

    # loop from 2nd page to last page
    for idx, page_number in zip(range(0, last_page), range(2, last_page + 2)):
        if page_number == last_page + 1:
            save_names_and_smc(idx)
        save_names_and_smc(idx)
        click(page_number)

