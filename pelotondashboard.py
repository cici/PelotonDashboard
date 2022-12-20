from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

# from csv_generator import generate_csv

pio.renderers.default = "vscode"


df = pd.read_csv("CacheCoder_workouts.csv",
                 converters={'Length (minutes)': lambda x: pd.to_numeric(
                     x, errors='ignore')}
                 )

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

ts = "Workout Timestamp"
discipline_cycling = "Cycling"
calorie_field = "Calories Burned"
length_minutes = "Length (minutes)"
distance_miles = "Distance (mi)"

titleCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H1(
                    "Peloton Workout Dashboard", className="card-title"
                )
            ]
        )
    ],
    color="#fff",
    inverse=True,
    style={
        "background-color": "#1A5B92",
        "color"": "  # fff",
        "width": "55rem",
        "margin-left": "1rem",
        "margin-top": "1rem",
        "margin-bottom": "1rem",
    },
)

def create_total_rides_card(df: pd.DataFrame) -> dbc.Card:
    total_rides = getCountByDiscipline(df, discipline_cycling)
    return dbc.Card(
        [
            dbc.CardHeader(html.H5(total_rides, className="card-title")),
            dbc.CardBody(html.P("Total Rides", className="card-text"))
        ],
        className="text-center shadow"
    )

def create_total_riding_calories_card(df: pd.DataFrame) -> dbc.Card:
    total_riding_calories = getSumByDiscipline(
        df, discipline_cycling, calorie_field)
    return dbc.Card(
        [
            dbc.CardHeader(html.H5(total_riding_calories, className="card-title")),
            dbc.CardBody(html.P("Total Calories Burned Riding", className="card-text"))
        ],
        className="text-center shadow"
    )

def create_total_minutes_riding_card(df: pd.DataFrame) -> dbc.Card:
    # Convert to float (since float can have a null)
    df['Length (minutes)'] = pd.to_numeric(
        df['Length (minutes)'], errors='coerce')
    total_minutes_riding = getSumByDiscipline(
        df, discipline_cycling, length_minutes)
    return dbc.Card(
        [
            dbc.CardHeader(html.H5(total_minutes_riding, className="card-title")),
            dbc.CardBody(html.P("Total Minutes Riding", className="card-text"))
        ],
        className="text-center shadow"
    )

def create_total_miles_riding_card(df: pd.DataFrame) -> dbc.Card:
    total_miles_riding = getSumByDiscipline(
        df, discipline_cycling, distance_miles)
    return dbc.Card(
        [
            dbc.CardHeader(html.H5(total_miles_riding, className="card-title")),
            dbc.CardBody(html.P("Total Miles Riding", className="card-text"))
        ],
        className="text-center shadow"
    )

def create_totals(df: pd.DataFrame):


    # Convert to float (since float can have a null)
    df['Length (minutes)'] = pd.to_numeric(
        df['Length (minutes)'], errors='coerce')

    total_riding_calories = getSumByDiscipline(
        df, discipline_cycling, calorie_field)
    total_rides = getCountByDiscipline(df, discipline_cycling)
    total_minutes_riding = getSumByDiscipline(
        df, discipline_cycling, length_minutes)
    total_miles_riding = getSumByDiscipline(
        df, discipline_cycling, distance_miles)
    totalsCardGroup = dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.CardHeader(html.H5(total_rides, className="card-title")),
                    dbc.CardBody(html.P("Total Rides", className="card-text"))
                ],
                className="text-center shadow"
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(total_minutes_riding, className="card-title"),
                        html.P("Total Minutes Riding", className="card-text")
                    ]
                )
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(total_miles_riding, className="card-title"),
                        html.P("Total Miles Riding", className="card-text")
                    ]
                )
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(total_riding_calories, className="card-title"),
                        html.P("Total Calories Burned Riding", className="card-text")
                    ]
                )
            ),
        ]
    )
    return totalsCardGroup

