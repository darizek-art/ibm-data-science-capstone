"""Interactive SpaceX launch dashboard for the IBM capstone project."""

from pathlib import Path
import re

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


DATA_PATH = Path(__file__).resolve().parents[1] / "05-eda-sql" / "Spacex.csv"


def _booster_category(version: str) -> str:
    """Collapse detailed booster names into the categories used in the lab."""
    match = re.search(r"(v1\.0|v1\.1|FT|B4|B5)", str(version))
    return match.group(1) if match else "Other"


def load_launch_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the existing project data and create dashboard-friendly fields."""
    data = pd.read_csv(path).rename(
        columns={
            "Launch_Site": "Launch Site",
            "PAYLOAD_MASS__KG_": "Payload Mass (kg)",
            "Booster_Version": "Booster Version",
            "Mission_Outcome": "Mission Outcome",
        }
    )
    data["Launch Site"] = data["Launch Site"].replace(
        {
            "CCAFS LC-40": "CCAFS SLC 40",
            "CCAFS SLC-40": "CCAFS SLC 40",
            "VAFB SLC-4E": "VAFB SLC 4E",
        }
    )
    data["Payload Mass (kg)"] = pd.to_numeric(
        data["Payload Mass (kg)"], errors="coerce"
    ).fillna(0)
    data["class"] = (data["Mission Outcome"] == "Success").astype(int)
    data["Booster Version Category"] = data["Booster Version"].map(
        _booster_category
    )
    return data


spacex_df = load_launch_data()
launch_sites = sorted(spacex_df["Launch Site"].dropna().unique())
min_payload = int(spacex_df["Payload Mass (kg)"].min())
max_payload = int(spacex_df["Payload Mass (kg)"].max())

app = Dash(__name__)
app.title = "SpaceX Launch Records Dashboard"

app.layout = html.Div(
    [
        html.H1("SpaceX Launch Records Dashboard", className="dashboard-title"),
        dcc.Dropdown(
            id="site-dropdown",
            options=[{"label": "All Sites", "value": "ALL"}]
            + [{"label": site, "value": site} for site in launch_sites],
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True,
            clearable=False,
        ),
        html.Label("Payload range (kg)", className="control-label"),
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=max(10000, max_payload),
            step=1000,
            value=[min_payload, max_payload],
            marks={0: "0", 2500: "2,500", 5000: "5,000", 7500: "7,500", 10000: "10,000"},
        ),
        dcc.Graph(id="success-pie-chart"),
        dcc.Graph(id="success-payload-scatter-chart"),
    ],
    className="dashboard-container",
)


@app.callback(Output("success-pie-chart", "figure"), Input("site-dropdown", "value"))
def update_pie_chart(entered_site: str):
    filtered = spacex_df if entered_site == "ALL" else spacex_df[spacex_df["Launch Site"] == entered_site]
    if entered_site == "ALL":
        counts = filtered.groupby("Launch Site", as_index=False)["class"].sum()
        title, names, values = "Total Successful Launches by Site", "Launch Site", "class"
    else:
        counts = filtered["class"].value_counts().rename_axis("Outcome").reset_index(name="Count")
        counts["Outcome"] = counts["Outcome"].map({0: "Failed", 1: "Successful"})
        title, names, values = f"Launch Outcomes for {entered_site}", "Outcome", "Count"
    return px.pie(counts, values=values, names=names, title=title)


@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [Input("site-dropdown", "value"), Input("payload-slider", "value")],
)
def update_scatter_chart(entered_site: str, payload_range: list[int]):
    filtered = spacex_df[spacex_df["Payload Mass (kg)"].between(*payload_range)]
    if entered_site != "ALL":
        filtered = filtered[filtered["Launch Site"] == entered_site]
    title_site = "All Sites" if entered_site == "ALL" else entered_site
    return px.scatter(
        filtered,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        hover_data=["Launch Site", "Booster Version", "Mission Outcome"],
        title=f"Payload Mass vs. Launch Success — {title_site}",
        labels={"class": "Launch success (1 = yes, 0 = no)"},
    )


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8050)
