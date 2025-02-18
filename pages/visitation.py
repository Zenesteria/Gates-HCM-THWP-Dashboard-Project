import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


# Register this page in Dash's page registry
dash.register_page(__name__, path="/visitation")

# Load CSV files into DataFrames
patients_df = pd.read_csv("data/CSVs/cleaned_patients_data.csv")
facilities_df = pd.read_csv("data/CSVs/facilities.csv")
wards_df = pd.read_csv("data/CSVs/wards.csv")
lgas_df = pd.read_csv("data/CSVs/lgas.csv")
states_df = pd.read_csv("data/CSVs/states.csv")

# Merge datasets to create necessary relationships
wards_lgas_df = pd.merge(wards_df, lgas_df, left_on="lga_id", right_on="id")
facilities_wards_df = pd.merge(
    facilities_df, wards_df, left_on="ward_id", right_on="id"
)
patients_wards_df = pd.merge(
    patients_df, wards_df, left_on="ward_name", right_on="name"
)
patients_wards_lgas_df = pd.merge(
    patients_wards_df, lgas_df, left_on="lga_id", right_on="id"
)
visitation_df = pd.read_csv("data/CSVs/cleaned_visitations_data.csv")
# Merge without repeating similar columns
patients_visitation_df = pd.merge(
    patients_df.drop(columns=["state_name", "lga_name", "ward_name"]),
    visitation_df.drop(columns=["patient_project_number", "facility_name"]),
    on="patient_id",
    how="inner",
)


# Convert start_date column to datetime format
patients_visitation_df["start_date"] = pd.to_datetime(
    patients_visitation_df["start_date"]
)

# Extract day, month, and year into separate columns
patients_visitation_df["start_day"] = patients_visitation_df["start_date"].dt.day
patients_visitation_df["start_month"] = patients_visitation_df["start_date"].dt.month
patients_visitation_df["start_year"] = patients_visitation_df["start_date"].dt.year

# Extract week number and day of the week
patients_visitation_df["week_number"] = (
    patients_visitation_df["start_date"].dt.isocalendar().week
)
patients_visitation_df["day_of_week"] = patients_visitation_df[
    "start_date"
].dt.day_name()


# Define layout function
def layout():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H4(
                        "Visitation Trends and Planning",
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
                                        dcc.Dropdown(
                                            id="vs-state-filter",
                                            options=[
                                                {"label": state, "value": state}
                                                for state in states_df[
                                                    "state_name"
                                                ].unique()
                                            ],
                                            placeholder="Select State",
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="vs-lga-filter", placeholder="Select LGA"
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="vs-ward-filter",
                                            placeholder="Select Ward",
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="vs-facility-filter",
                                            placeholder="Select Facility",
                                            multi=True,
                                            style={"width": "100%"},
                                        ),
                                        width=3,
                                    ),
                                    dbc.Col(
                                        dcc.DatePickerRange(
                                            id="date-picker",
                                            start_date=patients_visitation_df[
                                                "start_date"
                                            ].min(),
                                            end_date=patients_visitation_df[
                                                "start_date"
                                            ].max(),
                                            display_format="YYYY-MM-DD",
                                        ),
                                        width=3,
                                    ),
                                ],
                                className="mb-4",
                            ),
                            # 1- charts
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id="gender-pie-chart"
                                                    ),  # Disable mode bar controls
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "20px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ],
                                        width=4,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id="visitation-by-age-group-bar-chart"
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
                                        width=4,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id="marital-status-bar-chart"
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
                                        width=4,
                                    ),
                                ],
                                className="my-4",
                            ),
                            # 2 - heatmap
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id="hourly-traffic-heatmap"
                                                    ),
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "20px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ]
                                    )
                                ],
                                className="my-4",
                            ),
                            # 3 - time series
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(id="visitation-chart"),
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "20px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ]
                                    )
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
