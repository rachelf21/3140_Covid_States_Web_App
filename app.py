from flask import Flask, render_template, url_for, jsonify, request, redirect, flash
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import plotly 
import plotly.graph_objs as go
from forms import Top_States_Form
from data_sources import DataSourceCTP, DataSourceNYT, DataSourceOWID
from state_abbrev import State_Abbrev

info = DataSourceNYT()
data_source = 'New York Times'
logo = ""
curr_date = ''

##GLOBAL USA VARIABLES
usa_total_cases = 0
usa_total_deaths = 0
usa_increase_deaths = 0
usa_increase_cases = 0

##GLOBAL STATE VARIABLES
state_total_cases = 0
state_total_deaths = 0
state_increase_cases = 0
state_increase_deaths = 0
#go through these:
user_state = ""
selected_state = "California"
starting_date = datetime(2020, 3, 1).date()
max_cases = []
max_deaths = []
graphJSON_usa_cases="[]"
graphJSON_usa_deaths="[]"
graphJSON_states_cases="[]"
graphJSON_states_deaths="[]"
states = []
df_states = []
data_cases = []
data_deaths = []
top = 3

##COLOR SCHEME
color1 = 'rgb(56,83,93)'
color2 = 'rgb(61,116,137)'
color3 = 'rgb(67,149,179)'
color4 = 'rgb(85,174,200)'
color5 = 'rgb(116,191,195)'
color6 = 'rgb(148,208,191)'
#teal = 'rgb(109, 43, 173)'  
teal = 'rgb(67, 149, 179)'
green = 'rgb(87,24,69)'
purple = 'rgb(85, 41, 116)'
burgundy = 'rgb(144, 12, 62)'
red = 'rgb(199,0,57)'
orange = 'rgb(255,87,51)'
yellow = 'rgb(255,195,0)'

    
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


#1  DONE
def get_usa_data():
    global data_source, usa_increase_cases, usa_increase_deaths, usa_total_cases, usa_total_deaths, curr_date, logo, info
    
    if data_source == 'Covid Tracking Project':
        info = DataSourceCTP()
    elif data_source == 'Our World in Data':
        info = DataSourceOWID()
    else:
        info = DataSourceNYT()
        
    info.retrieve_data_usa()
    data_source = info.data_source_name
    usa_increase_cases = info.usa_increase_cases
    usa_increase_deaths = info.usa_increase_deaths
    usa_total_cases = info.usa_total_cases
    usa_total_deaths = info.usa_total_deaths
    curr_date = info.latest_date
    logo = info.logo
    return info

#5  DONE
@app.route('/get_usa_chart/')
def create_usa_chart():
    global graphJSON_usa_cases, graphJSON_usa_deaths, usa_increase_deaths, usa_increase_cases

    info = get_usa_data()
    data_source = info.data_source_name
    
    graphJSON_usa_cases = create_chart(info.usa_dates, info.usa_cases, orange, .95)
    graphJSON_usa_deaths = create_chart(info.usa_dates, info.usa_deaths, burgundy, .95)
 
    print("Generating usa charts with data from", data_source)
    return render_template('usa.html',  
                           graphJSON_usa_cases=graphJSON_usa_cases, 
                           graphJSON_usa_deaths=graphJSON_usa_deaths,
                           usa_increase_deaths = usa_increase_deaths,
                           usa_increase_cases = usa_increase_cases,
                           curr_date = curr_date,
                           data_source = data_source,
                           logo = logo)

#NEW FUNCTION TO TAKE x and y data as arguments and return json string to then pass on to plotly  DONE
def create_chart(dates, values, my_color, my_opacity ):
    trace_data = go.Bar(
        x = dates,
        y = values,
        marker_color = my_color,
        opacity = my_opacity)
    data = [trace_data]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


#2  WORK ON THIS NEXT
def get_states_data(state, starting_date):
    global data_source, curr_date, logo, state_increase_cases, state_increase_deaths, state_total_cases,state_total_deaths, info
    
    if info.data_source_id == 2:
        state = State_Abbrev().get_abbrev(state)
    elif info.data_source_id == 3:
        info = DataSourceNYT() #no states data from OWID

    info.retrieve_data_state(state)
    data_source = info.data_source_name
    state_total_cases = info.state_total_cases
    state_total_deaths = info.state_total_deaths
    state_increase_cases = info.state_increase_cases
    state_increase_deaths = info.state_increase_deaths

    curr_date = info.latest_date
    logo = info.logo
    return info
    
stdata=get_states_data(selected_state, starting_date)

#4
def create_states2_chart(): 
    global graphJSON_states2_cases, graphJSON_states2_deaths, info
    
    info = get_states_data(selected_state, starting_date)       
    graphJSON_states2_cases = create_chart(info.state_dates, info.state_cases, orange, .95) 
    graphJSON_states2_deaths = create_chart(info.state_dates, info.state_deaths, burgundy, .95)
    
    return graphJSON_states2_cases, graphJSON_states2_deaths


