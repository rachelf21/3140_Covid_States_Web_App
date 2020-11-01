from flask import Flask, render_template, url_for, jsonify, request, redirect, flash
import timeit
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import plotly 
import plotly.graph_objs as go
from forms import Top_States_Form
from data_sources import DataSourceCTP, DataSourceNYT, DataSourceOWID
from state_abbrev import State_Abbrev

testdates = []
info = DataSourceNYT()
data_source = info.data_source_name
logo = info.logo
curr_date = info.latest_date
link = ''
button = 4

##GLOBAL USA VARIABLES
usa_total_cases = 0
usa_total_deaths = 0
usa_increase_deaths = 0
usa_increase_cases = 0

##GLOBAL STATE VARIABLES
state_total_cases = 0
states_total_cases = []
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
df_states = [] #replaced with states_current
data_cases = []
data_deaths = []
top = 3
x= 0 # temp fix. use for position of starting date in array, instead of rewriting all functions with starting date

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


#1  
def get_usa_data():
    global data_source, usa_increase_cases, usa_increase_deaths, usa_total_cases, usa_total_deaths, curr_date, logo, info, button
            
    button = 0
    info.retrieve_data_usa()
    data_source = info.data_source_name
    usa_increase_cases = info.usa_increase_cases
    usa_increase_deaths = info.usa_increase_deaths
    usa_total_cases = info.usa_total_cases
    usa_total_deaths = info.usa_total_deaths
    curr_date = info.latest_date
    logo = info.logo
    return info

#5 
@app.route('/get_usa_chart/')
def create_usa_chart():
    global graphJSON_usa_cases, graphJSON_usa_deaths, usa_increase_deaths, usa_increase_cases, button

    info = get_usa_data()
    data_source = info.data_source_name
    
    graphJSON_usa_cases = create_chart(info.usa_dates, info.usa_cases, orange, .95)
    graphJSON_usa_deaths = create_chart(info.usa_dates, info.usa_deaths, burgundy, .95)
 
    return render_template('usa.html', 
                           button = button,
                           graphJSON_usa_cases=graphJSON_usa_cases, 
                           graphJSON_usa_deaths=graphJSON_usa_deaths,
                           usa_increase_deaths = usa_increase_deaths,
                           usa_increase_cases = usa_increase_cases,
                           curr_date = curr_date,
                           data_source = data_source,
                           logo = logo,
                           link = info.link)

def create_chart(dates, values, my_color, my_opacity ):
    trace_data = go.Bar(
        x = dates,
        y = values,
        marker_color = my_color,
        opacity = my_opacity)
    data = [trace_data]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

#2 
def get_states_data(state, starting_date):
    global data_source, curr_date, logo, state_increase_cases, state_increase_deaths, info, state_total_cases,state_total_deaths, x
    
    #x= np.where(info.state_dates == starting_date)
    
    if info.data_source_id == 2 and len(selected_state)>3:
        state = State_Abbrev().get_abbrev(state)
    # elif info.data_source_id == 3:
    #     info = DataSourceNYT() #no states data from OWID

    info.retrieve_data_state(state)
    
    formatted_date = starting_date.strftime('%Y-%m-%d')
    new_date = datetime.strptime(formatted_date, '%Y-%m-%d').date()
    i=0
    for d in info.state_dates:
        i=i+1
        if new_date == d:
            x = i

    # try:
    #     x = info.state_dates.index(new_date)  # preferred way to find position of date, but this does not work
    # except:
    #     x = 0
    
    state_total_cases = info.state_total_cases
    state_total_deaths = info.state_total_deaths
    state_increase_cases = info.state_increase_cases
    state_increase_deaths = info.state_increase_deaths
    curr_date = info.latest_date
    logo = info.logo
    return info
    
#4
def create_states2_chart(): 
    global graphJSON_states2_cases, graphJSON_states2_deaths, info, selected_state, x
    info = get_states_data(selected_state, starting_date)   
    info.state_dates = info.state_dates[x:]
    info.state_cases = info.state_cases[x:]
    info.state_deaths = info.state_deaths[x:]
    graphJSON_states2_cases = create_chart(info.state_dates, info.state_cases, orange, .95) 
    graphJSON_states2_deaths = create_chart(info.state_dates, info.state_deaths, burgundy, .95)
    
    return graphJSON_states2_cases, graphJSON_states2_deaths

#7
@app.route('/get_state', methods=['GET', 'POST'])
def get_state():
    global selected_state, button
    button = 3
    selected_state = request.form['state']
    graphJSON_states_cases, graphJSON_states_deaths = create_states2_chart()
    return render_template('select_state.html', 
                           button = button,
                           selected_state = selected_state, 
                           graphJSON_states_cases = graphJSON_states_cases, 
                           graphJSON_states_deaths = graphJSON_states_deaths,
                           curr_date = curr_date,
                           state_increase_deaths = state_increase_deaths,
                           state_increase_cases = state_increase_cases,
                           logo = logo,
                           link = info.link,
                           data_source = data_source
                           )

