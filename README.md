# Covid19 Charts Web Application

This web application allows the user to view charts for daily cases and daily deaths in different states across the United States. User can choose to sort by cases, deaths or view a specific state. [Click here to run the application.](https://cs3140-covid-web-app.herokuapp.com/)

![Screenshot off app](https://raw.githubusercontent.com/rachelf21/3140_Covid_States_Web_App/master/static/img/screenshot.jpg)

## Getting Started

### Folder Structure

```
-root
    -static (required for Flask)
        -css
        -js
        -img
    -templates (required for Flask)
        -all html pages go here
    -venv
        -packages for virtual environment
    app.py (starting point)
    Procfile (required for Heroku)
    requirements.txt (required for Heroku)
```

### Prerequisites

```
Python version 3.6
Bootstrap version 4.5
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

## Deployment

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
- [Plotly](https://plotly.com/javascript/) - Used to generate charts
- [Heroku](https://devcenter.heroku.com/categories/reference) - Used to host the web application

## Author

- **Rachel Friedman** [View more of my work](https://github.com/rachelf21)

[//]: # "![W3Validdator badge](https://img.shields.io/w3c-validation/html?style=plastic&targetUrl=https%3A%2F%2Fvalidator.w3.org%2F"

![W3Validdator badge](https://heroku-badge.herokuapp.com/?app=cs3140-covid-web-app) ![Repo size](https://img.shields.io/github/repo-size/rachelf21/3140_Covid_States_Web_App?style=flat)
