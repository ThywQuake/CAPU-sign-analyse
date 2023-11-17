import os
import pickle
import seaborn as sns
import calplot
import pandas as pd
import hashlib
from datetime import datetime, timedelta

import matplotlib
import matplotlib.pyplot as plt

import update as upd

matplotlib.rc("font", family='DengXian')
root = r'C:\Users\AnotherMe\Documents\PythonScripts\datas_daily'
_format= '%Y-%m-%d'
save_path=r"C:\Users\Public\Pictures"
csv_path=r"C:\Users\AnotherMe\Documents\PythonScripts\csv\datas.csv"
person_root=r'C:\Users\AnotherMe\Documents\PythonScripts\datas_person'


def is_valid_date(datestr: str):
    try:
        year, month, day = map(int, datestr.split('-'))
        date = datetime(year, month, day)
        if (date.year == year) and (date.month == month) and (date.day == day):
            return True
        else:
            return False
    except ValueError:
        return False


def get_buffer_from_date(date: datetime):
    path = root + os.sep + str(date.year) + os.sep + str(date.month) + os.sep + str(date.day)
    if not os.path.exists(path):
        if input(f'Data in {date} is missing. Do you want to update dataset?[y/n]\n') == 'y':
            upd.update()
            return get_buffer_from_date(date)
        else:
            return -1
    with open(path, 'rb') as f:
        # print(f'Getting data from {path} ...')
        buffer = pickle.load(f)
    return buffer


def enter_date(describe: str):
    date = input(f'Please enter the ' + describe + ' date(yyyy-mm-dd): ')
    while not is_valid_date(date):
        date = input('Invalid input! Please try again(yyyy-mm-dd): ')
    year, month, day = map(int, date.split('-'))
    date = datetime(year, month, day)
    return date

def transfer_date(date:str):
    year, month, day = map(int, date.split('-'))
    date = datetime(year, month, day)
    return date

