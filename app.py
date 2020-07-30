from flask import Flask, render_template, url_for, jsonify, request
import json
import numpy as np
import pandas as pd
from datetime import datetime
import plotly 
import plotly.graph_objs as go

graphJSON_usa_cases="[]"

def get_usa_data():
    usa_data = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv", error_bad_lines=False)
    usa_data['date'] = pd.to_datetime(usa_data['date'], format="%Y-%m-%d" )
    usa_data['date'] = usa_data['date'].dt.date
    usa_data['case_increase']=(usa_data.cases - usa_data.cases.shift(1))
    usa_data['death_increase']=(usa_data.deaths - usa_data.deaths.shift(1))
    print("retrieving USA data")
    return usa_data

app = Flask(__name__)

@app.route('/get_usa_chart/')
def create_chart(my_data=get_usa_data()): 
    global graphJSON_usa_cases
    trace_usa_cases = go.Scatter (
        x = my_data.date,
        y = my_data.case_increase
        )
    data = [trace_usa_cases]
    graphJSON_usa_cases = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)      
    print("returning usa chart")
    return render_template('index.html',  graphJSON_usa_cases=graphJSON_usa_cases)

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