def create_totals_header_card(df: pd.DataFrame) -> dbc.Card:
    """
    Creates a dbc card with overall totals (rides, minutes spent, miles traveled, calories burned)

    Parameters
    ----------
        df : pd.DataFrame The dataframe to be plotted.

    Returns
    -------
        dbc.Card: Card with header and totals.
    """
    calorie_field = "Calories Burned"
    discipline_cycling = "Cycling"
    length_minutes = "Length (minutes)"
    distance_miles = "Distance (mi)"

    # Convert to float (since float can have a null)
    df['Length (minutes)'] = pd.to_numeric(
        df['Length (minutes)'], errors='coerce')

    total_riding_calories = getSumByDiscipline(
        df, discipline_cycling, calorie_field)
    total_rides = getCountByDiscipline(df, discipline_cycling)
    total_minutes_riding = getSumByDiscipline(
        df, discipline_cycling, length_minutes)
    total_miles_riding = getSumByDiscipline(
        df, discipline_cycling, distance_miles)

    # start_date = pd.to_datetime(df['Workout Timestamp']).dt.strftime("%YYYY-%MM-%d")
    workout_date = df['Workout Timestamp'].str.split("(")
    # workout_date = workout_date_time.str.split(" ")
    print("workout date")
    print(workout_date)
    min_start_date = workout_date.min()
    max_start_date = workout_date.max()

    # parsed_date = pd.to_datetime(start_date).dt.strftime("%YYYY-%MM-%d")

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.Center(
                        html.H1(
                            "Ride Totals",
                            className="card-title",
                        )
                    ),
                    html.Center(
                        html.H6(
                            "({} - {})".format(min_start_date[0], max_start_date[0]), className="card-title"
                        )
                    ),
                    html.H5(total_minutes_riding, className="card-title"),
                    html.P("Total Minutes Riding", className="card-text"),

                ]
            )
        ],
        color="#fff",
        inverse=True,
        style={
            "background-color": "#1A5B92",
            "color"": "  # fff",
            "width": "55rem",
            "margin-left": "1rem",
            "margin-top": "1rem",
            "margin-bottom": "1rem",
        },
    )