@app.route('/get_max/<category>')
def get_max(category):
    global data_cases, data_deaths, df_states, curr_date, max_cases, max_deaths, states, selected_state,top,button, states_total_cases, info, starting_date
    states_total_cases = []
    data_cases=[]
    data_deaths=[]
    states = []    
    info.retrieve_current_states()

    if category == 'cases':
        button = 1
        states, max_cases, max_deaths = info.get_max_cases()
    else:
        button = 2 
        states, max_deaths, max_cases = info.get_max_deaths()
    
    start = timeit.default_timer()   
    for i in range(top):
        selected_state = states[i]
        #states.append(state)
        states_total_cases.append(info.state_total_cases)
        # print(selected_state, "cases", info.state_total_cases)  #troubleshooting cases figure
        graph_cases, graph_deaths = create_states2_chart()
        data_cases.append(graph_cases)
        data_deaths.append(graph_deaths)
        
    stop = timeit.default_timer()
    print('Retrieving each individual state data from', data_source, '{:.2f}'.format(stop-start))
    
    if info.data_source_id == 2:
        for index, st in enumerate(states):
            states[index] = State_Abbrev().get_full_name(st)
            
    return render_template('top_states2.html', 
                               button = button,
                               states = states,
                               data_cases = data_cases,
                               data_deaths = data_deaths,
                               states_total_cases = states_total_cases,
                               curr_date = curr_date,
                               logo = logo,
                               link = info.link)

#8
@app.route('/form/<category>', methods=['GET', 'POST'])
def form(category):
    global top, button, starting_date, data_cases, data_deaths, states_total_cases #fix starting_date later
    if category=="cases":
        button = 1
    else:
        button = 2
    form = Top_States_Form(request.form)
    #form.amount.data = 3
    if request.method=='GET':
        form.starting_date.data = datetime(2020, 9, 1).date()  #this doesn't update later. why?????
    
    elif request.method=='POST':
        if form.validate():
            top = form.amount.data
            st_date = form.starting_date.data 
            starting_date = st_date #quick fix for now. fix this later
            get_max(category)
            return render_template('top_states2.html', 
                               states = states,
                               button = button,
                               logo = logo,
                               link = info.link,
                               data_source = data_source,
                               data_cases = data_cases,
                               data_deaths = data_deaths,
                               curr_date = curr_date,
                               max_cases = max_cases,
                               max_deaths = max_deaths,
                               category=category,
                               states_total_cases = states_total_cases, 
                               )
        else:
            if (request.form.get('amount')) is not None:
                flash('Invalid Entry. Please enter a number from 1-50.', 'danger')
    return render_template('form.html', 
                                   title='Select Top States', 
                                   button = button,
                                   form=form, 
                                   category=category,
                                   logo = logo,
                                   data_source = data_source,
                                   curr_date = curr_date,
                                   link = info.link
                                   )


@app.route('/choose_source', methods=['GET', 'POST'])
def choose_source():
    global data_source, info, logo
    data_source = request.form['source']
    if data_source == 'Covid Tracking Project':
        flash('Data source set to ' + data_source + '.', 'info')
        info = DataSourceCTP()
    elif data_source == 'Our World in Data':
        info = DataSourceOWID()
    else:
        info = DataSourceNYT()
        flash('Data source set to ' + data_source + '.', 'success')
    logo = info.logo
    if request.referrer == "http://127.0.0.1:5000/get_state":
        return redirect(url_for("index"))
    return redirect(request.referrer) #! manual fix. this does not work when on select_state page. do more research


@app.route('/data_tables')
def data_tables():
    global testdates
    js_dates = []
    # info = get_usa_data()  #this is for testing only. delete this one we connect this with the right page and info is set
    usa_cases = list(info.usa_cases)
    usa_deaths = list(info.usa_deaths)
    usa_dates = list(info.usa_dates)
    usa_total_cases = list(info.usa_daily_total_cases)
    usa_total_deaths = list(info.usa_daily_total_deaths)
    
    for d in usa_dates:
        js_d = int(time.mktime(d.timetuple())) * 1000
        js_dates.append(js_d)
    testdates = js_dates

    print("Latest date", info.latest_date)
    return render_template('data_tables.html', 
                           button = button, 
                           curr_date = info.latest_date,
                           data_source = data_source,
                           data_source_id = info.data_source_id,
                           logo = info.logo, 
                           link = info.link,
                           usa_cases = usa_cases,
                           usa_deaths = usa_deaths,
                           usa_dates = js_dates,
                           usa_total_cases = usa_total_cases,
                           usa_total_deaths = usa_total_deaths
                           )
    
@app.route('/', methods=['GET', 'POST'])
def index():
    global button
    get_usa_data()
    button = 4
    return render_template('index.html',
                           button = button,
                           usa_total_deaths = usa_total_deaths,
                           usa_total_cases = usa_total_cases,
                           curr_date = curr_date,
                           data_source = data_source,
                           logo = logo,
                           link = info.link
                           )

@app.route('/about')
def about():
    global button
    return render_template('about.html', button = button, logo=logo, data_source = data_source, curr_date=curr_date)  

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down (for travis)'
    
if __name__ == '__main__':
  app.run(debug = False)