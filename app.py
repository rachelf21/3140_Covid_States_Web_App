from flask import Flask, render_template, url_for, jsonify, request
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import plotly 
import plotly.graph_objs as go

user_state = "Idaho"
selected_state = "California"
selected_state2 = "California"
selected_state3 = "California"
max_3_cases=[]
max_3_deaths=[]
curr_date = ''

color1 = 'rgb(56,83,93)'
color2 = 'rgb(61,116,137)'
color3 = 'rgb(67,149,179)'
color4 = 'rgb(85,174,200)'
color5 = 'rgb(116,191,195)'
color6 = 'rgb(148,208,191)'
teal = 'rgba(109, 43, 173)'
purple = 'rgb(85, 41, 116)'
green = 'rgb(32,171,125)'
orange = 'rgb(255,124,48)'

graphJSON_usa_cases="[]"
graphJSON_usa_deaths="[]"
graphJSON_states_cases="[]"
graphJSON_states_deaths="[]"
graphJSON_states2_cases="[]"
graphJSON_states2_deaths="[]"
graphJSON_states3_cases="[]"
graphJSON_states3_deaths="[]"
graphsJSON_cases = []
graphsJSON_deaths = []
st_increase_deaths = st_increase_cases = 0
usa_increase_deaths = usa_increase_cases = 0
curr_date = ''

def get_usa_data():
    global usa_increase_cases, usa_increase_deaths
    usa_data = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv", error_bad_lines=False)
    usa_data['date'] = pd.to_datetime(usa_data['date'], format="%Y-%m-%d" )
    usa_data['date'] = usa_data['date'].dt.date
    usa_data['case_increase']=(usa_data.cases - usa_data.cases.shift(1))
    usa_data['death_increase']=(usa_data.deaths - usa_data.deaths.shift(1))
    usa_increase_deaths = '{:,.0f}'.format(usa_data['death_increase'].iloc[-1])
    usa_increase_cases = '{:,.0f}'.format(usa_data['case_increase'].iloc[-1])
    curr_date = usa_data['date'].iloc[-1]
    print("retrieving USA data")
    return usa_data

usa_data = get_usa_data()

def get_states_data(state):
    global st_increase_deaths, st_increase_cases
    states_data = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv", error_bad_lines=False)
    states_data['date'] = pd.to_datetime(states_data['date'], format="%Y-%m-%d" )
    states_data['date'] = states_data['date'].dt.date
    st = state
    states_data = states_data[states_data.state==st]
    states_data['case_increase']=(states_data.cases - states_data.cases.shift(1))
    states_data['death_increase']=(states_data.deaths - states_data.deaths.shift(1))
    st_increase_deaths = '{:,.0f}'.format(states_data['death_increase'].iloc[-1])
    st_increase_cases = '{:,.0f}'.format(states_data['case_increase'].iloc[-1])
    curr_date = states_data['date'].iloc[-1]   
    print("retrieving states data")
    return states_data

stdata=get_states_data(selected_state)

def get_max_increase(category):
    global selected_state, selected_state2, selected_state3, max_3_cases, max_3_deaths, curr_date
    max_3_cases=[]
    max_3_deaths=[]
    states_data = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv", error_bad_lines=False)
    states_data['date'] = pd.to_datetime(states_data['date'], format="%Y-%m-%d" )
    states_data['date'] = states_data['date'].dt.date
    states_data.sort_values(by=['date','state'], inplace=True, ascending=False)
    curr_date = states_data[['date']].values[0][0]
    yest_date = curr_date - timedelta(days=1)
    states_latest = states_data[states_data.date==curr_date]  
    states_yest =  states_data[states_data.date==yest_date]
    states_latest = states_latest.append(states_yest, ignore_index=True)
    df = states_latest.assign(cases_increase=0)
    df = states_latest.assign(deaths_increase=0)    
    df.sort_values(by=['state','date'],inplace=True)
    mask = df.duplicated(['state'])
    df['cases_increase'] = np.where(mask, df['cases']-df['cases'].shift(1), np.nan)
    df['deaths_increase'] = np.where(mask, df['deaths']-df['deaths'].shift(1), np.nan)
    if(category=="cases"): #cases
        print(category, "max cases")
        df.sort_values(by=['cases_increase'],inplace=True, ascending=False)
        # for i in range(0,3):
        #     max_3_cases.append('{:.0f}'.format(df.cases_increase.iloc[i]))
        #     max_3_deaths.append('{:.0f}'.format(df.deaths_increase.iloc[i]))
        # print("max cases = ", max_3_cases)
    else: #deaths
        print(category, "max deaths")
        df.sort_values(by=['deaths_increase'],inplace=True, ascending=False)
    for i in range(0,3):
        max_3_cases.append('{:.0f}'.format(df.cases_increase.iloc[i]))
        max_3_deaths.append('{:.0f}'.format(df.deaths_increase.iloc[i]))
    df = df.reset_index(drop=True)
    selected_state = df.state[0]
    selected_state2 = df.state[1]
    selected_state3 = df.state[2]
    print("state with largest increase in", category, selected_state)
    print("state with second largest increase in", category, selected_state2)
    print("state with third largest increase in", category, selected_state3)
    return df
    
max_cases = get_max_increase("cases")    
max_deaths = get_max_increase("deaths")    

