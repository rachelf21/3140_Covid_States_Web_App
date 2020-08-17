# Covid19 Web Application

This web application allows the user to view charts for daily cases and daily deaths in different states across the United States. User can choose to sort by cases, deaths or view a specific state. [Click here to run the application.](https://cs3140-covid-web-app.herokuapp.com/)

![Screenshot off app](https://raw.githubusercontent.com/rachelf21/3140_Covid_States_Web_App/master/static/img/screenshot.jpg)

## Features

- View an overview of total cases and deaths in the United States.
- View graphs of new cases and new deaths in the United States.
- View data table of new cases, total cases, new deaths, total deaths in the United States.
- View graphs of top \_\_\_ states _(user can select how many)_ with the most new cases today.
- View graphs of top \_\_\_ states _(user can select how many)_ with the most new deaths today.
- View graphs of new cases and new deaths for selected state.
- User can select from two different sources. (I would like to add more.)

## Data Sources

The user can choose which data source this web application should use when displaying the graphs. The following API endpoints are used in this application. Click on the links below for more details on their API.

- [New York Times Covid-19 Data](https://developer.nytimes.com/covid)
- [The Covid Tracking Project](https://covidtracking.com/data/api)

## How the data is retrieved

I created a class in Python called DataSource, and two classes (one for each data source) which inherit from DataSource. These classes uses the Python `requests` package to retrieve data from the API endpoints. The following attributes are set for this class:

```
data_source_name  (String)
data_source_id (int)
logo (string)
latest_date (date)
link (string - link to their website)
url_usa (String - API endpoint for USA data)
usa_data (String - json object returned, contains all usa data - parse this to set all other usa data)
usa_total_cases(int)
usa_total_deaths (int)
usa_increase_cases(int)
usa_increase_deaths (int)
usa_cases  (list)
usa_deaths (list)
usa_dates (list)
url_state (String - API endpoint for states data)
state_data (String - json object returned, contains all states data - parse this to set all other states data)
state_total_cases(int)
state_total_deaths (int)
state_increase_cases(int)
state_increase_deaths (int)
state_cases  (list)
state_deaths (list)
state_dates (list)
states_current (list of all states with values for today only)
```

The Data Source class has the following functions:

```
- retrieve_data_usa (Connects to the API endpoint. Retrieves USA data. Sets all USA attributes above. Does not return anything.)
- retrieve_data_state (Connects to the API endpoint. Retrieves historic states data. Sets all attributes of state listed above. Does not return anything.)
- retrieve_current_states (Connects to the API endpoint. Retrieves a list of values for today - used to determine which states to list, based on max values for states. Sets a list of dictionaries - one entry per state of today’s data. Does not return anything.)
- get_max_cases (returns a list of states, cases, and deaths sorted in desc order by max cases for latest date)
- get_max_deaths  (returns a list of states, deaths, cases, sorted in desc order by max deaths for latest date)
```

When an object of the class is created, it makes a usa or state call (depending on where it's called) to the relevant API endpoint. It then parses that data, and assigns values to the relevant attributes of that object. The main application then uses those values to create the JSON lists necessary to build the charts, passes the JSON objects to `plotly` to create the charts, which then passes it on to javascript to display it to the user.

## Getting Started

### Folder Structure

```
-root
    -static (required for Flask)
        -css
            -bootstrap css files
        -js
        -img
            -flags
            -logos
    -templates (required for Flask)
        -all html pages go here
    -venv
        -packages for virtual environment
    app.py (starting point)
    DataSource.py (class used to retrieve API data)
    ... other python files
    Procfile (required for Heroku)
    requirements.txt (required for Heroku and Travis CI)
    .travis.yml (required for Travis CI)
```

### Prerequisites

```
Python version 3.6
Bootstrap version 4.5
Bootstrap DataTable
popper.js
jQuery
d3.js
plotly.js
Heroku CLI
Python packages detailed in requirements.txt
```

## Installing

- Download and install [Python 3.6.](https://www.python.org/downloads/)

- Download and install [Bootstrap 4.5](https://getbootstrap.com/docs/4.5/getting-started/download/)

- Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

- Create a virtual environment. Note that the venv folder is in the root folder of the project.

```
    python3 -m venv /path/to/venv
```

- Run the following command to install required Python packages.

```
    pip install -r requirements.txt
```

## Deployment on Heroku

Create a Procfile in your root directory and add the following line of code.
(Note that this has already been done, but I am including it here for the sake of completion.)

```
web: gunicorn app:app
```

Create a new directory for this project, navigate to that directory, then initialize it as a git repository by typing:

```
$ git init
```

Clone [this repository](https://github.com/rachelf21/3140_Covid_States_Web_App.git) to this repository you just created.

```
$ git clone https://github.com/rachelf21/3140_Covid_States_Web_App.git
```

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

```
$ heroku login
```

Follow these step-by-step instructions: [Deploying with Git](https://devcenter.heroku.com/articles/git) to create a new web app on Heroku and link this repo with the Heroko project.

Make some changes to the code you just cloned and deploy them to Heroku using Git.

```
$ git add.
$ git commit -m "describe changes made"
$ git push heroku master
```

Your app should now run on the Heroku server.

## Built With

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
- [Bootstrap](https://getbootstrap.com/docs/4.5/getting-started/introduction/) - Used to style website
- [DataTables](https://datatables.net/) - used to build data tables for USA data
- [Plotly](https://plotly.com/javascript/) - Used to generate charts
- [Heroku](https://devcenter.heroku.com/categories/reference) - Used to host the web application

## About this project

- Created by **Rachel Friedman** [View more of my work](https://github.com/rachelf21)
- For Brooklyn College, CISC 3140, Professor Katherine Chuang
- August 2020

![W3Validdator badge](https://img.shields.io/w3c-validation/html?style=flat&targetUrl=https%3A%2F%2Fvalidator.w3.org%2F)
![W3Validdator badge](https://heroku-badge.herokuapp.com/?app=cs3140-covid-web-app)
![Travis badge](https://img.shields.io/travis/rachelf21/3140_Covid_States_Web_App)
![Repo size](https://img.shields.io/github/repo-size/rachelf21/3140_Covid_States_Web_App?style=flat)