def group_data_by_timestamp(
    start_date=df[ts].min(), end_date=df[ts].max(), freq: str = "W"
) -> pd.DataFrame:
    """
    Filters dataframe by date range and groups by frequency of week by default.
    Returns a dataframe with Calories Burned and Total Output summed by the chosen frequency.

    Parameters
    ----------
        start_date : date The start date of the range
        end_date : date The end date of the range
        freq : str The frequency of the group. Default is weekly.

    Returns
    -------
        df : pd.DataFrame The dataframe with the summed columns.

    """
    dff = df.loc[(start_date <= df[ts]) & (df[ts] <= end_date)]

    for tz in ["EST", "EDT", "-04", "-05"]:
        dff.loc[:, ts] = dff[ts].str.replace(f"\({tz}\)", "", regex=True)

    dff.loc[:, ts] = pd.to_datetime(
        dff[ts], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    return (
        dff.groupby(pd.Grouper(key=ts, freq=freq))[
            ["Calories Burned", "Total Output"]]
        .agg("sum")
        .reset_index()
    )


#print(group_data_by_timestamp())


def create_timeseries_figure(df: pd.DataFrame, frequency="W") -> go.Figure:
    """
    Creates a timeseries figure with two subplots. The first subplot graphs
    the Total Output for the week. The second subplot graphs the Calories Burned
    for the week.

    Parameters
    ----------
        df : pd.DataFrame The dataframe to be plotted.
        frequency : str The frequency of the group. Default is weekly.

    Returns
    -------
        go.Figure: The figure to be plotted.
    """
    switcher = {"D": "Day", "W": "Week", "M": "Month"}
    freq = switcher.get(frequency, "Week")
    line = make_subplots(specs=[[{"secondary_y": True}]])
    line.add_trace(
        go.Scatter(
            x=df["Workout Timestamp"],
            y=df["Calories Burned"],
            marker=dict(size=10, color="MediumPurple"),
            name="Total Calories",
        ),
        secondary_y=False,
    )
    line.add_trace(
        go.Scatter(
            x=df["Workout Timestamp"],
            y=df["Total Output"],
            marker=dict(size=10, color="MediumSeaGreen"),
            name="Total Output",
        ),
        secondary_y=True,
    )

    line.update_layout(
        title=f"Calories and Total Output per {freq}",
        title_x=0.5,
        yaxis_title="Calories Burned",
    )

    line.update_yaxes(title_text="Total Output", secondary_y=True)
    line.update_yaxes(title_text="Calories Burned", secondary_y=False)
    line.update_xaxes(title=f"{freq}")
    return line

def create_calories_and_output_card(df: pd.DataFrame) -> dbc.Card:
    """
    Creates a dbc card with a title, DatePicker, RadioButton, and a timeseries figure.

    Parameters
    ----------
        df : pd.DataFrame The dataframe to be plotted.

    Returns
    -------
        dbc.Card: Card with header, datepicker, radio buttons and plot.
    """
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.Center(
                        html.H1(
                            "Weekly Calorie and Output Breakdown",
                            className="card-title",
                        )
                    ),
                    html.Center(
                        dcc.DatePickerRange(
                            id="date-range-picker-2",
                            min_date_allowed=df["Workout Timestamp"].min(),
                            max_date_allowed=df["Workout Timestamp"].max(),
                            initial_visible_month=df["Workout Timestamp"].min(
                            ),
                            start_date=df["Workout Timestamp"].min(),
                            end_date=df["Workout Timestamp"].max(),
                            style={"margin-top": "1rem",
                                   "margin-bottom": "1rem"},
                        )
                    ),
                    html.Center(
                        dcc.RadioItems(
                            options=[
                                {"label": "Daily", "value": "D"},
                                {"label": "Weekly", "value": "W"},
                                {"label": "Monthly", "value": "M"},
                            ],
                            value="W",
                            id="frequency-radio-2",
                            labelStyle={"padding-right": "20px"},
                        ),
                    ),
                    dcc.Graph(
                        id="calories-output-graph",
                    ),
                ]
            )
        ],
        outline=True,
        color="info",
        style={"width": "40rem", "margin-left": "5rem", "margin-bottom": "1rem"},
    )


@app.callback(
    Output("calories-output-graph", "figure"),
    [
        Input("date-range-picker-2", "start_date"),
        Input("date-range-picker-2", "end_date"),
        Input("frequency-radio-2", "value"),
    ],
)
def update_weekly_calories_burned_chart(start_date, end_date, frequency):
    """
    Updates the weekly calories burned chart with the selected date range and frequency.
    """
    grouped_df = group_data_by_timestamp(start_date, end_date, frequency)
    return create_timeseries_figure(grouped_df, frequency)


def get_instructor_chart(df: pd.DataFrame) -> px.scatter:
    pie = px.pie(
        df,
        values="Length (minutes)",
        names="Instructor Name",
        title="Time Spent per Instructor",
        hole=0.2,
    )
    pie.update_traces(textposition="inside", textinfo="percent+label")
    pie.update_layout(width=1600)
    pie.update_layout(title_x=0.5)
    return pie


def get_fitness_discipline_chart(df: pd.DataFrame) -> px.scatter:
    pie = px.pie(
        df,
        values="Length (minutes)",
        names="Fitness Discipline",
        title="Time Spent Per Fitness Discipline",
        hole=0.2,
    )
    pie.update_traces(textposition="inside", textinfo="percent+label")
    pie.update_layout(width=1600)
    pie.update_layout(title_x=0.5)
    return pie


