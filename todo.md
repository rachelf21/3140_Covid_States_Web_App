## TODO

- [x] create virtual environment
- [x] set up flask structure
- [x] download bootstrap
- [x] install python packages
- [x] create readme file
- [x] create color scheme
- [x] get state silhouettes or flags
- [x] create shortcut icon ico file
- [x] change abbreviation to full name for state flag images and state name
- [x] fix redirect on select data source for cases/deaths/select pages
- [x] data source in footer link to original data source
- [x] fit data source in footer to fit in main window
- [x] format total_cases with commas (nyt and ctp)
- [x] add timers to functions
- [ ] display total cases and total deaths as of today
- [x] add form validation not to allow more than 50 states
- [ ] give user the option to change starting date for graph
- [x] disable date button temporarily
- [ ] give user the option to select specific date (ending date)
- [x] highlight button of feature currently displayed
- [x] display notification when data source is switched
- [ ] when switching data source on select_state page, how to redirect to same page and keep selected_state value??
- [x] display datatable for USA
- [ ] display datatable for states
- [x] change cases/deaths charts to deaths/cases charts when "view by new deaths" is selected
- [?] color code charts according to data source
- [ ] add Johns Hopkins as source (each day new csv file)
- [x] remove print and debug statements in app .py
- [ ] .gitignore practice files and other system folders. How to remove them only from github after ignoring?
- [ ] streamline some features, make code run more efficiently - why is ctp so slow to load?
- [ ] reformat data table. Color code cases/deaths. Adjust pagination buttton color. Why won't it center properly?
- [ ] work on a different color scheme. Blues and greens?

### PYTHON FUNCTIONS

- [x] create DataSource class (to access API endpoints):
  - [x] determine necessary attributes and how to set
  - [x] initialize DataSource class with name, id, API endpoints, image logo, latest date
  - [x] create python functions to retrieve usa data (2 ways: json and csv) and set attributes
  - [x] create python functions to retrieve states data (2 ways: json and csv) and set attributes
  - [x] create python functions to parse usa data (2 ways: json and csv) and set attributes
  - [x] create python functions to parse states data (2 ways: json and csv) and set attributes
- [x] app . py (main app, create DataSource objects to access data attributes)
  - [x] create python function for creating JSON chart objects for usa data deaths
  - [x] create python function for creating JSON chart objects for usa data cases
  - [x] create python function for creating JSON chart objects for states data cases
  - [x] create python function for creating JSON chart objects for states data deaths
  - [x] create python function for setting appropriate data source, per user choice
  - [x] create flask routes for rendering html page with usa cases and deaths
  - [x] create flask routes for rendering html page with usa overview
  - [x] create flask routes for rendering html page with top states for cases and deaths
  - [x] create flask routes for rendering html page with user_selected state
- [x] create python function for extracting latest data for states
- [x] create python function for sorting states data by max cases and max deaths
- [x] create python function for states and abbrev, both ways
- _see function workflow for more functions and detail_

### HTML PAGES

- [x] create base.html (navigation bar, buttons. data source)
- [x] create index.html (retrieve usa numbers from python)
- [x] create usa.html
- [x] create form.html (integrate with wtform)
- [x] create top_states.html for cases/deaths
- [x] create choose_state.html for cases/deaths
- [x] create data_tables.html for cases/deaths (usa)
- [ ] create data_tables.html for cases/deaths (states)
- [x] create about.html
