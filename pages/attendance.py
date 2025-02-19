import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Register this page with a different path
dash.register_page(__name__, path="/attendance")

# Load the CSV file
df = pd.read_csv("data/CSVs/cleaned_hrh_timecard_data.csv")

# Ensure date and time columns are in the correct format
df["date"] = pd.to_datetime(df["date"])


# Define layout function
def layout():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H4(
                        "HRH - Attendance Overview",
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
                                            # Year dropdown filter
                                            dcc.Dropdown(
                                                id="year-dropdown",
                                                placeholder="Select Year",
                                                options=[
                                                    {
                                                        "label": year,
                                                        "value": year,
                                                    }
                                                    for year in df[
                                                        "date"
                                                    ].dt.year.unique()
                                                ],
                                                clearable=False,
                                            ),
                                        ],
                                        width=2,
                                    ),
                                    dbc.Col(
                                        [
                                            # Date range picker
                                            dcc.DatePickerRange(
                                                id="date-range",
                                                min_date_allowed=df["date"].min(),
                                                max_date_allowed=df["date"].max(),
                                                start_date=df["date"].min(),
                                                end_date=df["date"].max(),
                                            ),
                                        ],
                                        width=5,
                                    ),
                                    dbc.Col(
                                        width=1,
                                    ),
                                ],
                                className="mb-4",
                            ),
                            # 1 - charts
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    # Time series plot
                                                    dcc.Graph(id="time-series"),
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
                            # 2 - charts
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    # Heatmap plot
                                                    dcc.Graph(id="heatmap")
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
