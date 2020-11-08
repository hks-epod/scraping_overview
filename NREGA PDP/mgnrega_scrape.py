# MGNREGA Scraping
#     Website: https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx
#     Author: Hongdi Zhao (hzhao.hks@gmail.com)
#     Date: May 6th 2020
# 
# Instructions
# 
# Download Chrome driver if you dont have it:
# 
# https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.69/
# 
# (Check your chrome version to download the same version of chrome driver)

import sys, os, time, csv
import pandas as pd
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

today = date.today().strftime("%B_%d_%Y")

# You have to create a folder with today's date in the dropbox first before you download the file
save_to = os.getcwd() + "/scrape_job_" + today
os.makedirs(save_to, exist_ok=True)
os.chdir(save_to)

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": save_to}

chromeOptions.add_experimental_option("prefs", prefs)
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("enable-automation")
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--disable-infobars")
chromeOptions.add_argument("--disable-dev-shm-usage")
chromeOptions.add_argument("--disable-browser-side-navigation")
chromeOptions.add_argument("--disable-gpu")

driver = webdriver.Chrome(ChromeDriverManager().install(), options = chromeOptions)
driver.set_page_load_timeout(3000)
driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Download single indicators first
# 
# It takes too long to download all indicators at the same time, thus we seperate these indicators into different downalods. First we download the folloing:
# 
#     Worker participation details
#     Demand for work
#     Allotcation of work
# Select Indicators
# Worker participation details
driver.find_element_by_xpath(".//*[contains(text(), 'Total households applied for job card')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total job cards issued')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total job cards (SC)')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total job cards (ST)')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total job cards (non-SC/ST)')]").click()
# Demand for work
driver.find_element_by_xpath(".//*[contains(text(), 'Total households demanded work')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total persons demanded work')]").click()
# Allocation of work
driver.find_element_by_xpath(".//*[contains(text(), 'Total households allotted work')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total persons allotted work')]").click()

# And then we download the "Employment Provided" indicators:
# 
#     Employment provided: A few cannot be found by text. so I just xpath'd
driver.find_element_by_xpath(".//*[contains(text(), 'Total muster rolls filled')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total households worked')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total persons worked')]").click()
driver.find_element_by_xpath("""//*[@id="ChkLstFieldsWorkerE_3"]""").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total persons with disability')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total households worked (non-SC/ST)')]").click()
driver.find_element_by_xpath("""//*[@id="ChkLstFieldsWorkerE_6"]""").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total SC households worked')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total person-days worked by SCs')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total ST households worked')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total person-days worked by STs')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total land reform/IAY households worked')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total person-days worked by women')]").click()
driver.find_element_by_xpath("""//*[@id="ChkLstFieldsWorkerE_13"]""").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total SC households over 100 day limit')]").click()
driver.find_element_by_xpath(".//*[contains(text(), 'Total ST households over 100 day limit')]").click()

# Select all the india data
driver.find_element_by_xpath("""//*[@id='regionselect']""").send_keys("Block")
driver.find_element_by_xpath(".//*[contains(text(), ' India')]").click()

# Select year
driver.find_element_by_xpath("""//*[@id='DdlstFinYear']""").send_keys("2020-2021")

# Download the data
driver.find_element_by_xpath("""//*[@id="viewDummy"]""").click()

soup = BeautifulSoup(driver.page_source, 'html.parser')
header = soup.find_all("tbody")[1].find_all("tr")[0]
# print(header)
table = soup.find_all("tbody")[1].find_all("tr")[1:]

list_header = []
for items in header:
    try:
#         print(items.get_text())
        list_header.append(items.get_text())
    except:
        continue

table_data = []
for elem in table:
    sub_data = []
    for sub_elem in elem:
        try:
            sub_data.append(sub_elem.get_text())
        except:
            continue
    table_data.append(sub_data)

data_frame = pd.DataFrame(data = table_data, columns = list_header)

data_frame.to_csv('report_1.csv', index = False)

os.system('say "done with chunk 1"')
