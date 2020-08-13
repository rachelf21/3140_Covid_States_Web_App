import timeit
import requests
import pandas as pd

data = []
st_case_increase = []
st_death_increase = []
st_dates=[]
curr_date = ''
states = [] #keep track of states with most cases/deaths, in desc order

# LOADING DATA WITH requests
start = timeit.default_timer()
response= requests.get('https://api.covidtracking.com/v1/states/daily.json')

if response.status_code == 200:
    for info in response.json():
        if info['state']=='NY':
            #data.append(info)
            st_dates.append(info['date']) 
            st_case_increase.append(info['positiveIncrease']) 
            st_death_increase.append(info['deathIncrease'])

            # print(info['date'], info['positiveIncrease']) #print dictionary item
    st_dates.reverse()
    st_case_increase.reverse()
    st_death_increase.reverse()
    
# for day in data:  #print list
#     print(day['date'], day['positiveIncrease']) #dictionary item within list

stop = timeit.default_timer()
print('Time json: {:.2f}'.format(stop - start))

start = timeit.default_timer()
response = requests.get('https://api.covidtracking.com/v1/states/current.json')
if response.status_code == 200:
    for info in response.json():
        data.append(info)        
data = sorted(data, key = lambda i: i['deathIncrease'], reverse=True)   

for entry in data:
    states.append(entry['state']) 
                        
stop = timeit.default_timer()
print('Time json2: {:.2f}'.format(stop - start))
            
            
# #LOADING DATA WITH pandas

# start = timeit.default_timer()

# content = pd.read_json(r'https://api.covidtracking.com/v1/states/daily.json')
# st_case_increase = content['positiveIncrease']
# st_dates = content['date']
# st_death_increase = content['deathIncrease']

# stop = timeit.default_timer()
# print('Time pandas: {:.2f}'.format(stop - start))