#7
@app.route('/get_state', methods=['GET', 'POST'])
def get_state():
    global selected_state
    selected_state = request.form['state']
    graphJSON_states_cases, graphJSON_states_deaths = create_states2_chart()
    print("User selected state: ", selected_state)
    return render_template('select_state.html',  
                           selected_state = selected_state, 
                           graphJSON_states_cases = graphJSON_states_cases, 
                           graphJSON_states_deaths = graphJSON_states_deaths,
                           curr_date = curr_date,
                           state_increase_deaths = state_increase_deaths,
                           state_increase_cases = state_increase_cases,
                           logo = logo,
                           data_source = data_source
                           )



#3
def get_max_increase(category):
    global selected_state, selected_state2, selected_state3, max_3_cases, max_3_deaths, curr_date, df_states
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
    df_states = df.state[df.date==curr_date]
    selected_state = df.state[0]
    return df
    
max_cases = get_max_increase("cases")    
max_deaths = get_max_increase("deaths")    



#SKIP THIS ONE
@app.route('/get_states_chart/')  #this route is note being used but the function is
def create_states_chart(my_data=get_states_data(selected_state, starting_date)): 
    global graphJSON_states_cases, graphJSON_states_deaths
    
    trace_states_cases = go.Scatter (
        x = my_data.date,
        y = my_data.case_increase,
        marker_color = orange,
        opacity = .5
        )
    data = [trace_states_cases]
    graphJSON_states_cases = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder) 
    
    trace_states_deaths = go.Scatter (
        x = my_data.date,
        y = my_data.death_increase,
        marker_color = purple,
        opacity = .5
        )
    data = [trace_states_deaths]
    graphJSON_states_deaths = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder) 
 
    print("generating states chart")
    return render_template('index.html',  graphJSON_states_cases=graphJSON_states_cases, graphJSON_states_deaths=graphJSON_states_deaths)

#6
@app.route('/get_max/<category>')
def get_max(category):
    global data_cases, data_deaths, df_states, curr_date, max_cases, max_deaths, states
    data_cases=[]
    data_deaths=[]
    states = []
    
    df = get_max_increase(category)  #returns df database - used for sorting purposes
    max_cases = list(df['cases_increase'][df.date==curr_date])
    max_deaths = list(df['deaths_increase'][df.date==curr_date])
      
    for i in range(top):
        state = df_states[i]
        states.append(state)
        #print("state", state)
        graph_cases, graph_deaths = create_states2_chart(my_data=get_states_data(state, starting_date))
        data_cases.append(graph_cases)
        data_deaths.append(graph_deaths)
        
    return render_template('top_states2.html', 
                               states = states,
                               data_cases = data_cases,
                               data_deaths = data_deaths,
                               curr_date = curr_date,
                               max_cases = max_cases,
                               max_deaths = max_deaths,
                               max_3_cases = max_3_cases,
                               max_3_deaths = max_3_deaths)


# @app.route('/states_page')
# def states_page():
#     return render_template('select_state.html')    

 

# @app.route('/choose_top', methods=['GET', 'POST'])
# def choose_top():
#     print("testing choose top function")
#     return redirect('/')

#8
@app.route('/form/<category>', methods=['GET', 'POST'])
def form(category):
    global top, starting_date #fix starting_date later
    form = Top_States_Form()
    #form.amount.data = 3
    form.starting_date.data = datetime(2020, 3, 1).date()  #this doesn't update later. why?????
    if form.is_submitted():
        print("Form validated!")
        top = form.amount.data
        st_date = form.starting_date.data 
        starting_date = st_date #quick fix for now. fix this later
        print("Starting Date: ", st_date)
        get_max(category)
        return render_template('top_states2.html', 
                           states = states,
                           data_cases = data_cases,
                           data_deaths = data_deaths,
                           curr_date = curr_date,
                           max_cases = max_cases,
                           max_deaths = max_deaths,
                           category=category)
    else:
        flash('Invalid entry.', 'danger')
        return render_template('form.html', title='Select Top States', form=form, category=category)


@app.route('/choose_source', methods=['GET', 'POST'])
def choose_source():
    global data_source, info
    data_source = request.form['source']
    if data_source == 'Covid Tracking Project':
        info = DataSourceCTP()
    elif data_source == 'Our World in Data':
        info = DataSourceOWID()
    else:
        info = DataSourceNYT()
    print("Source: ", data_source)
    print("Request referrer", request.referrer)
    return redirect(request.referrer) #! this does not work when on select_state page. do more research

@app.route('/', methods=['GET', 'POST'])
def index():
    # global usa_total_cases, usa_total_deaths, data_source
    get_usa_data()
    return render_template('index.html', 
                           usa_total_deaths = usa_total_deaths,
                           usa_total_cases = usa_total_cases,
                           curr_date = curr_date,
                           data_source = data_source,
                           logo = logo
                           )

@app.route('/about.html')
def about():
    return render_template('about.html')  

if __name__ == '__main__':
  app.run(debug = False)