class Analyse():
    def __init__(self, start_date=None, end_date=None):
        if start_date is None:
            self.start_date = enter_date('start')
        else:self.start_date=transfer_date(start_date)
        if end_date is None:
            self.end_date = enter_date('end')
        else:self.end_date=transfer_date(end_date)
        self.signs = self.get_signs()

    def get_signs(self):
        signs = []
        current_date = self.start_date
        while current_date != self.end_date:
            sign = get_buffer_from_date(current_date)
            if sign == -1:
                return -1
            signs.append(len(sign))
            current_date += timedelta(days=1)
        return signs

    def get_signer(self, ID):
        signer = {}
        current_date = self.start_date
        while current_date != self.end_date:
            sign = get_buffer_from_date(current_date)
            if sign == -1:
                return -1
            if ID in sign.keys():
                signer[current_date] = int(sign[ID])
            else:
                signer[current_date] = 0
            current_date += timedelta(days=1)
        return signer

    def show_signs(self, show_type='plot', color='b', showMax=False, showMin=False):
        signs = self.signs
        if signs != -1:
            print('Analysing...')
            if show_type == 'plot':
                plt.plot(range(len(signs)), signs, color)
            else:
                plt.bar(range(len(signs)), signs, color)
            plt.title(f'CAPU signs {show_type}\n From {self.start_date.date()} To {self.end_date.date()}\n')
            # f'Sign Max Day: ' +
            # (self.start_date + timedelta(days=signs.index(max(signs)))).date().strftime('%Y-%m-%d') +
            # f' :{max(signs)} signs\n'
            # f'Sign Min Day: ' +
            # (self.start_date + timedelta(days=signs.index(min(signs)))).date().strftime('%Y-%m-%d') +
            # f' :{min(signs)} signs\n')
            if showMax:
                plt.axvline(signs.index(max(signs)), 0, 500)
            if showMin:
                plt.axvline(signs.index(min(signs)), 0, 500)

            plt.xlabel('Date')
            plt.ylabel('Signs')
            plt.show()

    def show_signs_heatmap(self,view='year',save=False):
        signs = self.signs
        if view=='year':
            years=range(self.start_date.year,self.end_date.year+1)
            months_name=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            data=[[0 for i in range(12)] for j in range(len(years))]
            date_A=self.start_date
            date_B=date_A
            while date_A!=self.end_date:
                sum_of_signs=0
                while date_A.month==date_B.month and date_A!=self.end_date:
                    sum_of_signs+=signs[(date_A-self.start_date).days]
                    date_A+=timedelta(days=1)
                date_B=date_A
                data[date_A.year-self.start_date.year][date_A.month-1]=sum_of_signs
            plt.figure(figsize=(12,6))
            plt.title(f'CAPU signs heatmap\n From {self.start_date.date()} To {self.end_date.date()}\n')
            sns.heatmap(data,xticklabels=months_name,yticklabels=years,square=True,cmap='Reds')
            if save:
                plt.savefig(save_path+os.sep+'CAPU signs heatmap.png')
            
                
        elif view=='month':
            months_name=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            days=range(1,32)
            data=[[0 for i in range(31)] for j in range(len(months_name))]
            date_A=self.start_date
            while date_A!=self.end_date:
                signs_of_day=signs[(date_A-self.start_date).days]
                date_A+=timedelta(days=1)
                data[date_A.month-1][date_A.day-1]=signs_of_day
            plt.figure(figsize=(12,6))
            plt.title(f'CAPU signs heatmap\n From {self.start_date.date()} To {self.end_date.date()}\n')
            sns.heatmap(data,xticklabels=days,yticklabels=months_name,square=True,cmap='Reds')
            if save:
                plt.savefig(save_path+os.sep+'CAPU signs heatmap.png')

        elif view=='calendar':
            df=pd.DataFrame(
            {'signs':signs},index=pd.date_range(start=self.start_date.strftime(_format),
                                                     end=(self.end_date-timedelta(days=1)).strftime(_format),freq='D')
            )
            df.index.name='date'
            calplot.calplot(data=df['signs'],cmap='Reds',suptitle=f'CAPU signs From {self.start_date.date()} To {self.end_date.date()}\n')
            plt.show()
            if save:
                plt.savefig(save_path+os.sep+'CAPU signs heatmap.png')            
            

    def show_signer(self, ID):
        signer = self.get_signer(ID)
        real_signs = {}
        for k, v in signer.items():
            if v != 0:
                real_signs[k] = v
        if signer != -1:
            print('Analysing...')
        print(f'{ID} has signed for {len(real_signs)} days!\n'
              f'In this period, {ID} start signing in {list(real_signs.keys())[0].strftime(_format)}\n'
              f'end signing in {list(real_signs.keys())[-1].strftime(_format)}\n')
        if input('Details?[y/n]\n') == 'y':
            for date, rank in real_signs.items():
                print(f'Date: ' + date.strftime(_format) + f'\nRank: {rank}')
        print('Plotting...')
        plt.bar(range(len(signer)), [int(sv) for sv in signer.values()])
        plt.title(f'Sign ranks of {ID}\n From {self.start_date.date()} To {self.end_date.date()}\n'
                  f'Total signs: {len(real_signs)} day(s)\n'
                  f'In this period, {ID} start signing in {list(real_signs.keys())[0].strftime(_format)}\n'
                  f'end signing in {list(real_signs.keys())[-1].strftime(_format)}\n')
        plt.xlabel('Date')
        plt.ylabel('Sign Ranks')
        plt.show()

    def show_signer_heatmap(self,ID,save=False):
        signer = self.get_signer(ID)
        real_signs = {}
        for k, v in signer.items():
            if v != 0:
                real_signs[k] = v
        df=pd.DataFrame(
            {'signs':real_signs.values()},index=pd.to_datetime(list(real_signs.keys()),format=_format)
        )
        df.index.name='date'
        calplot.calplot(data=df['signs'],cmap='Reds',suptitle=f'signs heatmap of {ID} From {self.start_date.date()} To {self.end_date.date()}\n')
        if save:
            plt.savefig(save_path+os.sep+f'signs heatmap of {ID}.png')

    def show_register(self):
        with open(root + os.sep + 'register', 'rb') as f:
            register = pickle.load(f)
        current_date = self.start_date
        register_period = {}
        while current_date != self.end_date:
            register_period[current_date] = len(register[current_date])
            current_date += timedelta(days=1)
        print('Analysing...')
        plt.bar(range(len(register_period)), register_period.values())
        plt.title(f'Registered people\n From {self.start_date.date()} To {self.end_date.date()}\n')
        plt.xlabel('Date')
        plt.ylabel('People')
        plt.show()

    def show_register_heatmap(self,save=False):
        with open(root + os.sep + 'register', 'rb') as f:
            register = pickle.load(f)
        current_date = self.start_date
        register_period = {}
        while current_date != self.end_date:
            register_period[current_date] = len(register[current_date])
            current_date += timedelta(days=1)
        df=pd.DataFrame(
            {'people':register_period.values()},index=pd.date_range(start=self.start_date.strftime(_format),
             end=(self.end_date-timedelta(days=1)).strftime(_format),freq='D')
        )
        df.index.name='date'
        calplot.calplot(data=df['people'],cmap='Reds',suptitle=f'Registered people From {self.start_date.date()} To {self.end_date.date()}\n')
        if save:
            plt.savefig(save_path+os.sep+f'Registered people.png')

class RegisterAnalyse():
    def __init__(self):
        self.ids=self.get_ids()
        self.register=self.get_register()
        self.start_date=datetime(2014,1,1)
        self.end_date=datetime.today()

    def get_ids(self):
        ids=os.listdir(person_root)
        ids.remove('register')
        ids.remove('register_keyerror')
        return ids
    
    def get_register(self):
        with open(person_root+os.sep+'register','rb') as f:
            register=pickle.load(f)
        return register

    def get_register_date_and_latest_date(self, ID):
        id_md5 = hashlib.md5(ID.encode('utf-8')).hexdigest()
        path = person_root + os.sep + id_md5
        if not os.path.exists(path):
            return -1
        with open(path, 'rb') as f:
            signer = pickle.load(f)
        signer.pop('ID')
        return min(signer.keys()), max(signer.keys())
    
    def get_life_span(self,ID):
        register_date,latest_date=self.get_register_date_and_latest_date(ID)
        if register_date==-1:
            return -1
        else:
            return (latest_date-register_date).days
        
    
    



