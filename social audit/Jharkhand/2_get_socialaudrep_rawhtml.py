import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import csv
import pandas as pd
#import MySQLdb
import datetime
import warnings
import sys
import os
import numpy as np
import json
import time
import re
from urllib.parse import unquote

'''
Selenium Scrapper to get data from NREGA MIS Report 9 Social Audit and store in an csv file.
After a successful run 7 files will be outputted, the panchayat-audit data file, panchayat-audit-auditteam data file,
panchayat-audit-auditissueWorks file, panchayat-audit-auditissueJC file, 
and panchayat-audit-auditissue file, 
a file contaning records with website access errors, a file contaning html parse errors.

written by: Wendy Wong 
last updated: February 22, 2019
'''

def get_audrep_html(BASE_URL, statecode, distcode, blockcode, panchcode,gscode):
    driver = webdriver.Firefox(options=options, executable_path = '/Users/samuelsolomon/Documents/WebDriver/geckodriver')
    #driver = webdriver.Firefox(options=options)

    #driver = webdriver.Chrome(options=chrome_options)
   #driver = webdriver.Chrome(options=chrome_options, executable_path='/home/wendywong/Documents/chrome76/chromedriver') 
    driver.implicitly_wait(10)
    driver.set_window_size(1280,1024)
    #select panchayat from dropdowns and 'Proceed'
    #yr_option = driver.find_elements_by_css_selector("#ctl00_ContentPlaceHolder1_ddlFin option[value='"+YEARS+"']")
    driver.get(BASE_URL)
    print("Arrived at Base URL!")
    wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ddlstate"]/option[2]')))
    select = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlstate'))
    select.select_by_value(statecode)
    print("Selected state")
    wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ddldistrict"]/option[2]')))
    select = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddldistrict'))
    select.select_by_value(distcode)
    print("Selected district")
    wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ddlBlock"]/option[2]')))
    select = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlBlock'))
    select.select_by_value(blockcode)
    print("Selected block")
    wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ddlPanchayat"]/option[2]')))
    select = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlPanchayat'))
    select.select_by_value(panchcode)
    print("Selected panchayat")
    wait = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ddlGSDate"]/option[2]')))
    #wait = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ddlGSDate"]/option[@value="'+str(gscode)+'"]')))
    select = Select(driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ddlGSDate"]'))
    select.select_by_value(gscode)
    print("Selected GS code, then wait")
    time.sleep(8) #BUG: for some unknown reason, we can't select gscode when building in sleep time only; need to select gscode first then sleep then select gscode again. Has worked consistently for a few consecutive tries, but error could still pop up...
    select = Select(driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ddlGSDate"]'))
    select.select_by_value(gscode)
    wait = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_lblSA_start_dt"]')))
    print("Selecting again by GS code..")
    #time.sleep(8)
    
    return(driver)

def get_issue_html(table_issues):
    os.chdir(outputPath + 'issues')
    if table_issues != '':
        for j in range(1,len(table_issues)):
            if j<10:
                num = '0'+str(j)
            else:
                num = str(j)
            issuenum = '' if table_issues[j].findChildren('td')[1] is None else table_issues[j].findChildren('td')[1].text.strip()
            issueid = 'ctl00_ContentPlaceHolder1_Repeater3_ctl'+num+'_btnView'
            driver.find_element_by_id(issueid).click()
            wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_grd_RespondIssueDetail"]')))
            time.sleep(5)
            issuedetsoup=BeautifulSoup(driver.page_source, "html.parser")
            raw_issue = open(panchcode+'_'+gsdate.replace("/","_")+'_'+issuenum+'.html','w+',encoding='utf-8-sig', newline='\n')
            raw_issue.write(issuedetsoup.prettify())
            raw_issue.close()
            print('Grabbed issue '+str(j)+'/'+str(len(table_issues)))
            closebtn = 'btnCloseModel'
            wait = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="btnCloseModel"]')))
            driver.find_element_by_id(closebtn).click()
    
    os.chdir("..")



chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--log-level=3") 

#set directory
#project = 'C:/Users/doubl/Documents/Dropbox/UChicago/00 - Current Courses/EPoD India/NREGA MIS and auditing/Jharkhand social audit/Analysis/Raw Data/socialaudit_rep/'
workingDirectory = os. getcwd()
if "/Users/samuelsolomon" in workingDirectory:
    project = '/Users/samuelsolomon/Dropbox/NREGA Data visualization/NREGA_Payment_Delay/06_Data/01_Code/Social Audits/Wendy/'
elif "/gpfs/loomis/project/pande/ss3889" in workingDirectory:
    project = '/Users/samuelsolomon/Dropbox/NREGA Data visualization/NREGA_Payment_Delay/06_Data/01_Code/Social Audits/Wendy/'


outputPath = project + 'data/raw_data/raw_html/'
os.chdir(outputPath)

#webdriver options
options = Options()
options.add_argument("--headless")
options.add_argument("--log-level=3")

#may have to update the url using link accessed from local computer
BASE_URL = 'http://mnregaweb4.nic.in/netnrega/SocialAuditFindings/SA-GPReport.aspx?page=S&lflag=eng&state_name=JHARKHAND&state_code=34&fin_year=2019-2020&source=national&Digest=nAW75GZcSq7wwuQ9UFJOeA'

#initiate datafiles
g = open(project+'data/raw_data/socialauditrep_apierror1.csv','a',encoding='utf-8-sig', newline='')
writeapierror = csv.writer(g)
if len(sys.argv)!=2: 
  writeapierror.writerow(["state_code",
                          "dist_code",
                          "block_code",
                          "panch_code", 
                          "x",
                          "gs_code",
                           "error_type"
                          ])
h = open(project+'data/raw_data/socialauditrep_issueapierror1.csv','a',encoding='utf-8-sig', newline='')
writeissueapierror = csv.writer(h)
if len(sys.argv)!=2: 
  writeissueapierror.writerow(["state_code",
                          "dist_code",
                          "block_code",
                          "panch_code", 
                          "x",
                          "gs_code",
                           "error_type"
                          ])


#initiate live error-tracking   
api_error_list = []
issueapi_error_list = []
error_count = 0


#load panch codes
codes = pd.read_csv(project+'data/raw_data/socialauditrep_codes_2019-2020.csv',dtype={'district_code':object,'district_name':object,'block_code':object,'block_name':object,'panchayat_code':object,'panchayat_name':object,'gsdate_code':object,'gsdate':object})
codes = codes[codes.gsdate_code != '0'] #remove panchayats without a report
#codes = codes[codes.panchayat_code.isin(codes_error)] #filter panch_codes not scraped and newly uploaded

#SMS only keep first 5 rows -- to debug
#codes = codes.head(5)

if len(sys.argv)==2: #distcode last_panch
    start_panch_index = codes.index[codes.panchayat_code==sys.argv[1]].values[0]
    end_panch_index = max(codes.index.values)
    codes = codes.loc[start_panch_index:end_panch_index]

codes = codes.to_dict(orient='records')
for x in range(len(codes)): 
    code = codes[x]
    statecode = str(code['state_code'])
    distcode = code['district_code']
    distname = code['district_name']
    blockcode = code['block_code']
    blockname = code['block_name']
    panchcode = code['panchayat_code']
    panchname = code['panchayat_name']
    gscode = code['gsdate_code']
    gsdate = code['gsdate']
    print(panchcode, x, '/', len(codes))
    
    for i in range(0, 3):
        api_success = 0
        try:
            driver.quit()
            driver.quit()
            driver.quit()
        except:
            print('No drivers open')
        try:
            driver = get_audrep_html(BASE_URL,statecode,distcode,blockcode,panchcode,gscode)
            #issueid = 'ctl00_ContentPlaceHolder1_Repeater3_ctl01_btnView'
            #driver.find_element_by_id(issueid).click()
            #wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_divIssue"]')))
           
        except Exception as error:
            if i == 2:
                api_error_list.append("API error for panch {}: {}".format(panchcode, str(error)))
                writeapierror.writerow([statecode,
                                        distcode,
                                        blockcode,
                                        panchcode,
                                        x,
                                        gscode,
                                        str(error)
                                        ])  
                error_count += 1
                break
            else:
                continue
        else:
            api_success = 1
            break

    if api_success == 1:
        response=BeautifulSoup(driver.page_source, "html.parser")
        raw_data = open(panchcode+'_'+gsdate.replace("/","_")+'.html','w+',encoding='utf-8-sig', newline='\n')
        raw_data.write(response.prettify())
        raw_data.close()
        souptable = response.findAll("table")
        if len(souptable)!=6:
            table_issues = ''
        elif len(souptable)==6:
            table_issues = souptable[5].findChildren("tr")
        for i in range(0, 3):
            try:
                get_issue_html(table_issues)
            except Exception as error:
                if i == 2:
                    issueapi_error_list.append("Issue API error for panch {}: {}".format(panchcode,str(error)))
                    writeissueapierror.writerow([statecode,
                                            distcode,
                                            blockcode,
                                            panchcode,
                                            x,
                                            gscode,
                                            str(error)
                                            ])  
                    error_count += 1
                    break
                else:
                    driver.quit()
                    driver = get_audrep_html(BASE_URL,statecode,distcode,blockcode,panchcode,gscode)
                    response = BeautifulSoup(driver.page_source, "html.parser")
                    souptable = response.findAll("table")
                    print('Site timeout, restart from panchayat API: ', panchcode)
            else:
                break

    g.flush()
    os.fsync(g.fileno())
    h.flush()
    os.fsync(h.fileno())
    driver.quit()
 
g.close()
h.close()
print(api_error_list)
print(error_count)

print("FINISHED running code")
