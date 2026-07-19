# Plotly Dash dashboard

This lab implements the IBM SpaceX launch dashboard tasks using the existing
project dataset at `05-eda-sql/Spacex.csv`.

## Run locally

```powershell
python -m pip install pandas dash plotly
python spacex_dash_app.py
```

Then open <http://127.0.0.1:8050>.

The dashboard includes a launch-site dropdown, a success pie chart, a payload
range slider, and a payload-versus-success scatter plot coloured by booster
version category.