def create_states2_chart(my_data=get_states_data(selected_state2)): 
    global graphJSON_states2_cases, graphJSON_states2_deaths, graphsJSON_cases, graphsJSON_deaths
    
    trace_states_cases = go.Bar (
        x = my_data.date,
        y = my_data.case_increase,
        marker_color = orange,
        opacity = .5
        )
    data = [trace_states_cases]
    
    graphJSON_states2_cases = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder) 
    graphsJSON_cases.append(graphJSON_states2_cases)

    trace_states_deaths = go.Bar (
        x = my_data.date,
        y = my_data.death_increase,
        marker_color = purple,
        opacity = .5
        )
    data = [trace_states_deaths]
    graphJSON_states2_deaths = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder) 
    graphsJSON_deaths.append(graphJSON_states2_deaths)

    print("generating states2or3 chart")
    
    return graphJSON_states2_cases, graphJSON_states2_deaths

    
app = Flask(__name__)


@app.route('/get_usa_chart/')
def create_usa_chart(my_data=get_usa_data()): 
    global graphJSON_usa_cases, graphJSON_usa_deaths
    
    trace_usa_cases = go.Bar (
        x = my_data.date,
        y = my_data.case_increase,
        marker_color = orange,
        opacity = .5
        )
    data = [trace_usa_cases]
    
    graphJSON_usa_cases = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder) 
    
    trace_usa_deaths = go.Bar (
        x = my_data.date,
        y = my_data.death_increase,
        marker_color = purple,
        opacity = .5
        )
    data = [trace_usa_deaths]
    graphJSON_usa_deaths = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder) 
     
    print("generating usa chart")
    return render_template('usa.html',  graphJSON_usa_cases=graphJSON_usa_cases, 
                           graphJSON_usa_deaths=graphJSON_usa_deaths,
                           usa_increase_deaths = usa_increase_deaths,
                           usa_increase_cases = usa_increase_cases,
                           curr_date = curr_date)


@app.route('/get_states_chart/')  #this route is note being used but the function is
def create_states_chart(my_data=get_states_data(selected_state)): 
    global graphJSON_states_cases, graphJSON_states_deaths, graphsJSON_cases, graphsJSON_deaths
    graphsJSON_cases=[] 
    graphsJSON_deaths=[]
    
    trace_states_cases = go.Bar (
        x = my_data.date,
        y = my_data.case_increase,
        marker_color = orange,
        opacity = .5
        )
    data = [trace_states_cases]
    
    graphJSON_states_cases = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder) 
    graphsJSON_cases.append(graphJSON_states_cases)
    
    trace_states_deaths = go.Bar (
        x = my_data.date,
        y = my_data.death_increase,
        marker_color = purple,
        opacity = .5
        )
    data = [trace_states_deaths]
    graphJSON_states_deaths = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder) 
    graphsJSON_deaths.append(graphJSON_states_deaths)
 
    print("generating states chart")
    return render_template('index.html',  graphJSON_states_cases=graphJSON_states_cases, graphJSON_states_deaths=graphJSON_states_deaths)


@app.route('/get_max/<category>')
def get_max(category):
    get_max_increase(category)
    create_states_chart(my_data=get_states_data(selected_state))
    graphJSON_states2_cases, graphJSON_states2_deaths = create_states2_chart(my_data=get_states_data(selected_state2))
    graphJSON_states3_cases, graphJSON_states3_deaths = create_states2_chart(my_data=get_states_data(selected_state3))
    print("generating states chart from mask", category)
    return render_template('top_states.html',  
                           selected_state = selected_state, 
                           selected_state2 = selected_state2, 
                           selected_state3 = selected_state3, 
                           curr_date = curr_date,
                           graphJSON_states_cases = graphJSON_states_cases,
                           graphJSON_states_deaths = graphJSON_states_deaths,
                           graphJSON_states2_cases = graphJSON_states2_cases,
                           graphJSON_states2_deaths = graphJSON_states2_deaths,
                           graphJSON_states3_cases = graphJSON_states3_cases,
                           graphJSON_states3_deaths = graphJSON_states3_deaths,
                           max_3_cases = max_3_cases,
                           max_3_deaths = max_3_deaths,
                           graphsJSON_cases = graphsJSON_cases,
                           graphsJSON_deaths = graphsJSON_deaths)


@app.route('/SomeFunction')
def SomeFunction():
    print('In SomeFunction')
    return "Nothing"

@app.route('/get_state', methods=['POST'])
def get_state():
    global user_state
    user_state = request.form['state']
    create_states_chart(my_data=get_states_data(user_state))
    print("User selected state: ", user_state)
    selected_state = user_state
    return render_template('select_state.html',  
                           selected_state = selected_state, 
                           graphJSON_states_cases=graphJSON_states_cases, 
                           graphJSON_states_deaths=graphJSON_states_deaths,
                           curr_date = curr_date,
                           st_increase_deaths = st_increase_deaths,
                           st_increase_cases = st_increase_cases,
                           )

@app.route('/states_page')
def states_page():
    return render_template('select_state.html')    

@app.route('/about.html')
def about():
    return render_template('about.html')   
 
@app.route('/')
def index():
    global graphJSON_usa_cases, graphJSON_usa_deaths;
    graphJSON_usa_cases="[]"
    graphJSON_usa_deaths="[]"
    create_usa_chart(my_data=get_usa_data())
    return render_template('usa.html', graphJSON_usa_cases=graphJSON_usa_cases, graphJSON_usa_deaths=graphJSON_usa_deaths, selected_state = selected_state, selected_state2 = selected_state2)


if __name__ == '__main__':
  app.run(debug=True)