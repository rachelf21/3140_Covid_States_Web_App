import timeit
import requests
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
from operator import itemgetter 

class DataSource:
    data_source_name = 'Source'
    data_source_id = 0
    logo = ''
    latest_date = date.today()

#USA Attributes
    url_usa = ''
    usa_data = []  #all usa data. parse this to get specific data. Except for NYT - 
    usa_total_cases = 0
    usa_total_deaths = 0
    usa_increase_cases = 0
    usa_increase_deaths = 0
    usa_cases = [] #this list of cases is passed to the plotly function to be plotted
    usa_deaths = [] #this list of deaths is passed to the plotly function to be plotted
    usa_dates = [] #this list of dates is passed to the plotly function to be plotted

#State Attributes    
    url_state = ''
    state_data = [] #all state data. parse this to get specific data
    state_total_cases = 0
    state_total_deaths = 0
    state_increase_cases = 0
    state_increase_deaths = 0
    state_cases = [] #this list of cases is passed to the plotly function to be plotted
    state_deaths = [] #this list of deaths is passed to the plotly function to be plotted
    state_dates = [] #this list of dates is passed to the plotly function to be plotted
    states_current = []
    df = []
#%%            
class DataSourceNYT(DataSource):
    data_source_name = 'New York Times'
    data_source_id = 1
    logo = "nyt"
    url_usa = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    url_state = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'

    def retrieve_data_usa(self):
        usa_data = pd.read_csv(self.url_usa, error_bad_lines=False)
        usa_data['date'] = pd.to_datetime(usa_data['date'], format="%Y-%m-%d" )
        usa_data['date'] = usa_data['date'].dt.date
        usa_data['case_increase']=(usa_data.cases - usa_data.cases.shift(1))
        usa_data['death_increase']=(usa_data.deaths - usa_data.deaths.shift(1))
        self.latest_date = usa_data['date'].iloc[-1]
        self.usa_total_cases = '{:,.0f}'.format(usa_data['cases'].iloc[-1])
        self.usa_total_deaths = '{:,.0f}'.format(usa_data['deaths'].iloc[-1])
        self.usa_increase_deaths = '{:,.0f}'.format(usa_data['death_increase'].iloc[-1])
        self.usa_increase_cases = '{:,.0f}'.format(usa_data['case_increase'].iloc[-1])
        self.usa_cases = usa_data['case_increase']
        self.usa_deaths = usa_data['death_increase']
        self.usa_dates = usa_data['date']
        self.latest_date = usa_data['date'].iloc[-1]   

        print("retrieving USA data from NYT")
     
    def retrieve_data_state(self, state):
        self.state_data = pd.read_csv(self.url_state, error_bad_lines=False)
        self.state_data['date'] = pd.to_datetime(self.state_data['date'], format="%Y-%m-%d" )
        self.state_data['date'] = self.state_data['date'].dt.date
        self.state_data = self.state_data[self.state_data.state==state]
        self.state_total_cases = self.state_data['cases'].iloc[-1]
        self.state_total_deaths = self.state_data['deaths'].iloc[-1]
        self.state_data['case_increase']=(self.state_data.cases - self.state_data.cases.shift(1))
        self.state_data['death_increase']=(self.state_data.deaths - self.state_data.deaths.shift(1))
        self.state_increase_deaths = '{:,.0f}'.format(self.state_data['death_increase'].iloc[-1])
        self.state_increase_cases = '{:,.0f}'.format(self.state_data['case_increase'].iloc[-1])
        self.state_cases = self.state_data['case_increase']
        self.state_deaths = self.state_data['death_increase']
        self.state_dates = self.state_data['date']
        self.latest_date = self.state_data['date'].iloc[-1]   
        
        print("retrieving state data from NYT")
        #state_data = state_data[state_data.date >= starting_date]
        
    def retrieve_current_states(self):
        self.state_data = pd.read_csv(self.url_state, error_bad_lines=False)
        self.state_data['date'] = pd.to_datetime(self.state_data['date'], format="%Y-%m-%d" )
        self.state_data['date'] = self.state_data['date'].dt.date
        self.state_data.sort_values(by=['date','state'], inplace=True, ascending=False)
        curr_date = self.state_data[['date']].values[0][0]
        yest_date = curr_date - timedelta(days=1)
        states_latest = self.state_data[self.state_data.date==curr_date]  
        states_yest =  self.state_data[self.state_data.date==yest_date]
        states_latest = states_latest.append(states_yest, ignore_index=True)
        df = states_latest.assign(cases_increase=0)
        df = states_latest.assign(deaths_increase=0)    
        df.sort_values(by=['state','date'],inplace=True)
        mask = df.duplicated(['state'])
        df['cases_increase'] = np.where(mask, df['cases']-df['cases'].shift(1), np.nan)
        df['deaths_increase'] = np.where(mask, df['deaths']-df['deaths'].shift(1), np.nan)
        df.fillna(0, inplace=True)
        self.states_current = df
        
        
    def get_max_cases(self):
        self.states_current.sort_values(by=['cases_increase'],inplace=True, ascending=False)
        states = []
        max_cases = []
        max_deaths = []
        states = list(self.states_current['state'])
        max_cases = list(self.states_current['cases_increase'])
        max_deaths = list(self.states_current['deaths_increase'])
        return states, max_cases, max_deaths  

    def get_max_deaths(self):
        self.states_current.sort_values(by=['deaths_increase'],inplace=True, ascending=False)
        states = []
        max_cases = []
        max_deaths = []
        states = list(self.states_current['state'])
        max_cases = list(self.states_current['cases_increase'])
        max_deaths = list(self.states_current['deaths_increase'])
        return states, max_deaths, max_cases 
           
