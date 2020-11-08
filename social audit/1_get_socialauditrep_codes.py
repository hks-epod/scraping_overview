# -*- coding: utf-8 -*-

import pandas as pd
#import MySQLdb
import datetime
import warnings
import sys
import os
import numpy as np
import requests
import json
import csv
import time
import re
from bs4 import BeautifulSoup

error_count = 0

#set directory
project = '/Users/samuelsolomon/Dropbox/NREGA Data visualization/NREGA_Payment_Delay/06_Data/01_Code/Social Audits/Wendy/'
    
#arrival link for Jharkhand panchayat level social audit reports

#finyear = ['2016-2017','2017-2018','2018-2019','2019-2020']
finyear = ['2019-2020']

instance = {
        '2016-2017': {'addr': 'http://mnregaweb4.nic.in/netnrega/SocialAuditFindings/SA-GPReport.aspx?page=S&lflag=eng&state_name=JHARKHAND&state_code=34&fin_year=2016-2017&source=national&Digest=q+bg/rruthBTaQdhaxoiNA'},
        '2017-2018': {'addr': 'http://mnregaweb4.nic.in/netnrega/SocialAuditFindings/SA-GPReport.aspx?page=S&lflag=eng&state_name=JHARKHAND&state_code=34&fin_year=2017-2018&source=national&Digest=r9lqHZ2kwmfFLbdhYTkZJw'},
        '2018-2019': {'addr': 'http://mnregaweb4.nic.in/netnrega/SocialAuditFindings/SA-GPReport.aspx?page=S&lflag=eng&state_name=JHARKHAND&state_code=34&fin_year=2018-2019&source=national&Digest=iXkrYrHq7feaXrcsr1JeHg'},
        '2019-2020': {'addr': 'http://mnregaweb4.nic.in/netnrega/SocialAuditFindings/SA-GPReport.aspx?page=S&lflag=eng&state_name=JHARKHAND&state_code=34&fin_year=2019-2020&source=national&Digest=nAW75GZcSq7wwuQ9UFJOeA'},
        }


headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }

