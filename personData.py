from analyse import Analyse
import analyse
import update as upd
import pickle
import os
import hashlib
# Using hashlib to cover some corner cases in IDs such as containing \/.?|<> etc.
from datetime import timedelta

root=r'./datas_person'
register_path=r'./datas_person/register'

if not os.path.exists(root):
    os.mkdir(root)
a=Analyse('2014-01-01','2023-11-17')
ids=set(os.listdir(root))
ids.remove('register')
ids.remove('register_keyerror')
def get_data():
    current_date=a.start_date
    while current_date!=a.end_date:
        buffer=analyse.get_buffer_from_date(current_date)
        print(f'\nCurrent Date: {current_date} ...')
        for id in buffer.keys():
            id_md5=hashlib.md5(id.encode('utf-8')).hexdigest()
            if not id_md5 in ids:
                ids.add(id_md5)
                print(f'{len(ids)} : Getting data from {id} ...')
                path=root+os.sep+id_md5
                signer=a.get_signer(id)
                signer['ID']=id
                with open(path,'wb') as f:
                    pickle.dump(signer,f)
        current_date+=timedelta(days=1)

def get_register():
    register={}
    keyerror={}
    current_date=a.start_date
    while current_date!=a.end_date:
        register[current_date]=[]
        current_date+=timedelta(days=1)
    i=1
    for id_md5 in ids:
        path=root+os.sep+id_md5
        with open(path,'rb') as f:
            signer=pickle.load(f)
            try:
                id=signer.pop('ID')
                print(f'{i}/{len(ids)}Loading {id}')
                for date in signer.keys():
                    if signer[date]:
                        register_date=date
                        register[register_date].append(id)
                        break
            except KeyError:
                print(f'KeyError: {id_md5}')
                keyerror[id_md5]=signer
        i+=1
    with open(register_path,'wb') as f:
        print('Saving register ...')
        pickle.dump(register,f)
    with open(register_path+'_keyerror','wb') as f:
        print(f'Saving keyerror ...\n'
              f'{len(keyerror)} keyerrors in total.')
        pickle.dump(keyerror,f)

def get_keyerror():
    with open(register_path+'_keyerror','rb') as f:
        keyerror=pickle.load(f)
    return keyerror.keys()

def print_register():
    with open(register_path,'rb') as f:
        register=pickle.load(f)
    for k,v in register.items():
        print(f'{k} : {v}')
