from bs4 import BeautifulSoup
import csv
import pandas as pd
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
parse raw html of social audit report issues using beautifulsoup

written by: Wendy Wong 
last updated: February 24, 2020
'''

def parse_issue_html(issuedetsoup,panchcode,gsdate,issue_num_filename,issuewriter,issueWorkwriter,issueJCwriter):
    soupspan = issuedetsoup.findAll("span")
    print('soupspan length is '+ str(len(soupspan)))
    souptable = issuedetsoup.findAll("table")
    state = issuedetsoup.find('span',id = "ctl00_ContentPlaceHolder1_lblstate").text.strip()
    district = issuedetsoup.find('span',id = "ctl00_ContentPlaceHolder1_lbldistrict").text.strip()
    block = issuedetsoup.find('span',id = "ctl00_ContentPlaceHolder1_lblblock").text.strip()
    panch = issuedetsoup.find('span',id = "ctl00_ContentPlaceHolder1_lblpanchayat").text.strip()
    SA_start_date = '' if issuedetsoup.find('span',id = "ctl00_ContentPlaceHolder1_lblSA_start_dt") is None else issuedetsoup.find('span',id = "ctl00_ContentPlaceHolder1_lblSA_start_dt").text.strip()
    SA_end_date = '' if issuedetsoup.find('span',id = "ctl00_ContentPlaceHolder1_lblSA_end_dt") is None else issuedetsoup.find('span',id = "ctl00_ContentPlaceHolder1_lblSA_end_dt").text.strip()

    if len(souptable)<6:
        table_issues = ''               
    else:
        table_issues = souptable[5].findChildren("tr")

    if table_issues != '':
        for j in range(1,len(table_issues)):
            issue_num = '' if table_issues[j].findChildren('td')[1] is None else table_issues[j].findChildren('td')[1].text.strip()   
            if issue_num==issue_num_filename:
                issue_sno = '' if table_issues[j].findChildren('td')[0] is None else table_issues[j].findChildren('td')[0].text.strip()
                issue_type = '' if table_issues[j].findChildren('td')[2] is None else table_issues[j].findChildren('td')[2].text.strip()
                issue_desc = '' if table_issues[j].findChildren('td')[3] is None else table_issues[j].findChildren('td')[3].text.strip()
                issue_amt = '' if table_issues[j].findChildren('td')[4] is None else table_issues[j].findChildren('td')[4].text.strip()
                issue_fwdto = '' if table_issues[j].findChildren('td')[5] is None else table_issues[j].findChildren('td')[5].text.strip()
                issue_status = '' if table_issues[j].findChildren('td')[6] is None else table_issues[j].findChildren('td')[6].text.strip()
                print('parsed Issuetable')
                break
    issueJCtable = issuedetsoup.find('table', id = 'ctl00_ContentPlaceHolder1_gridJCDetails').findAll('tr')
    issueWorkstable = issuedetsoup.find('table', id = 'ctl00_ContentPlaceHolder1_gridWorkDetails').findAll('tr')
    issueRPtable = issuedetsoup.find('table', id = 'ctl00_ContentPlaceHolder1_gridResponsePerson').findAll('tr')
    
    issue_cat = issuedetsoup.find('span', id = "ctl00_ContentPlaceHolder1_lblIssueCat").text.strip()
    issue_subcat = issuedetsoup.find('span', id = "ctl00_ContentPlaceHolder1_lblIssueSubCat").text.strip()  
    issue_RPdesigdeptnameAll = ''
    issueJCIDed = 1 if len(issueJCtable)>1 else 0
    issueWorksIDed = 1 if len(issueWorkstable)>1 else 0
 
    if len(issueRPtable)>1:               
        for k in range(1,len(issueRPtable)):
            #issue_RPsno = issueRPtable[k].findAll('td')[0].text.strip()
            issue_RPname = '' if issueRPtable[k].findAll('td')[1] is None else issueRPtable[k].findAll('td')[1].text.strip()
            issue_RPdesig = '' if issueRPtable[k].findAll('td')[2] is None else issueRPtable[k].findAll('td')[2].text.strip()
            #issue_RPmobile = issueRPtable[k].findAll('td')[3].text.strip()
            #issue_RPemail = issueRPtable[k].findAll('td')[4].text.strip()
            issue_RPdept = '' if issueRPtable[k].findAll('td')[5] is None else issueRPtable[k].findAll('td')[5].text.strip()
            if k>1:
                issue_RPdesigdeptnameAll = issue_RPdesigdeptnameAll + '; ' + issue_RPdesig + ', ' + issue_RPdept + ', ' + issue_RPname
            else:
                issue_RPdesigdeptnameAll = issue_RPdesigdeptnameAll + issue_RPdesig + ', ' + issue_RPdept + ', ' + issue_RPname
    else:
        issue_RPname = '' if issueRPtable[0].findAll('td')[0] is None else issueRPtable[0].findAll('td')[0].text.strip()
        issue_RPdesig = ''
        issue_RPdept = ''
    if len(issueWorkstable)>1:
        for k in range(1,len(issueWorkstable)):
            issueWork_sno = issueWorkstable[k].findAll('td')[0].text.strip()
            issueWork_id = issueWorkstable[k].findAll('td')[1].text.strip()
            issueWork_name = issueWorkstable[k].findAll('td')[2].text.strip()
            issueWorkwriter.writerow([
                state,
                district,
                block,
                panch,
                panchcode,
                gsdate,
                SA_start_date,
                SA_end_date,
                issue_num,
                issue_cat,
                issue_subcat,
                issueWork_sno,
                issueWork_id,
                issueWork_name
                    ])
            print('Parsed issueWork')
    else:
        issueWork_sno = '' if issueWorkstable[0].findAll('td')[0] is None else issueWorkstable[0].findAll('td')[0].text.strip()
        issueWork_id = ''
        issueWork_name = ''
        issueWorkwriter.writerow([
            state,
            district,
            block,
            panch,
            panchcode,
            gsdate,
            SA_start_date,
            SA_end_date,
            issue_num,
            issue_cat,
            issue_subcat,
            issueWork_sno,
            issueWork_id,
            issueWork_name
                ])
        print('Parsed issueWork')
    if len(issueJCtable)>1:
        for k in range(1,len(issueJCtable)):
            issueJC_sno = issueJCtable[k].findAll('td')[0].text.strip()
            issueJC_id = issueJCtable[k].findAll('td')[1].text.strip()
            issueJC_name = issueJCtable[k].findAll('td')[2].text.strip()
            issueJCwriter.writerow([
                state,
                district,
                block,
                panch,
                panchcode,
                gsdate,
                SA_start_date,
                SA_end_date,
                issue_num,
                issue_cat,
                issue_subcat,
                issueJC_sno,
                issueJC_id,
                issueJC_name
                    ])
    else:
        issueJC_sno = '' if issueJCtable[0].findAll('td')[0] is None else issueJCtable[0].findAll('td')[0].text.strip()
        issueJC_id = ''
        issueJC_name = ''
        print('Parsed issueJC')
        issueJCwriter.writerow([
            state,
            district,
            block,
            panch,
            panchcode,
            gsdate,
            SA_start_date,
            SA_end_date,
            issue_num,
            issue_cat,
            issue_subcat,
            issueJC_sno,
            issueJC_id,
            issueJC_name
                ])
    print('Will write in issuewriter')
    issuewriter.writerow([
            state,
            district,
            block,
            panch,
            panchcode,
            gsdate,
            SA_start_date,
            SA_end_date,
            issue_sno,
            issue_num,
            issue_type,
            issue_desc,
            issue_amt,
            issue_fwdto,
            issue_status, 
            issue_cat,
            issue_subcat,
            issue_RPdesigdeptnameAll,
            issueJCIDed,
            issueWorksIDed])



#set directory
#project = '/home/wendywong/jharkhand/socialaudit_rep/'
project = '/Users/samuelsolomon/Dropbox/NREGA Data visualization/NREGA_Payment_Delay/06_Data/01_Code/Social Audits/Wendy/'
outputPath = project + 'data/raw_data/'
os.chdir(outputPath)

#initiate datafiles
c = open(project+'data/raw_data/socialauditrep_issueWork.csv','a', encoding='utf-8-sig',newline='')
issueWorkwriter = csv.writer(c)
if len(sys.argv)!=2: 
  issueWorkwriter.writerow([
                  'state',
                  'district',
                  'block',
                  'panch',
                  'panchcode',
                  'gsdate',
                  'SA_start_date',
                  'SA_end_date',
                  'issue_num',
                  'issue_cat',
                  'issue_subcat',
                  'issueWork_sno',
                  'issueWork_id',
                  'issueWork_name'
                      ])
    
d = open(project+'data/raw_data/socialauditrep_issueJC.csv','a', encoding='utf-8-sig',newline='')
issueJCwriter = csv.writer(d)
if len(sys.argv)!=2: 
  issueJCwriter.writerow([
                  'state',
                  'district',
                  'block',
                  'panch',
                  'panchcode',
                  'gsdate',
                  'SA_start_date',
                  'SA_end_date',
                  'issue_num',
                  'issue_cat',
                  'issue_subcat',
                  'issueJC_sno',
                  'issueJC_id',
                  'issueJC_name'
                      ])
    
e = open(project+'data/raw_data/socialauditrep_issues.csv','a', encoding='utf-8-sig',newline='')
issuewriter = csv.writer(e)
if len(sys.argv)!=2: 
  issuewriter.writerow([
                  'state',
                  'district',
                  'block',
                  'panch',
                  'panchcode',
                  'gsdate',
                  'SA_start_date',
                  'SA_end_date',
                  'issue_sno',
                  'issue_num',
                  'issue_type',
                  'issue_desc',
                  'issue_amt',
                  'issue_fwdto',
                  'issue_status', 
                  'issue_cat',
                  'issue_subcat',
                  'issue_RPdesigdeptnameAll',
                  'issueJCIDed',
                  'issueWorksIDed'])

h = open(project+'data/input/socialauditrepissue_parseerror1.csv','a',encoding='utf-8-sig', newline='')
writeparseerror = csv.writer(h)
if len(sys.argv)!=2: 
  writeparseerror.writerow([
                          "panch_code", 
                          "filename",
                           "error_type"
                          ])

#initiate live error-tracking   
parse_error_list = []
error_count = 0

#merge by panchayat_code with *codes.csv to have complete dist,block,panch info
rawPath = outputPath + 'raw_html/issues'
os.chdir(rawPath)
filenames = os.listdir(os.getcwd())
filenames.sort()
for filename in filenames:
    if filename.endswith(".html"):
        panchcode = filename[0:10]
        gsdate = filename[11:21]
        issue_num_filename = filename[22:len(filename)].replace('.html','')
        rawhtml = open(filename,encoding='utf-8-sig', newline='\n')
        issuedetsoup = BeautifulSoup(rawhtml.read(),"lxml")
        rawhtml.close()
        try:
            parsed = parse_issue_html(issuedetsoup,panchcode,gsdate,issue_num_filename,issuewriter,issueWorkwriter,issueJCwriter)
            print("Parsed file: "+str(filename))
        except Exception as err:
            parse_error_list.append("Parse error for panch {} and  jcn {}: {}".format(panchcode,filename,err))
            error_count += 1
            writeparseerror.writerow([
                                      panchcode,
                                      filename,
                                      str(err)
                                      ])  
    else:
        continue

    
    c.flush()
    os.fsync(c.fileno())               
    d.flush()
    os.fsync(d.fileno())
    e.flush()
    os.fsync(e.fileno())
    h.flush()
    os.fsync(h.fileno())
 
c.close()
d.close()
e.close()
h.close()    
print(parse_error_list)
print(error_count)
