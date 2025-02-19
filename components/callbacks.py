from dash import Input, Output, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


# Load CSV files into DataFrames
patients_df = pd.read_csv("data/CSVs/cleaned_patients_data.csv")
facilities_df = pd.read_csv("data/CSVs/facilities.csv")
wards_df = pd.read_csv("data/CSVs/wards.csv")
lgas_df = pd.read_csv("data/CSVs/lgas.csv")
states_df = pd.read_csv("data/CSVs/states.csv")
visitation_df = pd.read_csv("data/CSVs/cleaned_visitations_data.csv")

# Merge datasets
patients_visitation_df = pd.merge(
    patients_df,
    visitation_df.drop(columns=["patient_project_number", "facility_name"]),
    on="patient_id",
    how="inner",
)

# Convert date column
patients_visitation_df["start_date"] = pd.to_datetime(
    patients_visitation_df["start_date"]
)

# Extract date parts
patients_visitation_df["week_number"] = (
    patients_visitation_df["start_date"].dt.isocalendar().week
)

# Ensure all values are strings and strip any whitespace
patients_visitation_df["time_in"] = (
    patients_visitation_df["time_in"].astype(str).str.strip()
)


# Handle inconsistent time formats
def parse_time(time_str):
    try:
        return pd.to_datetime(time_str, format="%H:%M").hour  # Standard case: HH:MM
    except ValueError:
        try:
            return pd.to_datetime(
                time_str, format="%H:%M:%S"
            ).hour  # If seconds are present
        except ValueError:
            return np.nan  # If neither works, return NaN


# Apply function to extract hours
patients_visitation_df["hour"] = patients_visitation_df["time_in"].apply(parse_time)

# Drop NaN rows if necessary
patients_visitation_df.dropna(subset=["hour"], inplace=True)


patients_visitation_df["day_of_week"] = pd.to_datetime(
    patients_visitation_df["start_date"]
).dt.day_name()


##### HR Data -------------------------------------------------------------
hr_personal_df = pd.read_csv("data/CSVs/cleaned_hrh_personal_data.csv")
employment_df = pd.read_csv("data/CSVs/cleaned_hrh_employment_data.csv")


def merge_hr_data(hr_personal_df, employment_df):
    filtered_df = pd.merge(hr_personal_df, employment_df, on="email", how="inner")
    return filtered_df


merged_hr_data = merge_hr_data(hr_personal_df, employment_df)


# state=None, lga=None, ward=None,
def prepare_employee_counts_by_qualification(filtered_df, facility=None):
    # Apply filters based on the dropdown selections
    filtered_df = filtered_df.copy()
    if facility:
        # filtered_df = filtered_df[filtered_df["facility_stationed"] == facility]
        # Since facility is a list (multi-select), use .isin() to filter
        filtered_df = filtered_df[filtered_df["facility_stationed"].isin(facility)]

    # Group by qualification and count
    qualification_counts = (
        filtered_df.groupby("qualification").size().reset_index(name="counts")
    )

    return qualification_counts


def prepare_employee_distribution_by_age_group(filtered_df, facility=None):
    # Apply filters
    filtered_df = filtered_df.copy()
    if facility:
        # filtered_df = filtered_df[filtered_df["facility_stationed"] == facility]
        # Since facility is a list (multi-select), use .isin() to filter
        filtered_df = filtered_df[filtered_df["facility_stationed"].isin(facility)]

    # Define age group order
    # ["below 20", "20-29", "30-39", "40-49", "50-59", "60+"]
    age_group_order = ["< 20", "20-29", "30-39", "40-49", "50-59", "60+"]

    # Group by age group and count
    age_group_counts = (
        filtered_df.groupby("age_group").size().reset_index(name="counts")
    )

    # Ensure proper ordering of age groups
    age_group_counts["age_group"] = pd.Categorical(
        age_group_counts["age_group"], categories=age_group_order, ordered=True
    )
    age_group_counts = age_group_counts.sort_values("age_group")

    return age_group_counts


def prepare_percentage_distribution_by_cadre(filtered_df, facility=None):
    # Apply filters
    filtered_df = filtered_df.copy()
    if facility:
        # filtered_df = filtered_df[filtered_df["facility_stationed"] == facility]
        # Since facility is a list (multi-select), use .isin() to filter
        filtered_df = filtered_df[filtered_df["facility_stationed"].isin(facility)]

    # Group by cadre and count
    cadre_counts = filtered_df.groupby("cadre").size().reset_index(name="counts")

    # Calculate percentage
    cadre_counts["percentage"] = (
        cadre_counts["counts"] / cadre_counts["counts"].sum()
    ) * 100

    return cadre_counts


