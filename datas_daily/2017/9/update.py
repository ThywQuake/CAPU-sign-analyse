import os
import pickle
import re
from datetime import datetime, timedelta
import hashlib
import requests
from bs4 import BeautifulSoup

root=r'./datas_daily'
person_root=r'./datas_person'


def get_path_from_date(date: datetime):
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(root + os.sep + year):
        os.mkdir(root + os.sep + year)
    if not os.path.exists(root + os.sep + year + os.sep + month):
        os.mkdir(root + os.sep + year + os.sep + month)
    return root + os.sep + year + os.sep + month + os.sep + day


def get_data_from_date(date: datetime):
    url_root = 'https://www.chexie.net/bbs/sign/?view='
    url = url_root + date.strftime('%Y-%m-%d')
    response = requests.get(url)
    signs = {}
    print(f'Retrieving data from {url}')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        soup_split = re.split('本年度签到统计：', str(soup))
        matches = re.findall('#(\d+): (.*)', str(soup_split[0]))
        for match in matches:
            signs[match[1]] = match[0]
        return signs
    else:
        print('Failed to retrieve webpage.')
        return -1

def get_data(start_date, end_date):
    current_date = start_date
    while current_date != end_date:
        signs=get_data_from_date(current_date)
        path = get_path_from_date(current_date)
        with open(path, 'wb') as f:
            pickle.dump(signs, f)
        current_date += timedelta(days=1)


def get_latest_date():
    year_dir = max(os.listdir(root))
    month_dirs = os.listdir(root + os.sep + year_dir)
    month_dirs = [int(m) for m in month_dirs]
    month = max(month_dirs)
    day = max(os.listdir(root + os.sep + year_dir + os.sep + str(month)))
    return datetime(int(year_dir), month, int(day))

def update():
    today = datetime.today()
    today = datetime(today.year, today.month, today.day)
    latest_date = get_latest_date()
    get_data(latest_date + timedelta(days=1), today)
    print(f'Updated from {latest_date} to {today} !')

def get_data_for_person(date:datetime):
    signs=get_data_from_date(date)
    path_r=person_root+os.sep+'register'
    with open(path_r,'rb') as register_f:
        register=pickle.load(register_f)
        register[date]=[]
    for id in signs.keys():
        id_md5=hashlib.md5(id.encode('utf-8')).hexdigest()
        path=person_root+os.sep+id_md5
        if not os.path.exists(path):
            signer={'ID':id}
            signer[date]=signs[id]
            with open(path,'wb') as f:
                pickle.dump(signer,f)
            path_r=person_root+os.sep+'register'
            register[date].append(id) 
        else:
            with open(path,'rb') as f:
                signer=pickle.load(f)
            signer[date]=signs[id]
            with open(path,'wb') as f:
                pickle.dump(signer,f)
    with open(path_r,'wb') as f:
        pickle.dump(register,f)
    
def get_data_for_person_over_days(start_date,end_date):
    current_date=start_date
    while current_date!=end_date:
        get_data_for_person(current_date)
        current_date+=timedelta(days=1)

def update_for_person():
    today = datetime.today()
    today = datetime(today.year, today.month, today.day)
    latest_date = get_latest_date()
    get_data_for_person_over_days(latest_date + timedelta(days=1), today)
    print(f'Updated from {latest_date} to {today} !')