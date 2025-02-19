import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# from components.sidebar import sidebar

# Load CSV files into DataFrames
patients_df = pd.read_csv("data/CSVs/cleaned_patients_data.csv")
facilities_df = pd.read_csv("data/CSVs/facilities.csv")
wards_df = pd.read_csv("data/CSVs/wards_gombe.csv")
lgas_df = pd.read_csv("data/CSVs/lgas_gombe.csv")
states_df = pd.read_csv("data/CSVs/states_gombe.csv")
visitation_df = pd.read_csv("data/CSVs/cleaned_visitations_data.csv")
hr_personal_df = pd.read_csv("data/CSVs/cleaned_hrh_personal_data.csv")

patients_visitation_df = pd.merge(
    visitation_df, patients_df, left_on="patient_id", right_on="patient_id"
)

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

# Calculate percentages
total_patients = len(patients_df)
# "{:.1f}K".format(...) formats the value to one decimal place and appends the "K" for thousands.
# For example, if total_patients = 53240, the formatted value would be displayed as 53.2K.
# formatted_total_patients = "{:.1f}K".format(total_patients / 1000)

formatted_total_patients = "{:,}".format(total_patients)
total_lgas = 1  # len(lgas_df)
total_wards = len(wards_df)
total_facilities = 24  # len(facilities_df)
# Registration - Gender
male_patients = patients_df.query('gender in ["male", "Male"]').shape[0]
female_patients = patients_df.query('gender in ["female", "Female"]').shape[0]

male_percentage = (male_patients / total_patients) * 100 if total_patients > 0 else 0
formatted_male_percentage = "{:.2f}".format(male_percentage)
female_percentage = (
    (female_patients / total_patients) * 100 if total_patients > 0 else 0
)
formatted_female_percentage = "{:.2f}".format(female_percentage)

# Visitation - Gender
v_male_patients = patients_visitation_df.query('gender in ["male", "Male"]').shape[0]
v_female_patients = patients_visitation_df.query(
    'gender in ["female", "Female"]'
).shape[0]

male_percentage = (male_patients / total_patients) * 100 if total_patients > 0 else 0
formatted_male_percentage = "{:.2f}".format(male_percentage)
female_percentage = (
    (female_patients / total_patients) * 100 if total_patients > 0 else 0
)
formatted_female_percentage = "{:.2f}".format(female_percentage)


# marital status
married_patients = patients_df.query('marital_status in ["married", "Married"]').shape[
    0
]
single_patients = patients_df.query('marital_status in  ["single", "Single"]').shape[0]

formatted_single_patients = "{:,}".format(single_patients)
formatted_married_patients = "{:,}".format(married_patients)

# Calculate percentages
hr_personal_df = pd.read_csv("data/CSVs/cleaned_hrh_personal_data.csv")
total_employees = len(hr_personal_df)
formatted_total_employees = "{:,}".format(total_employees)

# Personal - Disability
disability_status_employees = hr_personal_df.query("disability_status in [1, 1]").shape[
    0
]

disability_status_percentage = (
    (disability_status_employees / total_employees) * 100 if total_employees > 0 else 0
)
formatted_disability_status_percentage = "{:.2f}".format(disability_status_percentage)

line_colors = [
    "#062d14",
    "#18a145",
]

# Bar chart for age group distribution
desired_order = ["0-4", "5-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60+"]
# Custom hover template
hovertemp = "<b>Age Group: </b> %{x} <br>"
hovertemp += "<b>Patient Count: </b> %{y} <br>"

# Custom hover template for pie chart
ms_hovertemp = "<b>Status: </b> %{label}<br>"
ms_hovertemp += "<b>Count: </b> %{value}<br>"
ms_hovertemp += "<b>Percentage: </b> %{percent:.2%}<extra></extra>"

# Custom hover template for pie chart
g_hovertemp = "<b>Gender: </b> %{label}<br>"
g_hovertemp += "<b>Count: </b> %{value}<br>"
g_hovertemp += "<b>Percentage: </b> %{percent:.2%}<extra></extra>"

# Define custom colors for marital statuses
marital_status_colors = {
    "Single": "#062d14",
    "Married": "#15522a",
}

# 🔹 Bar Chart for Registered Patients (patients_df)
registered_marital_chart = dcc.Graph(
    figure=px.bar(
        x=list(marital_status_colors.keys()),
        y=[
            patients_df["marital_status"].value_counts().get(status, 0)
            for status in marital_status_colors.keys()
        ],
        color=list(marital_status_colors.keys()),
        color_discrete_map=marital_status_colors,
        labels={"x": "", "y": "Count"},
    )
    .update_traces(
        hovertemplate="<b>Status:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>"
    )
    .update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        # legend_title_text="Marital Status",  # Custom legend title
        title={
            "text": "<b><u>Patients by Marital Status</u></b>",
            "font": {"color": "#1E1E1E"},
        },
    ),
)

