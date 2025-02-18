import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Register this page with a different path
dash.register_page(__name__, path="/payroll")


# Define layout function
def layout():
    return dbc.Container(
        fluid=True,
    )
