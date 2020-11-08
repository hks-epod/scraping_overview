import requests
import json
import pandas as pd
import timeit
import argparse
import os
import csv
t_start = timeit.default_timer()

parser = argparse.ArgumentParser()
parser.add_argument('start', type=int)
args = parser.parse_args()
START = args.start
end = START + 25

# TO USE THIS make sure to modify the directories (!!)

data = r"/home/accts/ark79/EGC/selenium_demo/aakashpt2/oop/"
# pc_codes = pd.read_stata(data + "musters_2020.dta")
pc_codes = pd.read_csv("/home/accts/ark79/EGC/selenium_demo/aakashpt2/oop/oop.csv")
if(end < len(pc_codes)): 
    pc_codes = pc_codes[START:end]
else: 
    pc_codes = pc_codes[START:]

pc = pc_codes['panchayat_code']
mc = pc_codes['msr_no']
ali = zip(pc, mc)

musters = pd.DataFrame(columns = ['worker_code','msr_no', 'payment_date', 'total_dues', 'tot_persondays',
       'work_approval_date', 'work_code', 'muster_roll_period_from',
       'work_name', 'muster_roll_period_to'])
final = pd.DataFrame(columns = ['panchayat_code','address', 'age_at_reg', 'bpl_status', 'current_account_no',
       'current_bank_po', 'gender', 'hoh_name', 'job_card_number', 'person_id',
       'reg_date', 'Village_name', 'worker_code', 'worker_name', 'msr_no',
       'payment_date', 'total_dues', 'tot_persondays', 'work_approval_date',
       'work_code', 'muster_roll_period_from', 'work_name',
       'muster_roll_period_to'] )
headers = { 'Content-Type': 'application/x-www-form-urlencoded' }

for i, p in enumerate(ali):
    pc = p[0]
    mc = p[1]
    print(p)
    print("{} out of {} pcs".format(i, len(pc_codes)))
    #Get Workers 
    url = 'https://nregarep2.nic.in/netnrega/nregapost/API_API3.asmx/API_API3_Workers'
    myobj = {'panchayat_code': pc,'mustrolid':str(int(mc)), 'Workid':''}
    x = requests.post(url, data = myobj,headers = headers)
    data = json.loads(x.json()['reponse_data'])
    workers = pd.DataFrame.from_records(data)
    #Get Muster Rolls
    for w_i, w in enumerate(workers['worker_code']):
        try: 
            print("{} out of {} workers".format(w_i, len(workers['worker_code'])))
            url = 'https://nregarep2.nic.in/netnrega//nregapost/API_API2.asmx/API_API2'
            myobj = {'panchayat_code': p,'Workid':'', 'workerId':w}
            x = requests.post(url, data = myobj,headers = headers)
            data = json.loads(x.json()['reponse_data'])
            muster = pd.DataFrame.from_records(data)
            muster['worker_code'] = w
            musters = musters.append(muster)
            
        except: 
            f = open('/home/accts/ark79/EGC/selenium_demo/aakashpt2/oop/oop_issues/issues.csv', 'a+', newline='')
            issuewriter = csv.writer(f)
            issuewriter.writerow([p, w])
  

    #Merge muster and worker data, and add to final data 
    worker_musters = workers.merge(musters,how="left",on="worker_code")
    worker_musters['panchayat_code'] = pc
    final = final.append(worker_musters)

f = '/home/accts/ark79/EGC/selenium_demo/aakashpt2/oop/oop_data/' + str(START) + '_muster.csv'

final.to_csv(f)

t_stop = timeit.default_timer()
print('this took time: ', t_stop - t_start)  

    