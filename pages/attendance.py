import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Register this page with a different path
dash.register_page(__name__, path="/attendance")

# Load CSV files into DataFrames
# Load the CSV file
df = pd.read_csv("data/CSVs/cleaned_hrh_timecard_data.csv")

# Ensure date and time columns are in the correct format
df["date"] = pd.to_datetime(df["date"])
df["clockin_time"] = pd.to_datetime(df["clockin_time"], format="%H:%M:%S").dt.time

# Extract hour from clockin_time
df["clockin_hour"] = pd.to_datetime(df["clockin_time"], format="%H:%M:%S").dt.hour

# Extract day of the week from the date
df["weekday"] = df["date"].dt.day_name()

# Now aggregate data for the time series plot and heatmap
# Time series: Count of employees per date
time_series_data = (
    df.groupby("date")["employee_id"].nunique().reset_index(name="employee_count")
)

# Heatmap: Count employees for each hour of the day and weekday
heatmap_data = (
    df.groupby(["clockin_hour", "weekday"])["employee_id"].nunique().reset_index()
)
heatmap_data_pivot = heatmap_data.pivot(
    index="clockin_hour", columns="weekday", values="employee_id"
)

# Sorting weekdays in order
weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
heatmap_data_pivot = heatmap_data_pivot[weekday_order]


# Define layout function
def layout():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H4(
                        "Human Resources - Overview",
                        className="text-left my-4",
                    )
                )
            ),
            dbc.Row(
                [
                    # Column for main charts
                    dbc.Col(
                        [
                            # Dropdown for state, LGA, ward, and facility filters
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            # Filter inputs
                                            html.Div(
                                                [
                                                    html.Label("Select Year:"),
                                                    dcc.Dropdown(
                                                        id="year-dropdown",
                                                        options=[
                                                            {
                                                                "label": year,
                                                                "value": year,
                                                            }
                                                            for year in sorted(
                                                                df[
                                                                    "date"
                                                                ].dt.year.unique()
                                                            )
                                                        ],
                                                        value=df[
                                                            "date"
                                                        ].dt.year.max(),  # Default to the latest year
                                                        clearable=False,
                                                    ),
                                                    html.Label("Select Month:"),
                                                    dcc.Dropdown(
                                                        id="month-dropdown",
                                                        options=[
                                                            {
                                                                "label": month,
                                                                "value": month,
                                                            }
                                                            for month in range(1, 13)
                                                        ],
                                                        value=df[
                                                            "date"
                                                        ].dt.month.max(),  # Default to the latest month
                                                        clearable=False,
                                                    ),
                                                    html.Label(
                                                        "Number of Past Months:"
                                                    ),
                                                    dcc.Slider(
                                                        id="past-months-slider",
                                                        min=1,
                                                        max=12,  # Up to 12 months (1 year)
                                                        marks={
                                                            i: str(i)
                                                            for i in range(1, 13)
                                                        },
                                                        value=1,  # Default to past 1 month
                                                        step=1,
                                                    ),
                                                ],
                                                style={
                                                    "width": "30%",
                                                    "display": "inline-block",
                                                    "vertical-align": "top",
                                                },
                                            ),
                                        ],
                                        width=2,
                                    ),
                                ],
                                className="mb-4",
                            ),
                            # 1 - charts
                            dbc.Row(
                                [
                                    # employee-counts-by-qualification
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id="employee-counts-by-qualification"
                                                    )
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "20px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ],
                                        width=6,
                                    ),
                                    # employee-distribution-by-age
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id="employee-distribution-by-age"
                                                    ),
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "20px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ],
                                        width=6,
                                    ),
                                ],
                                className="my-4",
                            ),
                            # 2 - charts
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    # dcc.Graph(
                                                    #     id="percentage-distribution-by-cadre"
                                                    # ),
                                                    dcc.Graph(
                                                        id="percentage-distribution-by-cadre_treemap"
                                                    )
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "20px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ],
                                        width=12,
                                    ),
                                ]
                            ),
                            # 3 - charts
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    # dcc.Graph(
                                                    #     id="employee-percentage-by-employment-type"
                                                    # ),
                                                    dcc.Graph(
                                                        id="employee-percentage-by-employment-type_sb"
                                                    ),
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "20px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                    # "height": "150px",  # Reduce the overall height of the container
                                                },
                                            ),
                                        ],
                                        width=12,
                                    ),
                                ],
                                className="my-4",
                            ),
                        ],
                        width=12,
                    ),
                ]
            ),
        ],
        fluid=True,
    )