for y in finyear:
    print(y)
    f = open(project+'data/raw_data/socialauditrep_codes_'+y+'.csv','a', encoding="utf8",newline='')
    writer = csv.writer(f)
    writer.writerow(["state_code",
                     "state_name",
                     "district_code",
                     "district_name",                  
                     "block_code", 
                     "block_name", 
                     "panchayat_code",
                     "panchayat_name",
                     "fin_year",
                     "gsdate", #gram sabha or jansunwai date
                     "gsdate_code"
                     ])
    g = open(project+'data/raw_data/socialauditrep_codes_'+y+'_apierror.csv','a',encoding='utf-8-sig', newline='')
    writeapierror = csv.writer(g)
    writeapierror.writerow(["panch code", 
                     "Error type"
                    ])
    
    #get initial eventvalidation and viewstate parameters
    response = requests.get(instance[y]['addr'], timeout=30)
    response = BeautifulSoup(response.content, features = "lxml")
    viewstate = response.find('input', id='__VIEWSTATE').get('value')
    eventval = response.find('input', id='__EVENTVALIDATION').get('value')
    
    data = {    'ctl00$ContentPlaceHolder1$ddlstate': 34,
                '__VIEWSTATE': viewstate,
                '__EVENTVALIDATION': eventval,
                '__VIEWSTATEENCRYPTED': ''
             }
    
    response = requests.post(instance[y]['addr'], data = data, headers = headers, timeout=60)
    response = BeautifulSoup(response.content, features = "lxml")
    viewstate = response.find('input', id='__VIEWSTATE').get('value')
    eventval = response.find('input', id='__EVENTVALIDATION').get('value')
    
    soup = response.find('select', id='ctl00_ContentPlaceHolder1_ddldistrict').findChildren('option')
    districts = {}
    for h in range(1,len(soup)):
        distcode = soup[h].get('value')
        distname = soup[h].text
        districts[distcode] = distname
        
    for i in districts.keys():  
        print(i)
        data = {    'ctl00$ContentPlaceHolder1$ddlstate': 34,
                    'ctl00$ContentPlaceHolder1$ddldistrict': i,
                    
                    '__VIEWSTATE': viewstate,
                    '__EVENTVALIDATION': eventval,
                    '__VIEWSTATEENCRYPTED': ''
                 }
        response = requests.post(instance[y]['addr'], data = data, headers = headers, timeout=60)
        response = BeautifulSoup(response.content, features = "lxml")
        viewstate = response.find('input', id='__VIEWSTATE').get('value')
        eventval = response.find('input', id='__EVENTVALIDATION').get('value')
    
        soup = response.find('select', id='ctl00_ContentPlaceHolder1_ddlBlock').findChildren('option')
        blocks = {}
        for j in range(1,len(soup)):
            blockcode = soup[j].get('value')
            blockname = soup[j].text
            blocks[blockcode] = blockname
        for k in blocks.keys():
            print(k)
            data = {    'ctl00$ContentPlaceHolder1$ddlstate': 34,
                        'ctl00$ContentPlaceHolder1$ddldistrict': i,   
                        'ctl00$ContentPlaceHolder1$ddlBlock': k,
                        
                        '__VIEWSTATE': viewstate,
                        '__EVENTVALIDATION': eventval,
                        '__VIEWSTATEENCRYPTED': ''
                        #NOTES: Need to use viewstate and eventvalidation from previous post request; fields can be used for all blocks within the same districts.
                        }
            response = requests.post(instance[y]['addr'], data = data, headers = headers, timeout=60)
            response = BeautifulSoup(response.content, features = "lxml")
            viewstate = response.find('input', id='__VIEWSTATE').get('value')
            eventval = response.find('input', id='__EVENTVALIDATION').get('value')
    
            soup = response.find('select', id='ctl00_ContentPlaceHolder1_ddlPanchayat').findChildren('option')
            panchayats = {}
            for l in range(1,len(soup)):
                panchcode = soup[l].get('value')
                panchname = soup[l].text
                panchayats[panchcode] = panchname
            for m in panchayats.keys():
                print(m)
                data = {    
                            'ctl00$ContentPlaceHolder1$ddlstate': 34,
                            'ctl00$ContentPlaceHolder1$ddldistrict': i,   
                            'ctl00$ContentPlaceHolder1$ddlBlock': k,
                            'ctl00$ContentPlaceHolder1$ddlPanchayat': m,
                            #'ctl00$ContentPlaceHolder1$ddlGSDate' : '8/28/2017 12:00:00 AM',
                            
                            #'__EVENTTARGET': 'ctl00$ContentPlaceHolder1$Repeater3$ctl12$btnView', #use this param to iterate through each issue, e.g. issue #12
                            '__VIEWSTATE': viewstate,
                            '__EVENTVALIDATION': eventval,
                            '__VIEWSTATEENCRYPTED': ''
                }
                
                for z in range(0, 3):
                    api_success = 0
                    try:
                        response = requests.post(instance[y]['addr'], data = data, headers = headers, timeout=60)            
    
                    except Exception as e:
                        if z == 2:
                            writeapierror.writerow([m,
                                                    str(e)
                                                    ])  
                            error_count += 1
                            break
                        else:
                            continue
                    else:
                        api_success = 1
                        break
    
                if api_success == 1:
                    response = BeautifulSoup(response.content, features = "lxml") 
                    
                    viewstate = response.find('input', id='__VIEWSTATE').get('value')
                    eventval = response.find('input', id='__EVENTVALIDATION').get('value')
        
                    soup = response.find('select', id='ctl00_ContentPlaceHolder1_ddlGSDate').findChildren('option')
                    if len(soup)>1:
                        for n in range(1,len(soup)):
                            gscode = soup[n].get('value')
                            gsdate = soup[n].text
                    else:
                        gscode = soup[0].get('value')
                        gsdate = soup[0].text
                        
                    writer.writerow(['34',
                                     'JHARKHAND',
                                     i,
                                     districts[i],
                                     k,
                                     blocks[k],
                                     m,
                                     panchayats[m],
                                     y,
                                     gsdate,
                                     gscode])
    
            f.flush()
            os.fsync(f.fileno())
            g.flush()
            os.fsync(g.fileno())

    
    f.close()
    g.close()
    
print("FINISHED with code")


