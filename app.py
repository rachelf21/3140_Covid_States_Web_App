from flask import Flask, render_template, url_for, jsonify, request
import json
import numpy as np
import pandas as pd
from datetime import datetime
import plotly 
import plotly.graph_objs as go

selected_state = "California"
graphJSON_usa_cases="[]"
graphJSON_usa_deaths="[]"
graphJSON_states_cases="[]"
graphJSON_states_deaths="[]"


def get_usa_data():
    usa_data = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv", error_bad_lines=False)
    usa_data['date'] = pd.to_datetime(usa_data['date'], format="%Y-%m-%d" )
    usa_data['date'] = usa_data['date'].dt.date
    usa_data['case_increase']=(usa_data.cases - usa_data.cases.shift(1))
    usa_data['death_increase']=(usa_data.deaths - usa_data.deaths.shift(1))
    print("retrieving USA data")
    return usa_data


def get_states_data():
    states_data = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv", error_bad_lines=False)
    states_data['date'] = pd.to_datetime(states_data['date'], format="%Y-%m-%d" )
    states_data['date'] = states_data['date'].dt.date
    st = selected_state
    states_data = states_data[states_data.state==st]
    states_data['case_increase']=(states_data.cases - states_data.cases.shift(1))
    states_data['death_increase']=(states_data.deaths - states_data.deaths.shift(1))
    print("retrieving states data")
    return states_data

stdata=get_states_data()


app = Flask(__name__)


@app.route('/get_usa_chart/')
def create_usa_chart(my_data=get_usa_data()): 
    global graphJSON_usa_cases, graphJSON_usa_deaths
    
    trace_usa_cases = go.Bar (
        x = my_data.date,
        y = my_data.case_increase
        )
    data = [trace_usa_cases]
    
    graphJSON_usa_cases = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder) 
    
    trace_usa_deaths = go.Bar (
        x = my_data.date,
        y = my_data.death_increase
        )
    data = [trace_usa_deaths]
    graphJSON_usa_deaths = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder) 
     
    print("generating usa chart")
    return render_template('index.html',  graphJSON_states_cases=graphJSON_states_cases, graphJSON_states_deaths=graphJSON_states_deaths, graphJSON_usa_cases=graphJSON_usa_cases, graphJSON_usa_deaths=graphJSON_usa_deaths)


@app.route('/get_states_chart/')
def create_states_chart(my_data=get_states_data()): 
    global graphJSON_states_cases, graphJSON_states_deaths
    
    trace_states_cases = go.Bar (
        x = my_data.date,
        y = my_data.case_increase
        )
    data = [trace_states_cases]
    
    graphJSON_states_cases = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder) 
    
    trace_states_deaths = go.Bar (
        x = my_data.date,
        y = my_data.death_increase
        )
    data = [trace_states_deaths]
    graphJSON_states_deaths = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder) 
     
    print("generating states chart")
    return render_template('index.html',  graphJSON_states_cases=graphJSON_states_cases, graphJSON_states_deaths=graphJSON_states_deaths, graphJSON_usa_cases=graphJSON_usa_cases, graphJSON_usa_deaths=graphJSON_usa_deaths)



@app.route('/SomeFunction')
def SomeFunction():
    print('In SomeFunction')
    return "Nothing"

@app.route('/')
def index():
    global graphJSON_usa_cases
    graphJSON_usa_cases="[]"
    return render_template('index.html', graphJSON_usa_cases=graphJSON_usa_cases)


if __name__ == '__main__':
  app.run(debug=False)