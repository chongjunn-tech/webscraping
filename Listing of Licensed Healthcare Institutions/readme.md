# Webscraping on the Listing of Licensed Healthcare Institutions of Singapore
- This listing of Licensed Healthcare Institutions can be accessed on this [link](http://www.hcidirectory.gov.sg/hcidirectory/)

# Documentation of files 

- Webscraper_ListOfLinks.py:Scrape all the hyperlinks that pertains to a specific Licensed Healthcare Institutions and save it into an csv file 'listoflinks.csv'
- Webscraper_AllDetails.py: Scrape the required information from each hyperlink such as name, telephone, fax of healthcare institutions
- chromedriver.exe: webdriver needed for Selenium. Please place the file into the designated path
- listoflinks.csv: Store all the hyperlinks that pertain to a specific Licensed Healthcare Institutions. This is as the webscraping project is time-consuming
