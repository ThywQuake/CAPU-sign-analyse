# README
## How to use

These codes are used for collecting data of CAPU signs. 
Due to the easy accessiblity of sign data in the website, 
You can use ==update.py== to gain data by using proper functions. You can use ==analyse.py== to process the data already stored in the folder 'datas_daily'.
==Important: Do change the path in these two .py files before you start!==

## Data struct
### 1.datas_daily

```
/datas_daily/year/month/day
#Notice: This is a file storing a python object (pickle needed), it contains a dict:
{ID:sign_rank}
ID: string
sign_rank: string
```
### 2.Analyse
```
Analyse.signs()=[sum_of_signs]
sum_of_signs: int

Analyse.signer(ID)={date:sign_rank}
date: datetime
sign_rank: int
```

### 3.datas_person
```
/datas_person/register
{date:ID}
date: datetime
ID: array of string

/datas_person/id_md5
#Notice: the file name is the MD5 format of ID
{date:rank}
date: datetime
rank: int

```