#%% Covid Tracking Project    
class DataSourceCTP(DataSource):
    data_source_name = 'Covid Tracking Project'
    data_source_id = 2
    logo = "ctp"
    url_usa = 'https://api.covidtracking.com/v1/us/daily.json'
    url_state = 'https://api.covidtracking.com/v1/states/daily.json'
    url_states_current = ' https://api.covidtracking.com/v1/states/current.json'

    def retrieve_data_usa(self):
        response = requests.get(self.url_usa)
        if response.status_code >= 400:
            print('Error retrieving data') #output to html doc
        else:
            self.usa_data = response.json()
            s = str(self.usa_data[0]['date'])           
            self.latest_date = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8])).date()
            self.usa_total_cases = '{:,.0f}'.format(self.usa_data[0]['positive'])
            self.usa_total_deaths = '{:,.0f}'.format(self.usa_data[0]['death'])    
            self.usa_increase_cases = '{:,.0f}'.format(self.usa_data[0]['positiveIncrease'])
            self.usa_increase_deaths = '{:,.0f}'.format(self.usa_data[0]['deathIncrease'])
            self.usa_data.reverse()
            print("retrieving USA data from CTP")
    
            self.usa_cases.clear()
            self.usa_deaths.clear()
            self.usa_dates.clear()
            usa_temp_dates = []
             
            for info in self.usa_data:
                self.usa_cases.append(info['positiveIncrease'])
                self.usa_deaths.append(info['deathIncrease'])
                usa_temp_dates.append(str(info['date']))
                
            for s in usa_temp_dates:
                date1 = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]))
                self.usa_dates.append(date1)
                
    def retrieve_current_states(self):
        response = requests.get(self.url_states_current)
        if response.status_code >= 400:
            print('Error retrieving data') #output to html doc
        else:        
            self.states_current = response.json()
            
    def get_max_cases(self):
            self.states_current = sorted(self.states_current, key=itemgetter('positiveIncrease'), reverse=True)
            states = []
            max_cases = []
            max_deaths = []
            for item in self.states_current:
                states.append(item['state'])
                max_cases.append(item['positiveIncrease'])
                max_deaths.append(item['deathIncrease'])
            return states, max_cases, max_deaths
    
    def get_max_deaths(self):
            self.states_current = sorted(self.states_current, key=itemgetter('deathIncrease'), reverse=True)
            states = []
            max_deaths = []
            max_cases = []
            for item in self.states_current:
                states.append(item['state'])
                max_deaths.append(item['deathIncrease'])
                max_cases.append(item['positiveIncrease'])
            return states, max_deaths, max_cases
            
    def retrieve_data_state(self,state):
        start = timeit.default_timer()
        response = requests.get(self.url_state)
        if response.status_code >= 400:
            print('Error retrieving data') #output to html doc
        else:
            self.state_data = response.json()
            self.state_data = list(filter(lambda row: row['state'] == state, self.state_data))
            stop = timeit.default_timer()
            print("Time for retrieving state data {:.2f}".format(stop-start))
            s = str(self.state_data[0]['date'])
            self.latest_date = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8])).date()
            self.state_total_cases = '{:,.0f}'.format(self.state_data[0]['positive'])
            self.state_total_deaths = '{:,.0f}'.format(self.state_data[0]['death'])    
            self.state_increase_cases = '{:,.0f}'.format(self.state_data[0]['positiveIncrease'])
            self.state_increase_deaths = '{:,.0f}'.format(self.state_data[0]['deathIncrease'])
            self.state_data.reverse()
            print("retrieving USA data from CTP")
    
            self.state_cases.clear()
            self.state_deaths.clear()
            self.state_dates.clear()
            state_temp_dates = []
             
            for info in self.usa_data:
                self.state_cases.append(info['positiveIncrease'])
                self.state_deaths.append(info['deathIncrease'])
                state_temp_dates.append(str(info['date']))
                
            for s in state_temp_dates:
                date1 = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]))
                self.state_dates.append(date1)

#%% Our World in Data              
class DataSourceOWID(DataSource):
    data_source_name = 'Our World in Data'
    data_source_id = 3
    logo = "owid"
    url_usa = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.json'
    
    def retrieve_data_usa(self):
        response = requests.get(self.url_usa)
        if response.status_code >= 400:
            print('Error retrieving data') #output to html doc
        else:          
            self.usa_data = response.json()['USA']['data']
            s = self.usa_data[-1]['date']          
            self.latest_date = datetime(year=int(s[0:4]), month=int(s[5:7]), day=int(s[8:10])).date()
            self.usa_total_cases = '{:,.0f}'.format(self.usa_data[-1]['total_cases'])
            self.usa_total_deaths = '{:,.0f}'.format(self.usa_data[-1]['total_deaths'])    
            self.usa_increase_cases = '{:,.0f}'.format(self.usa_data[-1]['new_cases'])
            self.usa_increase_deaths = '{:,.0f}'.format(self.usa_data[-1]['new_deaths'])
            print("retrieving USA data from OWID")
    
            self.usa_cases.clear()
            self.usa_deaths.clear()
            self.usa_dates.clear()
            usa_temp_dates = []
             
            for info in self.usa_data:
                self.usa_cases.append(info['new_cases'])
                self.usa_deaths.append(info['new_deaths'])
                usa_temp_dates.append(str(info['date']))
                
            for s in usa_temp_dates:
                date1 = datetime(year=int(s[0:4]), month=int(s[5:7]), day=int(s[8:10]))
                self.usa_dates.append(date1)

#%%
nyt = DataSourceNYT()
nyt.retrieve_current_states()
a, b, c = nyt.get_max_deaths()

ctp = DataSourceCTP()
ctp.retrieve_current_states()

