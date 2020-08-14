## TODO

- [x] create virtual environment
- [x] set up flask structure
- [x] download bootstrap
- [x] install python packages
- [x] create readme file
- [x] create color scheme
- [x] get state silhouettes or flags
- [x] create shortcut icon ico file

_There were many other items, but I used a different workflow and did not keep this todo list current._

_But from this point on, I'm updating it continuously._

- [x] change abbreviation to full name for state flag images and state name
- [x] fix redirect on select data source for cases/deaths/select pages
- [ ] data source in footer link to original data source
- [x] fit data source in footer to fit in main window - adjust elements above
- [ ] format total_cases with commas (nyt and ctp)
- [ ] display total cases and total deaths as of today
- [ ] add form validation not to allow more than 50 states
- [ ] give user the option to change starting date for graph
- [ ] give user the option to select specific date (ending date)
- [ ] display datatable (view data button under graph)
- [ ] change cases/deaths charts to deaths/cases charts when "view by new deaths" is selected
- [ ] color code charts according to data source
- [ ] add Johns Hopkins as source (each day new csv file)
- [ ] revove print and debug statements in app.py
- [ ] streamline some features, make code run more efficiently. Don't have to download the data more than once per session.

### PYTHON FUNCTIONS

- [x] create python function for retrieving usa data
- [x] create python function for creating JSON chart objects for usa data deaths
- [x] create python function to extract latest data for usa
- [x] create python function for retrieving states data
- [x] create python function for sorting states data by max cases and max deaths
- [x] create python function for creating JSON chart objects for states data cases
- [x] create python function for creating JSON chart objects for states data deaths
- [x] create python function for extracting latest data for states
- _see function workflow for more functions and detail_

### HTML PAGES

- [x] create base.html (navigation bar, buttons)
- [x] create index.html (retrieve usa numbers from python)
- [x] create usa.html
- [x] create form.html (integrate with wtform)
- [x] create top_states.html for cases/deaths
- [x] create choose_state.html for cases/deaths
- [x] create about.html
