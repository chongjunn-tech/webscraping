## Webscraping on the Listing of Doctors registered under Singapore Medical Council (SMC)
- SMC Website can be accessed on this [link](https://prs.moh.gov.sg/prs/internet/profSearch/main.action?hpe=SMC)

## Documentation of files 

#### Webscrape_InitialListofNamesAndLicenceNo.py: 
  - Create an Initial List of Names and Licence Numbers of all doctors in the SMC website and save it into an csv file.
  - Webscrape_HCP_v3.py will utilise the Licence Number(s) on the saved csv file to input the search field. After searching the relevant Licence Number(s),  the required information from the doctor's records then can be extracted.
 <br></br> 
#### Webscrape_HCP_v3.py: 
  - Scrape all the required information from each person such as Name,Registration Number,Qualifications,Type of first registration/date,Type of current registration/date,Practising Certificate Start Date,Practising Certificate End Date,Specialty/Entry date into the Register of Specialists,Entry date into the Register of Family Physicians,Primary Place of Practice | Department/ Name of Practice Place,Address of Place of Practice and Tel

#### chromedriver.exe: 
  - Webdriver needed for Selenium. Please place the file into the designated path as specified from the Python Program


