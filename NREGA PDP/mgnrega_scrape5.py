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
driver.find_element_by_xpath(".//*[contains(text(), 'Total households completed')]").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox1']/option[@value='Period_wise_msr.per10']").click()

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

data_frame.to_csv('report_8.csv', index = False)

os.system('say "Done with dropdown 1-10"')

driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[contains(text(), 'Total households completed')]").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox1']/option[@value='Period_wise_msr.per20']").click()

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

data_frame.to_csv('report_9.csv', index = False)

os.system('say "Done with dropdown 11-20"')

driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[contains(text(), 'Total households completed')]").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox1']/option[@value='Period_wise_msr.per30']").click()

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

data_frame.to_csv('report_10.csv', index = False)

os.system('say "Done with dropdown 21-30"')

driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[contains(text(), 'Total households completed')]").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox1']/option[@value='Period_wise_msr.per40']").click()

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

data_frame.to_csv('report_11.csv', index = False)

os.system('say "Done with dropdown 31-40"')

driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[contains(text(), 'Total households completed')]").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox1']/option[@value='Period_wise_msr.per50']").click()

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

data_frame.to_csv('report_12.csv', index = False)

os.system('say "Done with dropdown 41-50"')

driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[contains(text(), 'Total households completed')]").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox1']/option[@value='Period_wise_msr.per60']").click()

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

data_frame.to_csv('report_13.csv', index = False)

os.system('say "Done with dropdown 51-60"')

driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[contains(text(), 'Total households completed')]").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox1']/option[@value='Period_wise_msr.per70']").click()

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

data_frame.to_csv('report_14.csv', index = False)

os.system('say "Done with dropdown 61-70"')

driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[contains(text(), 'Total households completed')]").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox1']/option[@value='Period_wise_msr.per80']").click()

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

data_frame.to_csv('report_15.csv', index = False)

os.system('say "Done with dropdown 71-80"')

driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[contains(text(), 'Total households completed')]").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox1']/option[@value='Period_wise_msr.per90']").click()

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

data_frame.to_csv('report_16.csv', index = False)

os.system('say "Done with dropdown 81-90"')

driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[contains(text(), 'Total households completed')]").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox1']/option[@value='Period_wise_msr.per100']").click()

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

data_frame.to_csv('report_17.csv', index = False)

os.system('say "Done with dropdown 100"')

driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[contains(text(), 'Total households completed')]").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox1']/option[@value='Period_wise_msr.per110']").click()

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

data_frame.to_csv('report_18.csv', index = False)

os.system('say "Done with dropdown greater than 100"')

driver.get("https://nregarep2.nic.in/netnrega/dynamic2/DynamicReport_new4.aspx")

# Select for Expenditure Details
driver.find_element_by_xpath(".//*[contains(text(), 'Total households completed')]").click()
driver.find_element_by_xpath("//select[@id='DdlstTxtBox1']/option[@value='Period_wise_msr.per14']").click()

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

data_frame.to_csv('report_19.csv', index = False)

os.system('say "Done with dropdown greater than 14"')