# 🔹 Bar Chart for Visiting Patients (patients_visitation_df)
visiting_marital_chart = dcc.Graph(
    figure=px.bar(
        x=list(marital_status_colors.keys()),
        y=[
            patients_visitation_df["marital_status"].value_counts().get(status, 0)
            for status in marital_status_colors.keys()
        ],
        color=list(marital_status_colors.keys()),
        color_discrete_map=marital_status_colors,
        labels={"x": "", "y": "Count"},
    )
    .update_traces(
        hovertemplate="<b>Status:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>"
    )
    .update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        # legend_title_text="Marital Status",  # Custom legend title
        title={
            "text": "<b><u>Patients by Marital Status</u></b>",
            "font": {"color": "#1E1E1E"},
        },
    ),
)

# Register this page in Dash's page registry
dash.register_page(__name__, path="/")


# Define layout function
def layout():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H5(
                        "Human Resources for Health Overview",
                        className="text-left my-4",
                    )
                )
            ),
            dbc.Row(
                [
                    # Column for main charts
                    dbc.Col(
                        [
                            # Display the indicators
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.H6(
                                                        [
                                                            "Patients: ",
                                                            html.Span(
                                                                formatted_total_patients,
                                                                style={
                                                                    "color": "orange"
                                                                },  # Set the color to orange
                                                            ),
                                                        ],
                                                        className="card-title",
                                                    ),
                                                ]
                                            ),
                                            className="card text-white bg-success mb-2",
                                            style={
                                                "height": "50px",
                                                "border": "2px solid green",  # Green border
                                                "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",  # Add shadow
                                            },  # Further reduced height for the cards
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.H6(
                                                        [
                                                            "LGAs: ",
                                                            html.Span(
                                                                total_lgas,
                                                                style={
                                                                    "color": "orange"
                                                                },  # Set the color to orange
                                                            ),
                                                        ],
                                                        className="card-title",
                                                    ),
                                                ]
                                            ),
                                            className="card text-white bg-success mb-2",
                                            style={
                                                "height": "50px",
                                                "border": "2px solid green",  # Green border
                                                "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",  # Add shadow
                                            },  # Further reduced height for the cards
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.H6(
                                                        [
                                                            "Wards: ",
                                                            html.Span(
                                                                total_wards,
                                                                className="indicator_value",
                                                                style={
                                                                    "color": "orange"
                                                                },  # Set the color to orange
                                                            ),
                                                        ],
                                                        className="card-title",
                                                    ),
                                                ]
                                            ),
                                            className="card text-white bg-success mb-2",
                                            style={
                                                "height": "50px",
                                                "border": "2px solid green",  # Green border
                                                "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",  # Add shadow
                                            },  # Further reduced height for the cards
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.H6(
                                                        [
                                                            "Facilities: ",
                                                            html.Span(
                                                                total_facilities,
                                                                style={
                                                                    "color": "orange"
                                                                },  # Set the color to orange
                                                            ),
                                                        ],
                                                        className="card-title",
                                                    )
                                                ]
                                            ),
                                            className="card text-white bg-success mb-2",
                                            style={
                                                "height": "50px",
                                                "border": "2px solid green",  # Green border
                                                "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",  # Add shadow
                                            },  # Further reduced height for the cards
                                        ),
                                        width=2,
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.H6(
                                                        [
                                                            "HRH: ",
                                                            html.Span(
                                                                formatted_total_employees,
                                                                style={
                                                                    "color": "orange"
                                                                },  # Set the color to orange
                                                            ),
                                                        ],
                                                        className="card-title",
                                                    ),
                                                ]
                                            ),
                                            className="card text-white bg-success mb-2",
                                            style={
                                                "height": "50px",
                                                "border": "2px solid green",  # Green border
                                                "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",  # Add shadow
                                            },  # Further reduced height for the cards
                                        ),
                                        width=2,
                                    ),
                                ],
                                className="bg-success py-1",  # Green background and white font
                            ),
                            ## Registration title
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.H5(
                                            "Registration Overview",
                                            className="text-left my-3",
                                        )
                                    )
                                ]
                            ),
                            # Registration charts
                            dbc.Row(
                                [
                                    # REGISTRATION - GENDER
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        figure=px.pie(
                                                            values=[
                                                                male_patients,
                                                                female_patients,
                                                            ],
                                                            names=[
                                                                "Male",
                                                                "Female",
                                                            ],
                                                            color_discrete_sequence=line_colors,
                                                        )
                                                        .update_traces(
                                                            hovertemplate=g_hovertemp
                                                        )  # Apply custom hover template
                                                        .update_layout(
                                                            showlegend=True,  # Remove legend
                                                            plot_bgcolor="rgba(0,0,0,0)",  # Remove background color of plot area
                                                            paper_bgcolor="rgba(0,0,0,0)",  # Remove background color of entire figure
                                                            legend_title_text="Gender",  # Custom legend title
                                                            title={
                                                                "text": "<b><u>Patients by Gender</u></b>",  # Bold and underline title
                                                                "font": {
                                                                    "color": "#1E1E1E"
                                                                },  # Set title color to green
                                                            },
                                                        ),
                                                        config={
                                                            "displayModeBar": True
                                                        },  # Disable Plotly menu bar
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
                                    # REGISTRATION - AGE GROUP
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        figure=px.bar(
                                                            x=desired_order,
                                                            y=[
                                                                patients_df["age_group"]
                                                                .value_counts()
                                                                .get(age_group, 0)
                                                                for age_group in desired_order
                                                            ],
                                                            color=desired_order,
                                                            color_discrete_map={
                                                                "0-4": "#062d14",
                                                                "5-9": "#15522a",
                                                                "10-19": "#165e2e",
                                                                "20-29": "#177e38",
                                                                "30-39": "#18a145",
                                                                "40-49": "#25c258",
                                                                "50-59": "#4cdc7a",
                                                                "60+": "#88eda7",
                                                            },
                                                            labels={
                                                                "x": "",
                                                                "y": "Count",
                                                            },
                                                        )
                                                        .update_traces(
                                                            hovertemplate=hovertemp
                                                        )  # Apply custom hover template
                                                        .update_layout(
                                                            showlegend=False,  # Remove legend
                                                            plot_bgcolor="rgba(0,0,0,0)",  # Remove background color of plot area
                                                            paper_bgcolor="rgba(0,0,0,0)",  # Remove background color of entire figure
                                                            # legend_title_text="Age Group",  # Custom legend title
                                                            title={
                                                                "text": "<b><u>Patient by Age Group</u></b>",  # Bold and underline title
                                                                "font": {
                                                                    "color": "#1E1E1E"
                                                                },  # Set title color to green
                                                            },
                                                        ),
                                                        config={
                                                            "displayModeBar": False
                                                        },  # Disable Plotly menu bar
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
                                    # REGISTRATION - MARITAL STATUS
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [registered_marital_chart],
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
                                ]
                            ),
                            ## Visitation title
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.H5(
                                            "Visitation Overview",
                                            className="text-left my-3",
                                        )
                                    )
                                ]
                            ),
                            # Charts 2 - Visitation
                            dbc.Row(
                                [
                                    # Pie chart for gender and age-group distribution
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        figure=px.pie(
                                                            values=[
                                                                v_male_patients,
                                                                v_female_patients,
                                                            ],
                                                            names=[
                                                                "Male",
                                                                "Female",
                                                            ],
                                                            color_discrete_sequence=line_colors,
                                                        )
                                                        .update_traces(
                                                            hovertemplate=g_hovertemp
                                                        )  # Apply custom hover template
                                                        .update_layout(
                                                            showlegend=True,  # Remove legend
                                                            plot_bgcolor="rgba(0,0,0,0)",  # Remove background color of plot area
                                                            paper_bgcolor="rgba(0,0,0,0)",  # Remove background color of entire figure
                                                            legend_title_text="Gender",  # Custom legend title
                                                            title={
                                                                "text": "<b><u>Patients by Gender</u></b>",  # Bold and underline title
                                                                "font": {
                                                                    "color": "#1E1E1E"
                                                                },  # Set title color to green
                                                            },
                                                        ),
                                                        config={
                                                            "displayModeBar": False
                                                        },  # Disable Plotly menu bar
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
                                    # Bar chart for patient age group distribution for registered patients and those who come for visitation
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        figure=px.bar(
                                                            x=desired_order,
                                                            y=[
                                                                patients_visitation_df[
                                                                    "age_group"
                                                                ]
                                                                .value_counts()
                                                                .get(
                                                                    age_group,
                                                                    0,
                                                                )
                                                                for age_group in desired_order
                                                            ],
                                                            color=desired_order,
                                                            color_discrete_map={
                                                                "0-4": "#062d14",
                                                                "5-9": "#15522a",
                                                                "10-19": "#165e2e",
                                                                "20-29": "#177e38",
                                                                "30-39": "#18a145",
                                                                "40-49": "#25c258",
                                                                "50-59": "#4cdc7a",
                                                                "60+": "#88eda7",
                                                            },
                                                            labels={
                                                                "x": "",
                                                                "y": "Count",
                                                            },
                                                        )
                                                        .update_traces(
                                                            hovertemplate=hovertemp
                                                        )  # Apply custom hover template
                                                        .update_layout(
                                                            showlegend=False,  # Remove legend
                                                            plot_bgcolor="rgba(0,0,0,0)",  # Remove background color of plot area
                                                            paper_bgcolor="rgba(0,0,0,0)",  # Remove background color of entire figure
                                                            # legend_title_text="Age Group",  # Custom legend title
                                                            title={
                                                                "text": "<b><u>Patient by Age Group</u></b>",  # Bold and underline title
                                                                "font": {
                                                                    "color": "#1E1E1E"
                                                                },  # Set title color to green
                                                            },
                                                        ),
                                                        config={
                                                            "displayModeBar": False
                                                        },  # Disable Plotly menu bar
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
                                    # VISITATION - MARITAL STATUS
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    visiting_marital_chart,
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
                                ]
                            ),
                        ],
                        width=12,
                    ),
                ]
            ),
        ],
        fluid=True,
    )
