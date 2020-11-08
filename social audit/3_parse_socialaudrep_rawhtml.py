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
parse raw html of social audit report

written by: Wendy Wong 
last updated: February 24, 2020
'''
def parse_socialaudrep_html(response,panchcode,gsdate,writer,auditorwriter):
    soupspan = response.findAll("span")
    print('soupspan length is '+ str(len(soupspan)))
#    souptd = response.findAll("td")
#    souptable = response.findAll("table")
    
    table_auditors = '' if response.findAll('div',id = "ctl00_ContentPlaceHolder1_divBasicInfo")[0].find('table') is None else response.findAll('div',id = "ctl00_ContentPlaceHolder1_divBasicInfo")[0].find('table').findChildren("tr")
    table_atrsummary = '' if response.findAll('div',id = "ctl00_ContentPlaceHolder1_divATR")[0].find('table') is None else response.findAll('div',id = "ctl00_ContentPlaceHolder1_divATR")[0].find('table').findChildren("tr")[1]
    table_issuesummary = '' if response.findAll('div',id = "ctl00_ContentPlaceHolder1_divReportedIssue")[0].find('table') is None else response.findAll('div',id = "ctl00_ContentPlaceHolder1_divReportedIssue")[0].find('table').findChildren('td')
    table_issues = '' if response.findAll('div',id = "ctl00_ContentPlaceHolder1_divIndIssue")[0].find('table') is None else response.findAll('div',id = "ctl00_ContentPlaceHolder1_divIndIssue")[0].find('table').findChildren("tr")

    FMissues_reported = '' if table_issuesummary=='' else table_issuesummary[1].text
    FMissues_closed = '' if table_issuesummary=='' else table_issuesummary[2].text
    FDissues_reported = '' if table_issuesummary=='' else table_issuesummary[3].text
    FDissues_closed = '' if table_issuesummary=='' else table_issuesummary[4].text
    PVissues_reported = '' if table_issuesummary=='' else table_issuesummary[5].text
    PVissues_closed = '' if table_issuesummary=='' else table_issuesummary[6].text
    Grievances_reported = '' if table_issuesummary=='' else table_issuesummary[7].text
    Grievances_closed = '' if table_issuesummary=='' else table_issuesummary[8].text
    Totissues_count = len(table_issues)-1
    Totissues_reported = '' if table_issuesummary=='' else table_issuesummary[9].text
    Totissues_closed = '' if table_issuesummary=='' else table_issuesummary[10].text

    state = response.find('span',id = "ctl00_ContentPlaceHolder1_lblstate").text.strip()
    district = response.find('span',id = "ctl00_ContentPlaceHolder1_lbldistrict").text.strip()
    block = response.find('span',id = "ctl00_ContentPlaceHolder1_lblblock").text.strip()
    panch = response.find('span',id = "ctl00_ContentPlaceHolder1_lblpanchayat").text.strip()
    panchcode = panchcode
    gsdate = gsdate
    SA_start_date = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblSA_start_dt") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblSA_start_dt").text.strip()
    SA_end_date = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblSA_end_dt") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblSA_end_dt").text.strip()
    gramsabha_date = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblGramSabha_dt") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblGramSabha_dt").text.strip()
    publichearing_date = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblPublic_Hearing_dt") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblPublic_Hearing_dt").text.strip()
    auditperiod_from_date = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblSA_Period_From_Date") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblSA_Period_From_Date").text.strip()
    auditperiod_to_date = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblSA_Period_To_Date") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblSA_Period_To_Date").text.strip()
    unskwageexp_rs = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblWage_exp") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblWage_exp").text.strip()
    materialexp_rs = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblmat_exp") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblmat_exp").text.strip()
    totalexp_rs = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lbltotal_expen") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lbltotal_expen").text.strip()
    unskwageexp_fromImpAgency_rs = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblwage_given") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblwage_given").text.strip()
    materialexp_fromImpAgency_rs = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblmat_given") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblmat_given").text.strip()
    totalexp_fromImpAgency_rs = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lbltotal_record_given") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lbltotal_record_given").text.strip()
    worksct = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lbltot_work") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lbltot_work").text.strip()
    hhworkedct = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lbltot_hh") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lbltot_hh").text.strip()
    worksct_verif = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lbltot_work_verified") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lbltot_work_verified").text.strip()
    hhworkedct_verif = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lbltot_hh_verified") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lbltot_hh_verified").text.strip()
    gramsabha_numparticip = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblno_of_ppl_participated_gs") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblno_of_ppl_participated_gs").text.strip()
    indepobs_name = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblobserver_name") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblobserver_name").text.strip()
    indepobs_desig = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblobserver_designation") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblobserver_designation").text.strip()
    saexp_printing = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblprinting_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblprinting_expense").text.strip()
    saexp_videography = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblvideography_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblvideography_expense").text.strip()
    saexp_tea = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lbltea_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lbltea_expense").text.strip()
    saexp_vrptraining = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblvrp_training_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblvrp_training_expense").text.strip()
    saexp_vrptravel = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblvrp_travel_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblvrp_travel_expense").text.strip()
    saexp_photocopy = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblphotocopying_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblphotocopying_expense").text.strip()
    saexp_other = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblother_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblother_expense").text.strip()
    saexp_vrphonararium = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblvrp_honorium_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblvrp_honorium_expense").text.strip()
    saexp_stationary = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblstationary_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblstationary_expense").text.strip()
    saexp_publicity = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblpublicity_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblpublicity_expense").text.strip()
    saexp_micsystem = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblmic_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblmic_expense").text.strip()
    saexp_photography = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblphotography_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblphotography_expense").text.strip()
    saexp_shamianatent = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblshamiana_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblshamiana_expense").text.strip()
    saexp_total = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lbltotal_expense") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lbltotal_expense").text.strip()
    sa_qualrep = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_lblqualitative_report") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_lblqualitative_report").text.strip()
    arejobcards_withppl = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label1") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label1").text.strip()
    arejobcards_updated = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label3") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label3").text.strip()
    arejobcards_renewed = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label4") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label4").text.strip()
    workwages_processtoregrct = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label2") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label2").text.strip()
    workwages_demandnotmet = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label29") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label29").text.strip()
    workwages_probgettingwages = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label30") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label30").text.strip()
    admin_musterworksite = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label5") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label5").text.strip()
    admin_wageslipsgiven = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label6") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label6").text.strip()
    admin_rozgardiwasheld = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label7") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label7").text.strip()
    admin_sevenregistersgp = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label17") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label17").text.strip()
    acctblty_infoboardcommworks = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label8") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label8").text.strip()
    acctblty_infoboardhhworks = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label9") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label9").text.strip()
    acctblty_wallwritings = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label10") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label10").text.strip()
    acctblty_grievance = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label15") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label15").text.strip()
    acctblty_records = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label16") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label16").text.strip()
    gs_approveworks = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label14") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label14").text.strip()
    gs_workspriority = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label18") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label18").text.strip()
    worksite_drinkingwater = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label19") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label19").text.strip()
    worksite_shade = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label20") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label20").text.strip()
    worksite_firstaid = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label21") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label21").text.strip()
    worksite_womanfivechildren = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label26") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label26").text.strip()
    personnel_mateselect = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label22") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label22").text.strip()
    personnel_matetrained = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label23") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label23").text.strip()
    personnel_nregsadeqstaff = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label24") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label24").text.strip()
    personnel_nregsdedicstaff = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label25") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label25").text.strip()
    personnel_nregsstafftrained = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label27") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label27").text.strip()
    personnel_adeqtechstaff = '' if response.find('span',id = "ctl00_ContentPlaceHolder1_Label28") is None else response.find('span',id = "ctl00_ContentPlaceHolder1_Label28").text.strip()
    atr_fmAmt = '' if table_atrsummary.findChildren('td')[1] is None else table_atrsummary.findChildren('td')[1].text #assume ATR summary table aways has one row...
    atr_fmAmtRecov = '' if table_atrsummary.findChildren('td')[2] is None else table_atrsummary.findChildren('td')[2].text
    atr_fdAmt = '' if table_atrsummary.findChildren('td')[3] is None else table_atrsummary.findChildren('td')[3].text
    atr_finepaid = '' if table_atrsummary.findChildren('td')[4] is None else table_atrsummary.findChildren('td')[4].text
    atr_numFIRs = '' if table_atrsummary.findChildren('td')[5] is None else table_atrsummary.findChildren('td')[5].text
    atr_numEmpSusp = '' if table_atrsummary.findChildren('td')[6] is None else table_atrsummary.findChildren('td')[6].text
    atr_numEmpTerm = '' if table_atrsummary.findChildren('td')[7] is None else table_atrsummary.findChildren('td')[7].text
    
    writer.writerow([   state, 
                        district,
                        block,
                        panch,
                        panchcode,
                        gsdate,
                        SA_start_date,
                        SA_end_date,
                        gramsabha_date,
                        publichearing_date,
                        auditperiod_from_date,
                        auditperiod_to_date,
                        unskwageexp_rs,
                        materialexp_rs,
                        totalexp_rs,
                        unskwageexp_fromImpAgency_rs,
                        materialexp_fromImpAgency_rs,
                        totalexp_fromImpAgency_rs,
                        worksct,
                        hhworkedct,
                        worksct_verif,
                        hhworkedct_verif,
                        gramsabha_numparticip,
                        indepobs_name,
                        indepobs_desig,
                        saexp_printing,
                        saexp_videography,
                        saexp_tea,
                        saexp_vrptraining,
                        saexp_vrptravel,
                        saexp_photocopy,
                        saexp_other,
                        saexp_vrphonararium,
                        saexp_stationary,
                        saexp_publicity,
                        saexp_micsystem,
                        saexp_photography,
                        saexp_shamianatent,
                        saexp_total,
                        sa_qualrep,
                        arejobcards_withppl,
                        arejobcards_updated,
                        arejobcards_renewed,
                        workwages_processtoregrct,
                        workwages_demandnotmet,
                        workwages_probgettingwages,
                        admin_musterworksite,
                        admin_wageslipsgiven,
                        admin_rozgardiwasheld,
                        admin_sevenregistersgp,
                        acctblty_infoboardcommworks,
                        acctblty_infoboardhhworks,
                        acctblty_wallwritings,
                        acctblty_grievance,
                        acctblty_records,
                        gs_approveworks,
                        gs_workspriority,
                        worksite_drinkingwater,
                        worksite_shade,
                        worksite_firstaid,
                        worksite_womanfivechildren,
                        personnel_mateselect,
                        personnel_matetrained,
                        personnel_nregsadeqstaff,
                        personnel_nregsdedicstaff,
                        personnel_nregsstafftrained,
                        personnel_adeqtechstaff,
                        FMissues_reported,
                        FMissues_closed,
                        FDissues_reported,
                        FDissues_closed,
                        PVissues_reported,
                        PVissues_closed,
                        Grievances_reported,
                        Grievances_closed,
                        Totissues_count,
                        Totissues_reported,
                        Totissues_closed,
                        atr_fmAmt,
                        atr_fmAmtRecov,
                        atr_fdAmt,
                        atr_finepaid,
                        atr_numFIRs,
                        atr_numEmpSusp,
                        atr_numEmpTerm
            ])

    if len(table_auditors)>1:
        for j in range(1,len(table_auditors)):
            auditor_sno = '' if table_auditors[j].findChildren('td')[0] is None else table_auditors[j].findChildren('td')[0].text
            auditor_name = '' if table_auditors[j].findChildren('td')[1] is None else table_auditors[j].findChildren('td')[1].text
            auditor_title = '' if table_auditors[j].findChildren('td')[2] is None else table_auditors[j].findChildren('td')[2].text
            auditorwriter.writerow([
                    state,
                    district,
                    block,
                    panch,
                    panchcode,
                    gsdate,
                    SA_start_date,
                    SA_end_date,
                    auditor_sno,
                    auditor_name,
                    auditor_title
                    ])






#set directory
#project = '/home/wendywong/jharkhand/socialaudit_rep/'
project = '/Users/samuelsolomon/Dropbox/NREGA Data visualization/NREGA_Payment_Delay/06_Data/01_Code/Social Audits/Wendy/'
outputPath = project + 'data/raw_data/'
os.chdir(outputPath)


#initiate datafiles
b = open(project+'data/raw_data/socialauditrep_auditor.csv','a', encoding='utf-8-sig',newline='')
auditorwriter = csv.writer(b)
if len(sys.argv)!=2: 
  auditorwriter.writerow([
                  'state',
                  'district',
                  'block',
                  'panch',
                  'panchcode',
                  'gsdate',
                  'SA_start_date',
                  'SA_end_date',
                  'auditor_sno',
                  'auditor_name',
                  'auditor_title'
                  ])
    
    
f = open(project+'data/raw_data/socialauditreports.csv','a', encoding='utf-8-sig',newline='')
writer = csv.writer(f)
if len(sys.argv)!=2: 
  writer.writerow([   'state', 
                      'district',
                      'block',
                      'panch',
                      'panchcode',
                      'gsdate',
                      'SA_start_date',
                      'SA_end_date',
                      'gramsabha_date',
                      'publichearing_date',
                      'auditperiod_from_date',
                      'auditperiod_to_date',
                      'unskwageexp_rs',
                      'materialexp_rs',
                      'totalexp_rs',
                      'unskwageexp_fromImpAgency_rs',
                      'materialexp_fromImpAgency_rs',
                      'totalexp_fromImpAgency_rs',
                      'worksct',
                      'hhworkedct',
                      'worksct_verif',
                      'hhworkedct_verif',
                      'gramsabha_numparticip',
                      'indepobs_name',
                      'indepobs_desig',
                      'saexp_printing',
                      'saexp_videography',
                      'saexp_tea',
                      'saexp_vrptraining',
                      'saexp_vrptravel',
                      'saexp_photocopy',
                      'saexp_other',
                      'saexp_vrphonararium',
                      'saexp_stationary',
                      'saexp_publicity',
                      'saexp_micsystem',
                      'saexp_photography',
                      'saexp_shamianatent',
                      'saexp_total',
                      'sa_qualrep',
                      'arejobcards_withppl',
                      'arejobcards_updated',
                      'arejobcards_renewed',
                      'workwages_processtoregrct',
                      'workwages_demandnotmet',
                      'workwages_probgettingwages',
                      'admin_musterworksite',
                      'admin_wageslipsgiven',
                      'admin_rozgardiwasheld',
                      'admin_sevenregistersgp',
                      'acctblty_infoboardcommworks',
                      'acctblty_infoboardhhworks',
                      'acctblty_wallwritings',
                      'acctblty_grievance',
                      'acctblty_records',
                      'gs_approveworks',
                      'gs_workspriority',
                      'worksite_drinkingwater',
                      'worksite_shade',
                      'worksite_firstaid',
                      'worksite_womanfivechildren',
                      'personnel_mateselect',
                      'personnel_matetrained',
                      'personnel_nregsadeqstaff',
                      'personnel_nregsdedicstaff',
                      'personnel_nregsstafftrained',
                      'personnel_adeqtechstaff',
                      'FMissues_reported',
                      'FMissues_closed',
                      'FDissues_reported',
                      'FDissues_closed',
                      'PVissues_reported',
                      'PVissues_closed',
                      'Grievances_reported',
                      'Grievances_closed',
                      'Totissues_count',
                      'Totissues_reported',
                      'Totissues_closed',
                      'atr_fmAmt',
                      'atr_fmAmtRecov',
                      'atr_fdAmt',
                      'atr_finepaid',
                      'atr_numFIRs',
                      'atr_numEmpSusp',
                      'atr_numEmpTerm'
          ])

h = open(project+'data/input/socialauditrep_parseerror1.csv','a',encoding='utf-8-sig', newline='')
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

rawPath = outputPath + 'raw_html/'
os.chdir(rawPath)
filenames = os.listdir(os.getcwd())
filenames.sort()

for filename in filenames:
    if filename.endswith(".html"):
        panchcode = filename[0:10]
        gsdate = filename[11:21]
        rawhtml = open(filename,encoding='utf-8-sig', newline='\n')
        audrepsoup = BeautifulSoup(rawhtml.read(),"lxml")
        rawhtml.close()
        try:
            track_atrsummary = parse_socialaudrep_html(audrepsoup,panchcode,gsdate,writer,auditorwriter)
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

    
    b.flush()
    os.fsync(b.fileno())
    f.flush()
    os.fsync(f.fileno())
    h.flush()
    os.fsync(h.fileno())
 
b.close()
f.close()
h.close()    
print(parse_error_list)
print(error_count)
print(track_atrsummary)
