# Cityplanner_Tool

Examination project for data engineering program from brightstraining.
Steps to use dash app - run files in this order:

1. Run in terminal:

   - `python -m venv cpt-venv`
   - `cpt-venv\Scripts\activate`
   - `pip install -r requirements.txt (in venv terminal)`

2. Run files (in order):
   - transform_finland-data
   - transform_sweden_data
     - get_prediction
     - load_data (create config.ini first)
       - app1.py

## TODO:

- [ ] Slider year should be displayed in graph title
- [ ] Include current tree carbon storage as stacks in recommendation bar graph. Possible [data source](https://www.globalforestwatch.org/dashboards/country/SWE/1/?category=climate&map=eyJjYW5Cb3VuZCI6dHJ1ZX0%3D)
- [ ] Checkbox for tree types ()
- [ ] Improve styling
  - [ ] Implement dash bootstrap components (dbc)
  - [ ] move styling to external stylesheet