def create_instructor_time_card(workout_df: pd.DataFrame) -> dbc.Card:
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.Center(
                        html.H1("Instructor Breakdown",
                                className="card-title")
                    ),
                    html.P(
                        "This chart shows the percentage of time spent with each instructor.",
                        className="card-body",
                    ),
                    dcc.Graph(
                        id="workouts-by-instructor",
                        figure=get_instructor_chart(workout_df),
                    ),
                ]
            )
        ],
        color="info",
        outline=True,
        style={"width": "40rem", "margin-bottom": "1rem"},
    )


def create_discipline_card(workout_df: pd.DataFrame) -> dbc.Card:
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.Center(
                        html.H1("Fitness Discipline Breakdown",
                                className="card-title")
                    ),
                    html.P(
                        "This chart shows the percentage of time spent in minutes for each fitness discipline.",
                        className="card-body",
                    ),
                    dcc.Graph(
                        id="fitness-discipline-by-calories-chart",
                        figure=get_fitness_discipline_chart(workout_df),
                    ),
                ]
            )
        ],
        color="info",
        outline=True,
        style={"width": "40rem", "margin-bottom": "1rem"},
    )


def get_instructors_by_discipline_chart(df: pd.DataFrame) -> px.bar:
    df.insert(0, "count", "")
    dff = (
        df.groupby(["Instructor Name", "Fitness Discipline"])["count"]
        .agg("count")
        .reset_index()
    )
    chart = px.bar(
        dff,
        x="Instructor Name",
        y="count",
        color="Fitness Discipline",
        title="Total Output by Instructor",
        width=1600,
    )
    chart.update_layout(title_x=0.5)
    return chart


def create_instructor_card(df: pd.DataFrame) -> dbc.Card:
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.Center(
                        html.H1(
                            "Instructor by Fitness Discipline", className="card-title"
                        )
                    ),
                    dcc.Graph(
                        id="instructor-by-discipline-chart",
                        figure=get_instructors_by_discipline_chart(df),
                        style={"margin-top": "1rem", "margin-bottom": "1rem"},
                    ),
                ]
            )
        ],
        color="info",
        outline=True,
        style={"margin-top": "1rem", "margin-left": "1rem",
               "margin-bottom": "1rem"},
    )


"""
 * Returns the sum of a number value within the objects of an array
 * @param {array} array Array of objects
 * @param {string} key Attribute pointing to a number within the objects of an array to get the sum of
 * @return {number} Sum
"""


def getTotalByAttribute(df, key):
    total = df[key].sum()
    return total


"""
 * Returns the average of a number value within the objects of an array
 * @param {array} array Array of objects
 * @param {string} key Attribute pointing to a number within the objects of an array to get the average of
 * @return {number} Average
"""


def getAverageByAttribute(df, key):
    average = df[key].avg()
    return average


def getCountByDiscipline(df, discipline):
    countByDiscipline = len(df[df['Fitness Discipline']
                               == discipline])
    return countByDiscipline


def getSumByDiscipline(df, discipline, key):
    print(key)
    sumByDiscipline = df.loc[df['Fitness Discipline']
                             == discipline, key].sum()
    return sumByDiscipline


app.layout = html.Div(
    children=[
        dbc.Row(
            [
                html.Center(titleCard),
            ],
            justify="center",
            style={"margin-left": "0.5rem"},
        ),
        dbc.Row(
            [
                #html.Center(create_totals_header_card(df))
                dbc.Col(create_total_rides_card(df)),
                dbc.Col(create_total_minutes_riding_card(df)),
                dbc.Col(create_total_miles_riding_card(df)),
                dbc.Col(create_total_riding_calories_card(df))
            ],
            style={"margin-bottom": "1.5rem", "margin-left": "0.5rem"},
        ),
        dbc.Row(
            [
                dbc.Col([create_calories_and_output_card(df)]),
                dbc.Col([create_discipline_card(df)]),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([create_instructor_card(df)])
            ]
        ),
        dbc.Row(
            [
                dbc.Col([create_instructor_time_card(df)])
            ]
        ),
    ]
)

app.run_server(debug=True)
