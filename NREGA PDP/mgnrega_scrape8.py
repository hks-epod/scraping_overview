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
# os.makedirs(save_to, exist_ok=True)
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

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[@id='TxtBox5']").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox5']/option[@value='mon_wise_dmd.aprilreg']").click()
driver.find_element_by_xpath(".//*[@id='TxtBox6']").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox6']/option[@value='mon_wise_dmd.aprilapp']").click()
driver.find_element_by_xpath(".//*[@id='TxtBox7']").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox7']/option[@value='mon_wise_empprov.aprilreg']").click()
driver.find_element_by_xpath(".//*[@id='TxtBox8']").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox8']/option[@value='mon_wise_empprov.aprilapp']").click()

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

data_frame.to_csv('report_27.csv', index = False)

os.system('say "Done with monthwise april"')

driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[@id='TxtBox5']").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox5']/option[@value='mon_wise_dmd.mayreg']").click()
driver.find_element_by_xpath(".//*[@id='TxtBox6']").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox6']/option[@value='mon_wise_dmd.mayapp']").click()
driver.find_element_by_xpath(".//*[@id='TxtBox7']").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox7']/option[@value='mon_wise_empprov.mayreg']").click()
driver.find_element_by_xpath(".//*[@id='TxtBox8']").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox8']/option[@value='mon_wise_empprov.mayapp']").click()

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

data_frame.to_csv('report_28.csv', index = False)

os.system('say "Done with monthwise may"')

driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[@id='TxtBox5']").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox5']/option[@value='mon_wise_dmd.junereg']").click()
driver.find_element_by_xpath(".//*[@id='TxtBox6']").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox6']/option[@value='mon_wise_dmd.juneapp']").click()
driver.find_element_by_xpath(".//*[@id='TxtBox7']").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox7']/option[@value='mon_wise_empprov.junereg']").click()
driver.find_element_by_xpath(".//*[@id='TxtBox8']").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox8']/option[@value='mon_wise_empprov.juneapp']").click()

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

data_frame.to_csv('report_29.csv', index = False)

os.system('say "Done with monthwise june"')
