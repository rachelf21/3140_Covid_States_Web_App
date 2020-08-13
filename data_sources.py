import requests
from datetime import date, datetime
import pandas as pd

class DataSource:
    data_source_name = 'Source'
    data_source_id = 0
    url_usa = ''
    # url_states_today = 'https://api.covidtracking.com/v1/states/current.json'
    # url_states = 'https://api.covidtracking.com/v1/states/daily.json'
    usa_data = []
    usa_total_cases = 0
    usa_total_deaths = 0
    usa_increase_cases = 0
    usa_increase_deaths = 0
    usa_cases = []
    usa_deaths = [] 
    usa_temp_dates = []
    usa_dates = []
    latest_date = date.today()
    logo = ''
    

        
class DataSourceNYT(DataSource):
    data_source_name = 'New York Times'
    data_source_id = 1
    logo = "nyt"
    url_usa = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'

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

        print("retrieving USA data from NYT")

#%% Covid Tracking Project    
class DataSourceCTP(DataSource):
    data_source_name = 'Covid Tracking Project'
    data_source_id = 2
    logo = "ctp"
    url_usa = 'https://api.covidtracking.com/v1/us/daily.json'
    
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
            self.usa_temp_dates.clear()
            self.usa_dates.clear()
             
            for info in self.usa_data:
                self.usa_cases.append(info['positiveIncrease'])
                self.usa_deaths.append(info['deathIncrease'])
                self.usa_temp_dates.append(str(info['date']))
                
            for s in self.usa_temp_dates:
                date1 = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]))
                self.usa_dates.append(date1)

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
            self.usa_temp_dates.clear()
            self.usa_dates.clear()
             
            for info in self.usa_data:
                self.usa_cases.append(info['new_cases'])
                self.usa_deaths.append(info['new_deaths'])
                self.usa_temp_dates.append(str(info['date']))
                
            for s in self.usa_temp_dates:
                date1 = datetime(year=int(s[0:4]), month=int(s[5:7]), day=int(s[8:10]))
                self.usa_dates.append(date1)

#%%
owid = DataSourceOWID()
owid.retrieve_data_usa()
