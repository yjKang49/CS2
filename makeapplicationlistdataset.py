# -*- coding: utf-8 -*-
"""makeApplicationListDataset.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kmKiIrtF0MxmXb48EtyprSALOANqG-TX
"""

import json
import random
import pandas as pd
import numpy as np
from collections import OrderedDict

file_data = OrderedDict()

dataframe = pd.read_csv('/content/adjusted-name-combinations-list.csv')
dataframe = dataframe.rename(columns = {'Unnamed: 0': 'id'})
df = dataframe.drop(['Adjustment', 'Estimate', 'finalEstimate'], axis = 1)
df

n = 400     # 데이터 개수
status = ['APP', 'REC', 'VER', 'REQ', 'RET', 'COM', 'REJ']  # 'applied', 'received', 'verified', 'requested', 'returned', 'completed', 'rejected'
type = ['NEW', 'REN', 'REK', 'REV', 'SUP', 'REC']
phone_random = random.sample(range(10000000,99999999),400)      # 랜덤으로 추출
phone = list(map(str, phone_random))  # list의 데이터를 str로 형변환
organ = ['samsung', 'tesla', 'apple', 'intel', 'ibm', 'amazon', 'skhynix', 'hyundai']
organUnit = ['executiveManager', 'seniorManager', 'manager', 'assistantManager', 'associate', 'staff', 'intern']  # 부장, 차장, 과장, 대리, 주임, 사원, 인턴
certId_random = random.sample(range(10000,99999),n)
certId = list(map(str, certId_random))
certType = ['naturalPerson', 'legalPerson', 'device', 'ETC']
certPeriod_random = [random.randint(1, 4) for i in range(n)]
certPeriod = list(map(str, certPeriod_random))
phoneCarrier = ['SKT', 'KT', 'LG']
month = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12' ]
day = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
rrn1 = list(map(str, np.random.randint(30, 100, size = n)))
rrn2 = [random.choice(month) for i in range(n)]
rrn3 = [random.choice(day) for i in range(n)]
rrn4 = list(map(str, np.random.randint(1,3, size = n)))
rrn5 = list(map(str, random.sample(range(100000, 999999), n )))
ra = ['likebnb', 'katherine']
ca = ['admin', 'subadmin']

df['status'] = [random.choice(status) for i in range(n)]      # 특정범위(list)에서 중복을 허용하여 랜덤 추출
df['type'] = [random.choice(type) for i in range(n)]
df['userId'] = df['cleanName'].str.replace(" ", "")     # 공백제거
df['phone'] = ['010'+phone[i] for i in range(n)]
df['user'] = df['FirstName'] +' '+ df['Surname']
df['organ'] = [random.choice(organ) for i in range(n)]
df['organUnit'] = [random.choice(organUnit) for i in range(n)]
df['country'] = ['KR' if x in ['samsung', 'skhynix', 'hyundai'] else 'US' for x in df['organ']]
df['province'] = ['Seoul' if x == 'KR' else 'California' for x in df['country']]
df['locality'] = ['01' if x == 'Seoul' else '02' for x in df['province']]
df['email'] = [ df['userId'][i] + '@' + df['organ'][i] + '.com' for i in range(n)]
df['certId'] = certId
df['certType'] = [random.choice(certType) for i in range(n)]
df['certPeriod'] =  certPeriod        #인증서기간 1년,2년,etc
df['agreedTc'] = '1'      # 1은 true(yes), 0은 false(no)
df['phoneCarrier'] = [random.choice(phoneCarrier) for i in range(n)]
df['rrn'] = [rrn1[i] + rrn2[i] + rrn3[i] + rrn4[i] + rrn5[i] for i in range(n)]
df['ra'] = [random.choice(ra) for i in range(n)]
df['ca'] = [random.choice(ca) for i in range(n)]
df

df['certId'].nunique()           #certId 유니크한지 검사

from datetime import datetime, timedelta
import random

# 시작일과 종료일 설정
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 12, 31)
phoneAuthTs = []

for i in range(n):
    # 랜덤한 날짜 생성
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

    # 랜덤한 시간 생성
    random_time = random.randint(0, 24 * 60 * 60 - 1)  # 0부터 1일의 초 단위까지의 랜덤한 시간 생성

    # 랜덤한 날짜와 시간을 합쳐서 datetime 객체 생성
    random_datetime = random_date.replace(hour=random_time // 3600, minute=(random_time % 3600) // 60, second=random_time % 60)

    # datetime 객체를 timestamp로 변환
    timestamp = random_datetime.timestamp()
    phoneAuthTs.append(int(timestamp))

print(phoneAuthTs)

# status = ['APP', 'REC', 'VER', 'REQ', 'RET', 'COM', 'REJ']
emailAuthTs = [phoneAuthTs[i] + (5 * 60) for i in range(n)]  # 5분
applicatedTs = [emailAuthTs[i] + (5 * 60) for i in range(n)] #5분
receivedTs = [applicatedTs[i] + (5 * 60) if df['status'][i] != 'APP' else 0 for i in range(n)] #5분
verifiedTs = [receivedTs[i] + (5 * 60) if df['status'][i] not in ['APP', 'REC'] else 0 for i in range(n)] #5분
returnedTs = [verifiedTs[i] + (5 * 60) if df['status'][i] == 'RET' else 0 for i in range(n)]
requestedTs = [verifiedTs[i] + (5 * 60) if df['status'][i] in ['REQ', 'COM', 'REJ'] else 0 for i in range(n)]
rejectedTs = [requestedTs[i] + (5 * 60) if df['status'][i] =='REJ' else 0 for i in range(n)]
completedTs = [requestedTs[i] + (5 * 60) if df['status'][i] =='COM' else 0 for i in range(n)]

df['phoneAuthTs'] = phoneAuthTs
df['emailAuthTs'] = emailAuthTs
df['applicatedTs'] = applicatedTs
df['receivedTs'] = receivedTs
df['verifiedTs'] = verifiedTs
df['returnedTs'] = returnedTs
df['requestedTs'] = requestedTs
df['rejectedTs'] = rejectedTs
df['completedTs'] = completedTs
df.loc[:50, ['status', 'applicatedTs', 'receivedTs', 'verifiedTs', 'returnedTs', 'requestedTs', 'rejectedTs', 'completedTs' ]]

df.drop(columns = ['FirstName', 'Surname', 'cleanName'], inplace = True)
df

# dataframe을 json 파일로 변환.
df.to_json('dataframe_records.json', orient = 'records' )       # orient는 생성할 json 파일의 format을 의미. columns, index, records, values, split 다섯종류







# 참고
# timestamp 형식을 yyyy-mm-dd HH:MM 형식으로 변환
s1 = pd.to_datetime(df['applicatedTs'], unit="s") # unit은 밀리세컨드로 설정
# time_data는 위 timestamp 데이터의 변수
s1.dt.strftime("%Y-%m-%d %H:%M")



