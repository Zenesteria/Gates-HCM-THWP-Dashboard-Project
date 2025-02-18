import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from components.callbacks import register_callbacks

# Create the Dash app with multipage support
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.Navbar(
    dbc.Container(
        [
            # Brand (logo and text)
            dbc.Row(
                [
                    # Logo on the left
                    dbc.Col(
                        html.Img(
                            src="/assets/gsphcda_logo.jpg", height="40px"
                        ),  # Adjust the height of the logo
                        width="auto",
                        className="me-2",  # Add space between the logo and the text
                    ),
                    # Brand text on the right, increased font size
                    dbc.Col(
                        dbc.NavbarBrand(
                            "Tracking Health Worker Productivity Dashboard",
                            style={
                                "font-size": "1.5rem",
                                "font-weight": "bold",
                            },  # Customize font size and weight
                        ),
                        width="auto",
                    ),
                ],
                align="center",
                className="g-0",  # No gutter spacing between columns
            ),
            # Navigation links (aligned to the right)
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(dcc.Link("Home", href="/", className="nav-link")),
                        dbc.NavItem(
                            dcc.Link(
                                "Human Resources",
                                href="/human-resources",
                                className="nav-link",
                            )
                        ),
                        # dbc.NavItem(
                        #     dcc.Link(
                        #         "Attendance",
                        #         href="/attendance",
                        #         className="nav-link",
                        #     )
                        # ),
                        dbc.NavItem(
                            dcc.Link(
                                "Visitation", href="/visitation", className="nav-link"
                            )
                        ),
                        dbc.NavItem(
                            dcc.Link("Payroll", href="/payroll", className="nav-link")
                        ),
                    ],
                    className="ms-auto",  # Align navigation items to the right
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ],
        fluid=True,
    ),
    color="success",
    dark=True,
    sticky="top",  # Navbar stays fixed at the top
)


footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Div(
                        [
                            html.Div("Powered By: "),
                            html.A(
                                href="https://hcm.ng/rite/",
                                children=[
                                    html.Img(
                                        alt="HCM",
                                        src="/assets/logo banner_cropped.png",
                                        style={
                                            "width": "150px",
                                            "height": "auto",
                                        },  # Adjust the width as needed
                                    )
                                ],
                            ),
                        ],
                        className="d-flex justify-content-center align-items-center gap-2",
                    ),
                ],
            )
        ],
    ),
    className="footer p-3",
    fluid=True,
)


# Define the layout, which includes the page navigation and content
app.layout = dbc.Container(
    [
        navbar,
        # Content of the current page
        dash.page_container,
        footer,
    ],
    fluid=True,
)

# Register the callbacks from the separate file
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
