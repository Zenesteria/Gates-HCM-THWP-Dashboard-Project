import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Register this page with a different path
dash.register_page(__name__, path="/human-resources")

# Load CSV files into DataFrames
hr_personal_df = pd.read_csv("data/CSVs/cleaned_hrh_personal_data.csv")

facilities_df = pd.read_csv("data/CSVs/facilities.csv")
wards_df = pd.read_csv("data/CSVs/wards.csv")
lgas_df = pd.read_csv("data/CSVs/lgas.csv")
states_df = pd.read_csv("data/CSVs/states.csv")

# Merge datasets to create necessary relationships
wards_lgas_df = pd.merge(wards_df, lgas_df, left_on="lga_id", right_on="id")
facilities_wards_df = pd.merge(
    facilities_df, wards_df, left_on="ward_id", right_on="id"
)


# Calculate percentages
total_employees = len(hr_personal_df)
formatted_total_employees = "{:,}".format(total_employees)

# Registration - Gender
male_employees = hr_personal_df.query('gender in ["male", "Male"]').shape[0]
female_employees = hr_personal_df.query('gender in ["female", "Female"]').shape[0]

male_percentage = (male_employees / total_employees) * 100 if total_employees > 0 else 0
formatted_male_percentage = "{:.2f}".format(male_percentage)
female_percentage = (
    (female_employees / total_employees) * 100 if total_employees > 0 else 0
)
formatted_female_percentage = "{:.2f}".format(female_percentage)

# Personal - Disability
disability_status_employees = hr_personal_df.query("disability_status in [1, 1]").shape[
    0
]

disability_status_percentage = (
    (disability_status_employees / total_employees) * 100 if total_employees > 0 else 0
)
formatted_disability_status_percentage = "{:.2f}".format(disability_status_percentage)


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
                                        dcc.Dropdown(
                                            id="hr-state-filter",
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
                                            id="hr-lga-filter", placeholder="Select LGA"
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="hr-ward-filter",
                                            placeholder="Select Ward",
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id="hr-facility-filter",
                                            placeholder="Select Facility",
                                            multi=True,
                                            style={"width": "100%"},
                                        ),
                                        width=5,
                                    ),
                                    dbc.Col(
                                        width=1,
                                    ),
                                ],
                                className="mb-4",
                            ),
                            # Display the indicators
                            # dbc.Row(
                            #     [
                            #         dbc.Col(
                            #             dbc.Card(
                            #                 dbc.CardBody(
                            #                     [
                            #                         html.H4(
                            #                             "Registered Employees:",
                            #                             className="card-title",
                            #                         ),
                            #                         html.H5(
                            #                             formatted_total_employees,
                            #                             className="card-text",
                            #                         ),
                            #                     ]
                            #                 ),
                            #                 className="card text-white bg-success mb-4",
                            #             ),
                            #             width=3,
                            #         ),
                            #         dbc.Col(
                            #             dbc.Card(
                            #                 dbc.CardBody(
                            #                     [
                            #                         html.H4(
                            #                             "Male Employees:",
                            #                             className="card-title",
                            #                         ),
                            #                         html.H5(
                            #                             formatted_male_percentage,
                            #                             className="card-text",
                            #                         ),
                            #                     ]
                            #                 ),
                            #                 className="card text-white bg-success mb-4",
                            #             ),
                            #             width=3,
                            #         ),
                            #         dbc.Col(
                            #             dbc.Card(
                            #                 dbc.CardBody(
                            #                     [
                            #                         html.H4(
                            #                             "Female Employees(%):",
                            #                             className="card-title",
                            #                         ),
                            #                         html.H5(
                            #                             formatted_female_percentage,
                            #                             className="card-text",
                            #                         ),
                            #                     ]
                            #                 ),
                            #                 className="card text-white bg-success mb-4",
                            #             ),
                            #             width=3,
                            #         ),
                            #         dbc.Col(
                            #             dbc.Card(
                            #                 dbc.CardBody(
                            #                     [
                            #                         html.H4(
                            #                             "Employees with Disabilities:",
                            #                             className="card-title",
                            #                         ),
                            #                         html.H5(
                            #                             formatted_disability_status_percentage,
                            #                             className="card-text",
                            #                         ),
                            #                     ]
                            #                 ),
                            #                 className="card text-white bg-success mb-4",
                            #             ),
                            #             width=3,
                            #         ),
                            #     ]
                            # ),
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