def prepare_employee_percentage_by_employment_type(filtered_df, facility=None):
    # Apply filters
    filtered_df = filtered_df.copy()
    if facility:
        # Since facility is a list (multi-select), use .isin() to filter
        filtered_df = filtered_df[filtered_df["facility_stationed"].isin(facility)]

    # Group by employment type and count
    employment_type_counts = (
        filtered_df.groupby("employment_type").size().reset_index(name="counts")
    )

    # Calculate percentage
    employment_type_counts["percentage"] = (
        employment_type_counts["counts"] / employment_type_counts["counts"].sum()
    ) * 100

    # Sort alphabetically by employment type
    employment_type_counts = employment_type_counts.sort_values(
        by="employment_type", ascending=False
    )

    return employment_type_counts


def prepare_emp_count_stackedbar(filtered_df, facility=None):
    # Apply filters
    filtered_df = filtered_df.copy()
    if facility:
        # filtered_df = filtered_df[filtered_df["facility_stationed"] == facility]
        # Since facility is a list (multi-select), use .isin() to filter
        filtered_df = filtered_df[filtered_df["facility_stationed"].isin(facility)]
    # Calculate the percentage of health workers by employment type
    employment_counts = (
        filtered_df.groupby("employment_type")["email"].count().reset_index()
    )
    employment_counts.columns = ["employment_type", "total_workers"]

    # Calculate percentage
    employment_counts["percent_health_workers"] = (
        employment_counts["total_workers"] / employment_counts["total_workers"].sum()
    ) * 100
    return employment_counts


def prepare_cadre_treemap_data(filtered_df, facility=None):
    # Apply filters
    filtered_df = filtered_df.copy()
    if facility:
        # Since facility is a list (multi-select), use .isin() to filter
        filtered_df = filtered_df[filtered_df["facility_stationed"].isin(facility)]

    # Clean and check for missing values in 'cadre'
    filtered_df["cadre"] = filtered_df["cadre"].fillna("Unknown")

    # Create a mock total number of health workers for demonstration purposes
    filtered_df["Total No. of Health Workers"] = filtered_df.groupby("cadre")[
        "cadre"
    ].transform("count")

    # Calculate percentage distribution of health workers by cadre
    total_health_workers = filtered_df["Total No. of Health Workers"].sum()
    filtered_df["% Distribution"] = (
        filtered_df["Total No. of Health Workers"] / total_health_workers
    ) * 100

    # Group the data by 'cadre' and calculate the total number of health workers
    top_10_cadres_df = (
        filtered_df.groupby("cadre")
        .agg({"Total No. of Health Workers": "sum"})
        .reset_index()
    )

    # Recalculate the % Distribution after grouping to avoid mean aggregation issues
    top_10_cadres_df["% Distribution"] = (
        (top_10_cadres_df["Total No. of Health Workers"] / total_health_workers) * 100
    ).round(2)  # Ensure the result is rounded to two decimal places

    # Sort by 'Total No. of Health Workers' and take the top 10 cadres
    top_10_cadres_df = top_10_cadres_df.sort_values(
        by="Total No. of Health Workers", ascending=False
    ).head(10)

    return top_10_cadres_df


# Load the CSV file
df = pd.read_csv("data/CSVs/cleaned_hrh_timecard_data.csv")

# Ensure date and time columns are in the correct format
df["date"] = pd.to_datetime(df["date"])
df["clockin_time"] = pd.to_datetime(df["clockin_time"], format="%H:%M:%S").dt.time

# Extract hour from clockin_time
df["clockin_hour"] = pd.to_datetime(df["clockin_time"], format="%H:%M:%S").dt.hour

# Extract day of the week from the date
df["weekday"] = df["date"].dt.day_name()


# Custom color scale
custom_colorscale = [
    [0, "lightgreen"],  # Low values
    [0.5, "yellow"],  # Midpoint values
    [1, "darkred"],  # High values
]

###### CALLBACKS


