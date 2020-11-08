from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.types import Integer, String, Float
from sqlalchemy import create_engine
import argparse
import pandas as pd
import pymysql
import requests
import json
import os
import csv
import re
from openpyxl import load_workbook

issues = []
error = 0


def api_calls(panchayat_list):

    url = 'https://nregarep2.nic.in/netnrega/nregapost/API_API2.asmx/API_API2'
    output = []

    for i, item in enumerate(panchayat_list):
        try:

            post_data = {
                'panchayat_code': (str(item['Panchayat_Code'])).zfill(10),
                'Workid': '',
                'workerId': ''
            }

            r = requests.post(url, data=post_data)
            r_dict = r.json()
            r_data = json.loads(r_dict['reponse_data'])

            print(r_data[0], len(r_data))
            exit()
            # Comes out as a list of dicts instead of a dict without a [0] at the end
            # That's because the json is an array with a single object inside

            # Appending to a json file directly produces an invalid json file with "]["
            # So we individually add each dict to the output list
            r_data = [{'panchayat_code': item['Panchayat_Code'],
                       'payment_date': muster['payment_date'],
                       'total_dues': muster['total_dues'],
                       'tot_persondays': muster['tot_persondays'],
                       'msr_no': muster['msr_no'],
                       'muster_roll_period_from': muster['muster_roll_period_from'],
                       'muster_roll_period_to': muster['muster_roll_period_to']} for muster in r_data]

            output.append(r_data)

        except Exception as e:
            print("EXCEPT 1")
            issues.append(item)

    try:
        output = pd.concat([pd.DataFrame(df) for df in output])
        return output
    except:
        print("EXCEPT 2")
        error = error + 1


if __name__ == '__main__':
    chunksize = 1
    f = 'tester.csv'
    project = '/Users/aliciakacharia/Pande Research Dropbox/Alicia Kacharia/C19 and Inclusion/2_Data/FBA_Data/'
    g = open(project + f, 'a+', encoding='utf-8-sig', newline='')
    writer = csv.writer(g)
    writer.writerow(['panchayat_code', 'payment_date', 'total_dues', 'tot_persondays',
                     'msr_no', 'muster_roll_period_from', 'muster_roll_period_to'])

    df_panchayats = pd.read_csv(project + 'FBA GPs.csv')
    panchayat_list = df_panchayats.to_dict('records')
    panchayat_chunks = [panchayat_list[i: i + chunksize]
                        for i in range(0,  len(panchayat_list),  chunksize)]

    empty = []
    for chunk, panchayat_chunk in enumerate(panchayat_chunks):
        print('This is chunk {}/{}'.format(chunk, len(panchayat_chunks) - 1))
        output = api_calls(panchayat_chunk)
        try:
            output.to_csv(f, mode='a', header=False)
        except:
            print("EXCEPT 3")
            empty.append(panchayat_chunk)

    print(issues, empty, error)
    g.close()
