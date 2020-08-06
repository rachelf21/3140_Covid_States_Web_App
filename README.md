# Covid19 Charts Web Application

This web application allows the user to choose a data source, state, and dates and then generates charts for the data selected. [Click here to run the application.](https://cs3140-covid-web-app.herokuapp.com/)

![Screenshot off app](https://raw.githubusercontent.com/rachelf21/3140_Covid_States_Web_App/master/static/img/screenshot.jpg)

## Getting Started

### Folder Structure

```
-root
    -static
        -css
        -js
        -img
    -templates
        -all html pages go here
    -venv
        -packages for virtual environment
    app.py (starting point)
    Procfile (required for heroku)
    requirements.txt (generated by pip freeze)
```

### Prerequisites

```
Python 3.6
Bootstrap 4.5
popper.js
jQuery
d3.js
plotly.js
python packages detailed in requirements.txt

```

### Installing

Run the following command to install required Python packages.

```
pip install -r requirements.txt
```

## Deployment

Create a Procfile and add the following line of code:

```
web: gunicorn app:app
```

Use git to deploy to Heroko. Follow the steps below, or for a more detailed step-by-step explannation, read [Deploying with Git](https://devcenter.heroku.com/articles/git).

```
git remote add herokoaddress - look up this command
git add .
git commit
git push heroku master
```

Your app should now run on the Heroku server.

## Built With

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
- [Bootstrap](https://getbootstrap.com/docs/4.5/getting-started/introduction/) - Used to style website
- [Plotly](https://plotly.com/javascript/) - Used to generate charts
- [Heroku](https://devcenter.heroku.com/categories/reference) - Used to host the web application

## Author

- **Rachel Friedman** [View more of my work](https://github.com/rachelf21)