def register_visitation_page_callbacks(app):
    """Registers dropdown callbacks and charts update callback"""

    @app.callback(
        [
            # Output("heatmap-chart", "figure"),
            Output("gender-pie-chart", "figure"),
            Output("marital-status-bar-chart", "figure"),
            Output("visitation-by-age-group-bar-chart", "figure"),
        ],
        [
            Input("vs-facility-filter", "value"),
            Input("date-picker", "start_date"),
            Input("date-picker", "end_date"),
        ],
    )
    def update_charts(selected_facilities, start_date, end_date):
        """Updates all charts based on selected filters."""

        # Convert dates
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter data
        filtered_df = patients_visitation_df[
            (patients_visitation_df["start_date"] >= start_date)
            & (patients_visitation_df["start_date"] <= end_date)
        ]

        # Apply facility filter
        if selected_facilities:
            filtered_df = filtered_df[
                filtered_df["facility_name"].isin(selected_facilities)
            ]

        # print("Filtered DataFrame Shape:", filtered_df.shape)  # Debugging Output

        # **Handle empty dataset**
        if filtered_df.empty:
            empty_fig = px.scatter(title="No Data Available")
            return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

        # **2️⃣ Gender Pie Chart**
        gender_fig = px.pie(
            filtered_df,
            names="gender",
            hole=0.4,
            color_discrete_sequence=[
                "#062d14",
                "#18a145",
            ],  # Custom colors
        )

        # Remove background and legend
        gender_fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend_title_text="Gender",  # Custom legend title
            title={
                "text": "<b><u>Patients by Gender</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        # Customize hover template
        gender_fig.update_traces(hovertemplate="%{label}: %{percent}")

        # **3️⃣ Marital Status Bar Chart (Fixed)**
        if "marital_status" in filtered_df.columns:
            marital_status_counts = (
                filtered_df["marital_status"]
                .fillna("Unknown")
                .value_counts()
                .reset_index()
            )
            marital_status_counts.columns = ["marital_status", "count"]

            marital_fig = px.bar(
                marital_status_counts,
                x="marital_status",
                y="count",
                labels={"marital_status": "Marital Status", "count": "Count"},
                color="marital_status",
                color_discrete_sequence=[
                    "#062d14",
                    "#ddfbe6",
                ],
            )

            marital_fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                legend_title_text="Marital Status",  # Custom legend title
                title={
                    "text": "<b><u>Patients by Marital Status</u></b>",
                    "font": {"color": "#1E1E1E"},
                },
            )

            marital_fig.update_traces(
                hovertemplate="Marital Status: %{x} <br>Count: %{y}"
            )
        else:
            marital_fig = px.bar(title="Marital Status Data Not Available")

        # **4️⃣ Visitation Count by Age Group**
        # Define the correct order of age groups
        desired_order = [
            "0-4",
            "5-9",
            "10-19",
            "20-29",
            "30-39",
            "40-49",
            "50-59",
            "60+",
        ]

        # Create a dictionary of age group counts with missing groups set to zero
        age_group_counts = filtered_df["age_group"].value_counts().to_dict()
        age_group_counts = {age: age_group_counts.get(age, 0) for age in desired_order}

        # Create the bar chart
        visitation_age_fig = px.bar(
            x=list(age_group_counts.keys()),  # Ensure correct order
            y=list(age_group_counts.values()),
            color=list(age_group_counts.keys()),
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
            labels={"x": "Age Group", "y": "Visit Count"},
        )

        # Apply custom hover template and clean up layout
        visitation_age_fig.update_traces(
            hovertemplate="<b>Age Group:</b> %{x}<br><b>Visits:</b> %{y}<extra></extra>"
        )
        visitation_age_fig.update_layout(
            showlegend=False,  # Remove legend
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
            paper_bgcolor="rgba(0,0,0,0)",  # Transparent figure background
            title={
                "text": "<b><u>Visitation by Age Group</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        return gender_fig, marital_fig, visitation_age_fig

    # **5️⃣ heatmap showing visitation count by hour of the day and day of the week.
    @app.callback(
        Output("hourly-traffic-heatmap", "figure"),
        [
            Input("vs-facility-filter", "value"),
            Input("date-picker", "start_date"),
            Input("date-picker", "end_date"),
        ],
    )
    def update_hourly_heatmap(selected_facilities, start_date, end_date):
        """Updates the heatmap showing visitation count by hour of the day and day of the week."""

        # Filter data based on date range
        filtered_df = patients_visitation_df[
            (patients_visitation_df["start_date"] >= pd.to_datetime(start_date))
            & (patients_visitation_df["start_date"] <= pd.to_datetime(end_date))
        ]

        # Apply facility filter
        if selected_facilities:
            filtered_df = filtered_df[
                filtered_df["facility_name"].isin(selected_facilities)
            ]

        # Add hour and weekday name columns
        filtered_df["hour"] = pd.to_datetime(
            filtered_df["time_in"], errors="coerce"
        ).dt.hour
        filtered_df["weekday"] = pd.to_datetime(
            filtered_df["start_date"], errors="coerce"
        ).dt.day_name()

        # Ensure the weekdays are ordered correctly
        weekday_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        # Group by weekday and hour to get counts
        heatmap_data = (
            filtered_df.groupby(["weekday", "hour"]).size().reset_index(name="count")
        )

        # Pivot the data for heatmap (weekday as rows, hour as columns)
        pivot_df = heatmap_data.pivot(
            index="weekday", columns="hour", values="count"
        ).reindex(weekday_order)

        # Create heatmap using go.Heatmap for more control
        fig = go.Figure(
            data=go.Heatmap(
                z=pivot_df.values,
                x=pivot_df.columns,
                y=pivot_df.index,
                colorscale=[
                    [0.0, "lightgreen"],  # Lighter green for the lowest values
                    [0.5, "yellow"],  # Yellow for mid-range values
                    [1.0, "darkred"],  # Dark red for the highest values
                ],
                hovertemplate="Hour: %{x}<br>Weekday: %{y}<br>Count: %{z}",
                hoverinfo="x+y+z",  # Exclude trace name from hover information
                name="",  # Set name to empty to remove "trace 0"
            )
        )
        # Update layout for better hourly view
        fig.update_layout(
            # title={
            #     # "text": f"Visitation Trends for {selected_facilities}",
            #     "text": "Visitation Traffic (Time and Day of the Week)",
            #     "font": {
            #         "size": 20,  # You can adjust the size if needed
            #         "color": "#1E1E1E",  # Set title color to green
            #         "family": "Arial",  # Optionally set font family
            #         "weight": "bold",  # Set font weight to bold
            #     },
            #     "x": 0.5,  # Center the title
            #     "xanchor": "center",
            #     "yanchor": "top",
            # },
            title={
                "text": "<b><u>Visitation Traffic (Time and Day of the Week)</u></b>",
                "font": {"color": "#1E1E1E"},
            },
            xaxis_title="Hour of Day (0-23)",
            yaxis_title="Weekday",
            xaxis=dict(tickmode="linear", dtick=1),
        )

        return fig

    @app.callback(
        Output("visitation-chart", "figure"),
        [
            Input("vs-facility-filter", "value"),
            Input("date-picker", "start_date"),
            Input("date-picker", "end_date"),
        ],
    )
    def update_chart(selected_facilities, start_date, end_date):
        # Filter data based on date range
        filtered_df = patients_visitation_df[
            (patients_visitation_df["start_date"] >= pd.to_datetime(start_date))
            & (patients_visitation_df["start_date"] <= pd.to_datetime(end_date))
        ]

        # Apply facility filter
        if selected_facilities:
            filtered_df = filtered_df[
                filtered_df["facility_name"].isin(selected_facilities)
            ]

        # Count rows for each visit_date
        visitations_over_time = (
            filtered_df.groupby("start_date")
            .size()
            .reset_index(name="visitation_count")
        )

        # Create the line chart
        fig = px.line(
            visitations_over_time,
            x="start_date",
            y="visitation_count",
            labels={"start_date": "Date", "visitation_count": "Total Visitations"},
            color_discrete_sequence=["green"],  # Change the line color here
        )

        # Improve layout
        fig.update_layout(xaxis_title="Date", yaxis_title="Total Visitations")
        # Remove background and legend
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            title={
                "text": "<b><u>Visitation Volume Over Time</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        return fig


def register_hr_page_callbacks(app):
    @app.callback(
        Output("employee-counts-by-qualification", "figure"),
        [
            Input("hr-facility-filter", "value"),
        ],
    )
    def update_employee_counts_by_qualification(facility):
        # state, lga, ward,
        qualification_counts = prepare_employee_counts_by_qualification(
            merged_hr_data, facility
        )
        if qualification_counts.empty:
            return go.Figure().add_annotation(
                text="No data available", x=0.5, y=0.5, showarrow=False
            )

        # Sort the DataFrame by 'counts' in descending order
        qualification_counts = qualification_counts.sort_values(
            "counts", ascending=False
        )

        # Create the bar chart
        fig = px.bar(
            qualification_counts,
            x="counts",
            y="qualification",
            labels={"counts": "Employee Count", "qualification": "Qualification"},
            orientation="h",  # Horizontal bars
            color_discrete_sequence=[
                "#18a145"
            ],  # Set the desired color (green in this case)
        )

        # Apply custom hover template and clean up layout
        fig.update_traces(
            hovertemplate="<b>Qualification:</b> %{y}<br><b>Counts:</b> %{x}<extra></extra>"
        )
        fig.update_layout(
            showlegend=True,  # Remove legend
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
            paper_bgcolor="rgba(0,0,0,0)",  # Transparent figure background
            title={
                "text": "<b><u>Employee Counts by Qualification</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        return fig

    @app.callback(
        Output("employee-distribution-by-age", "figure"),
        [
            Input("hr-facility-filter", "value"),
        ],
    )
    def update_employee_distribution_by_age(facility):
        age_group_counts = prepare_employee_distribution_by_age_group(
            merged_hr_data, facility
        )
        if age_group_counts.empty:
            return go.Figure().add_annotation(
                text="No data available", x=0.5, y=0.5, showarrow=False
            )

        fig = px.bar(
            age_group_counts,
            x="age_group",
            y="counts",
            labels={"counts": "Employee Count", "age_group": "Age Group"},
            color="age_group",  # Use 'age_group' column for color mapping
            # ["below 20", "20-29", "30-39", "40-49", "50-59", "60+"]
            color_discrete_map={
                "< 20": "#062d14",
                "20-29": "#15522a",
                "30-39": "#165e2e",
                "40-49": "#177e38",
                "50-59": "#18a145",
                "60+": "#25c258",
            },
        )

        # Apply custom hover template and clean up layout
        fig.update_traces(
            hovertemplate="<b>Age Group:</b> %{x}<br><b>Counts:</b> %{y}<extra></extra>"
        )
        fig.update_layout(
            showlegend=False,  # Remove legend
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
            paper_bgcolor="rgba(0,0,0,0)",  # Transparent figure background
            title={
                "text": "<b><u>Employee Distribution by Age Group</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        return fig

    @app.callback(
        Output("percentage-distribution-by-cadre", "figure"),
        [
            Input("hr-facility-filter", "value"),
        ],
    )
    def update_percentage_distribution_by_cadre(facility):
        # state, lga, ward,
        cadre_counts = prepare_percentage_distribution_by_cadre(
            merged_hr_data, facility
        )
        if cadre_counts.empty:
            return go.Figure().add_annotation(
                text="No data available", x=0.5, y=0.5, showarrow=False
            )
        if "cadre" not in cadre_counts.columns:
            return px.pie(title="Cadre column not found")
        # Sort the DataFrame by 'percentage' in descending order and select the top 10 rows
        top_10_cadre_counts = cadre_counts.sort_values(
            "percentage", ascending=False
        ).head(10)

        # Create the pie chart using the top 10 rows
        fig = px.pie(
            top_10_cadre_counts,
            names="cadre",
            values="percentage",
            labels={"percentage": "Percentage"},
            color_discrete_sequence=[
                "#062d14",
                "#15522a",
                "#165e2e",
                "#177e38",
                "#18a145",
                "#25c258",
                "#4cdc7a",
                "#88eda7",
                "#bcf6cd",
                "#ddfbe6",
            ],
        )

        # Apply custom hover template and clean up layout
        fig.update_traces(
            hovertemplate="<b>Cadre: </b> %{label}<br><b>Percentage: </b> %{percent:.2%}<extra></extra>"
        )
        fig.update_layout(
            showlegend=False,  # Remove legend
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
            paper_bgcolor="rgba(0,0,0,0)",  # Transparent figure background
            title={
                "text": "<b><u>Top 10 Percentage Distribution by Cadre</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        return fig

    @app.callback(
        Output("employee-percentage-by-employment-type", "figure"),
        [
            Input("hr-facility-filter", "value"),
        ],
    )
    def update_employee_percentage_by_employment_type(facility):
        # state, lga, ward,
        employment_type_counts = prepare_employee_percentage_by_employment_type(
            merged_hr_data, facility
        )
        if employment_type_counts.empty:
            return go.Figure().add_annotation(
                text="No data available", x=0.5, y=0.5, showarrow=False
            )
        if "employment_type" not in employment_type_counts.columns:
            return px.pie(title="Cadre column not found")

        fig = px.pie(
            employment_type_counts,
            names="employment_type",
            values="percentage",
            labels={"percentage": "Percentage"},
            color_discrete_sequence=[
                "#062d14",
                "#15522a",
                "#165e2e",
                "#177e38",
            ],
        )

        # Apply custom hover template and clean up layout
        fig.update_traces(
            hovertemplate="<b>Employment Type: </b> %{label}<br><b>Percentage: </b> %{percent:.2%}<extra></extra>"
        )
        fig.update_layout(
            showlegend=False,  # Remove legend
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
            paper_bgcolor="rgba(0,0,0,0)",  # Transparent figure background
            title={
                "text": "<b><u>Employee Percentage Count by Employment Type</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        return fig

    @app.callback(
        Output("employee-percentage-by-employment-type_sb", "figure"),
        [
            Input("hr-facility-filter", "value"),
        ],
    )
    def update_employee_percentage_by_employment_type_stackedbar(facility):
        employment_counts = prepare_employee_percentage_by_employment_type(
            merged_hr_data, facility
        )

        # Sort by employment_type to ensure the order is consistent for bars and legend
        employment_counts = employment_counts.sort_values("employment_type")

        # Create a stacked bar chart with multiple segments for each employment type
        fig = go.Figure()

        # Define the colors for the employment types
        colors = [
            "#062d14",
            "#165e2e",
            "#18a145",
            "#4cdc7a",
        ]

        # Add a segment for each employment type in the stacked bar
        for i, row in employment_counts.iterrows():
            fig.add_trace(
                go.Bar(
                    x=[row["percentage"]],  # Percentage for this employment type
                    name=row["employment_type"],  # Employment type as the label
                    orientation="h",
                    hovertemplate=f"Employment Type: {row['employment_type']}<br>Count: {row['counts']}<br>Percentage: {row['percentage']:.2f}%<extra></extra>",
                    text=f"{row['employment_type']}: {row['percentage']:.2f}%",
                    textposition="none",  # Hide the text inside the bar
                    marker_color=colors[
                        i % len(colors)
                    ],  # Cycle through the defined colors
                )
            )

        # Update the layout for the figure
        fig.update_layout(
            title={
                "text": "<b><u>% Health Workers by Employment Type</u></b>",
                "font": {"color": "#1E1E1E"},
            },
            xaxis_title="",
            barmode="stack",  # Stack the bars horizontally
            showlegend=True,  # Show the legend for the employment types
            legend_title_text="Workers Group",  # Custom legend title
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis_title="",  # Remove the y-axis title
            height=200,  # Adjust the height of the chart here
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Aligns the top of the legend box with the position defined by 'y'
                y=-0.6,  # Move the legend further down to add more space
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Position it at the center of the chart
            ),
        )

        # Optional: Customize y-axis ticks if needed
        fig.update_yaxes(
            tickmode="auto",  # Ensure tickmarks display correctly
            showline=True,  # Show the axis line
            zeroline=False,  # Disable the "zero" reference line
            showgrid=True,  # Optionally, show or hide the gridlines
        )

        return fig

    @app.callback(
        Output("percentage-distribution-by-cadre_treemap", "figure"),
        [
            Input("hr-facility-filter", "value"),
        ],
    )
    def update_percentage_distribution_by_cadre_treemap(facility):
        top_10_cadres_df = prepare_cadre_treemap_data(merged_hr_data, facility)

        # Create the treemap
        fig = px.treemap(
            top_10_cadres_df,
            path=["cadre"],  # The hierarchy of categories (only 'cadre' here)
            values="Total No. of Health Workers",  # The metric to represent the size of the treemap areas
            color="% Distribution",  # The column used to color the treemap
            color_continuous_scale="BuGn",  # Color scale for the treemap
        )

        # Remove grey background by setting plot and paper background to white (or transparent if you prefer)
        fig.update_layout(
            plot_bgcolor="white",  # Background color of the plot area
            paper_bgcolor="white",  # Background color of the entire figure
            title={
                "text": "<b><u>% Distribution of Health Workers by Cadre (Top 10)</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        # Update the hovertemplate to display both total workers and % distribution
        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Total Workers: %{value}<br>% Distribution: %{color:.2f}%<extra></extra>"
        )
        # fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

        return fig


def register_attendance_callbacks(app):
    # Callback to update charts based on selected year and date range
    # Callback to update charts based on selected year and date range
    @app.callback(
        [Output("time-series", "figure"), Output("heatmap", "figure")],
        [
            Input("year-dropdown", "value"),
            Input("date-range", "start_date"),
            Input("date-range", "end_date"),
        ],
    )
    def update_charts(selected_year, start_date, end_date):
        # Initially use the entire dataset
        filtered_df = df.copy()

        # Filter data based on the selected date range
        filtered_df = filtered_df[
            (filtered_df["date"] >= start_date) & (filtered_df["date"] <= end_date)
        ]

        if selected_year:
            # Filter data based on selected year
            filtered_df = df[df["date"].dt.year == selected_year]

        # Prepare time series data
        time_series_data = (
            filtered_df.groupby("date")["employee_id"]
            .nunique()
            .reset_index(name="employee_count")
        )

        # Prepare heatmap data (group by clockin_hour and weekday)
        heatmap_data = (
            filtered_df.groupby(["clockin_hour", "weekday"])["employee_id"]
            .nunique()
            .reset_index()
        )
        heatmap_data_pivot = heatmap_data.pivot(
            index="clockin_hour", columns="weekday", values="employee_id"
        )

        # Ensure weekdays are ordered correctly
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

        # Create time series plot
        time_series_fig = px.line(
            time_series_data,
            x="date",
            y="employee_count",
            title="Employee Count Over Time",
        )

        # Create heatmap with custom color scale
        heatmap_fig = px.imshow(
            heatmap_data_pivot,
            labels=dict(x="Weekday", y="Hour of Day", color="Employee Count"),
            x=weekday_order,
            y=heatmap_data_pivot.index,
            title="Employee Count Heatmap (Hour vs Weekday)",
            aspect="auto",
            color_continuous_scale=custom_colorscale,  # Apply custom color scale
        )

        return time_series_fig, heatmap_fig


# Define the function for registering callbacks for each page with multiple IDs
def register_filter_callbacks(
    app, state_filter, lga_filter, ward_filter, facility_filter
):
    # 🏽 **1️⃣ Update LGA dropdown based on selected State**
    @app.callback(Output(lga_filter, "options"), Input(state_filter, "value"))
    def update_lga_options(selected_state):
        if selected_state:
            state_id = states_df.loc[
                states_df["state_name"] == selected_state, "id"
            ].values[0]
            lgas_in_state = lgas_df[lgas_df["state_id"] == state_id]
            return [
                {"label": lga, "value": lga}
                for lga in lgas_in_state["lga_name"].unique()
            ]
        return []

    # 🏽 **2️⃣ Update Ward dropdown based on selected LGA**
    @app.callback(Output(ward_filter, "options"), Input(lga_filter, "value"))
    def update_ward_options(selected_lga):
        if selected_lga:
            lga_id = lgas_df.loc[lgas_df["lga_name"] == selected_lga, "id"].values[0]
            wards_in_lga = wards_df[wards_df["lga_id"] == lga_id]
            return [
                {"label": ward, "value": ward} for ward in wards_in_lga["name"].unique()
            ]
        return []

    # 🏽 **3️⃣ Update Facility dropdown based on selected Ward**
    @app.callback(Output(facility_filter, "options"), Input(ward_filter, "value"))
    def update_facility_options(selected_ward):
        if selected_ward:
            ward_id = wards_df.loc[wards_df["name"] == selected_ward, "id"].values[0]
            facilities_in_ward = facilities_df[facilities_df["ward_id"] == ward_id]
            return [
                {"label": facility, "value": facility}
                for facility in facilities_in_ward["name"].unique()
            ]
        return []


# Main function to register all callbacks for the app
def register_callbacks(app):
    # Register visitation page callbacks
    register_visitation_page_callbacks(app)

    # Register callbacks for Page 1 (vs-page)
    register_filter_callbacks(
        app, "vs-state-filter", "vs-lga-filter", "vs-ward-filter", "vs-facility-filter"
    )

    # Register callbacks for Page 2 (hr-page)
    register_filter_callbacks(
        app, "hr-state-filter", "hr-lga-filter", "hr-ward-filter", "hr-facility-filter"
    )

    register_hr_page_callbacks(app)

    register_attendance_callbacks(app)
