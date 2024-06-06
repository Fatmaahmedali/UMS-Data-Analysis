# Libraries
import dash
from dash import dcc, html, callback, Output, Input, State
from dash_extensions import Lottie
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from scipy import stats
from scipy.stats import linregress
from scipy.stats import f_oneway

# DB Libraries
import mysql.connector
from sqlalchemy import create_engine
from flask import session
from sqlalchemy import text
# store_uid = dcc.Store(id='store_uid')

import urllib.parse
from urllib.parse import urlparse, parse_qs
from flask import request

# Get the current URL and extract the query string
# url = request.url
# query_string = urllib.parse.urlparse(url).query
#
# # Parse the query string and extract the user_id parameter
# query_dict = urllib.parse.parse_qs(query_string)
# user_id = query_dict.get('user_id', [None])[0]
# print('wohi', user_id)

# Define the user_id value as a variable
# user_id = ''

from flask import session

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    database="mydb"
)

engine = create_engine(f'mysql+mysqlconnector://root@127.0.0.1:3306/mydb')
store_uid_student = dash.dcc.Store(id='store_uid_student')

# print("i accsess", store_uid_student)
################################### If I will Get The user ID FROM URL #################################################
# def update_user_id(search, current_user_id, user_id):
#     # Extract the user_id value from the URL query string
#     query_dict = urllib.parse.parse_qs(search[1:])
#     user_id = query_dict.get('user_id', [None])[0]
#
#     # If the user_id has changed, return the new value, otherwise return the current value
#     if user_id != current_user_id:
#         return user_id
#     else:
#         return dash.no_update

########################################################################################################################
########################################################################################################################

################################################## Queries #############################################################

########################################################################################################################
# CARDS QUERY
#
# query1 = """
# SELECT StudentID, PassedHours, RankValue, HoursInProgress, WarningsNumber, CGPA, Level
# FROM student
# where StudentID = '2v2nN3vhzK'
# """
#
# results = pd.read_sql_query(query1, engine)
# StudentID = results.iloc[0]['StudentID']
# PassedHoursValue = results.iloc[0]['PassedHours']
# RankValue = results.iloc[0]['RankValue']
# HoursInProgressValue = results.iloc[0]['HoursInProgress']
# WarningsNumberValue = results.iloc[0]['WarningsNumber']
# CGPAValue = results.iloc[0]['CGPA']
# LevelValue = results.iloc[0]['Level']
#
# print(StudentID)
# print(PassedHoursValue)
# print(RankValue)
# print(WarningsNumberValue)
# print(HoursInProgressValue)
# ########################################################################################################################
#
# ########################################################################################################################
# # FILTERS QUERY
query2 = """
SELECT *
FROM student_has_semester shs
INNER JOIN academicyear ay ON shs.AcademicYear_idAcademicYear = ay.idAcademicYear
WHERE Student_StudentID = '2v2nN3vhzK'
"""
results2 = pd.read_sql_query(query2, engine)

year_marks = {
    int(results2['Academic_Year_INT'].loc[i]): results2['Academic_Year_Name'].loc[i]
    for i in results2.index
}

semester_marks = {
    int(results2['Semester_INT'].loc[i]): results2['Semester_Name'].loc[i]
    for i in results2.index
}

print(year_marks)
print(semester_marks)

query3 = """
SELECT DISTINCT shc.Student_StudentID, shs.SGPA ,shc.Courses_CourseCode, shc.TotalMark ,shc.Grade,shc.CourseCategory, shc.CourseType,shc.AcademicYear_idAcademicYear, shp.Program_ProgramID, p.ProgramName, ay.Academic_Year_Name, ay.Semester_Name, ay.Academic_Year_INT, ay.Semester_INT
FROM student_has_courses shc
INNER JOIN student_has_program shp ON shc.Student_StudentID = shp.Student_StudentID
INNER JOIN program p ON p.ProgramID = shp.Program_ProgramID
INNER JOIN academicyear ay ON shc.AcademicYear_idAcademicYear = ay.idAcademicYear
INNER JOIN student_has_semester shs ON shs.Student_StudentID = shc.Student_StudentID AND shs.AcademicYear_idAcademicYear = shc.AcademicYear_idAcademicYear
where shc.Student_StudentID = 'wRvVWn5imY'
"""
results3 = pd.read_sql_query(query3, engine)
print(results3)
print(results3.columns)

########################################################################################################################
# # Student Semester (Without Summer) Query Used in analysis
Student_Query_data = """
SELECT DISTINCT shc.Student_StudentID, shs.SGPA ,shc.Courses_CourseCode, shc.TotalMark ,shc.Grade,shc.AcademicYear_idAcademicYear, ay.Academic_Year_Name, ay.Semester_Name
FROM student_has_courses shc
INNER JOIN student_has_program shp ON shc.Student_StudentID = shp.Student_StudentID
INNER JOIN program p ON p.ProgramID = shp.Program_ProgramID
INNER JOIN academicyear ay ON shc.AcademicYear_idAcademicYear = ay.idAcademicYear
INNER JOIN student_has_semester shs ON shs.Student_StudentID = shc.Student_StudentID AND shs.AcademicYear_idAcademicYear = shc.AcademicYear_idAcademicYear
where shc.Student_StudentID = '2v2nN3vhzK' AND Semester_Name != "summer"
"""
student_data = pd.read_sql_query(Student_Query_data, engine)

########################################################################################################################
# Courses Query
SubQuery1 = """
    SELECT c.CourseCode
    FROM courses c
    WHERE c.Level = 1 AND c.Semester = "spring"
"""
level1Courses_spring = pd.read_sql_query(SubQuery1, engine)

SubQuery2 = """
    SELECT c.CourseCode
    FROM courses c
    WHERE c.Level = 1 AND c.Semester = "autumn"
"""
level1Courses_autumn = pd.read_sql_query(SubQuery2, engine)

SubQuery3 = """
    SELECT c.CourseCode
    FROM courses c
    WHERE c.Level = 2 AND c.Semester = "spring"
"""
level2Courses_spring = pd.read_sql_query(SubQuery3, engine)

SubQuery4 = """
    SELECT c.CourseCode
    FROM courses c
    WHERE c.Level = 2 AND c.Semester = "autumn"
"""
level2Courses_autumn = pd.read_sql_query(SubQuery4, engine)

SubQuery5 = """
    SELECT c.CourseCode
    FROM courses c
    WHERE c.Level = 3 AND c.Semester = "spring"
"""
level3Courses_spring = pd.read_sql_query(SubQuery5, engine)

SubQuery6 = """
    SELECT c.CourseCode
    FROM courses c
    WHERE c.Level = 3 AND c.Semester = "autumn"
"""
level3Courses_autumn = pd.read_sql_query(SubQuery6, engine)

SubQuery7 = """
    SELECT c.CourseCode
    FROM courses c
    WHERE c.Level = 4 AND c.Semester = "spring"
"""
level4Courses_spring = pd.read_sql_query(SubQuery7, engine)

SubQuery8 = """
    SELECT c.CourseCode
    FROM courses c
    WHERE c.Level = 4 AND c.Semester = "autumn"
"""
level4Courses_autumn = pd.read_sql_query(SubQuery8, engine)


########################################################################################################################
year_min = 2019
year_max = 2023
year_marks = {year: str(year) for year in list(range(2019, 2023))}
year_value = [2019, 2023]
semester_min = 1
semester_max = 3
semester_marks = {1: 'Spring', 2: 'Autumn', 3: 'Summer'}
semester_value = [1, 3]

############################################# Statistical Analysis #####################################################
def perform_course_category_analysis(dataframe):
    # Select the relevant columns from the dataframe
    SelectedColumns = ['CourseCategory', 'TotalMark', 'Courses_CourseCode']
    CourseCategory_Stat = dataframe[SelectedColumns].dropna()

    # Group the courses by category
    categories = CourseCategory_Stat.groupby("CourseCategory")

    # Calculate the mean, median, and standard deviation of the grades for each category
    means = categories["TotalMark"].mean()
    medians = categories["TotalMark"].median()
    stds = categories["TotalMark"].std()

    # Test for significant differences in the grades between the different categories using ANOVA
    f_value, p_value = f_oneway(*[group["TotalMark"] for name, group in categories])

    # Find the category with the highest mean grade
    best_category = means.idxmax()

    # Determine the conclusion based on the P-value
    if p_value < 0.05:
        conclusion = f"There is a significant difference in your performance among different course categories\n" \
                     f"You Are Doing Very Well {best_category} Courses"
    else:
        conclusion = "There is no significant difference in your performance among different course categories"

    # Return the analysis results
    return conclusion


def perform_semester_type_analysis(dataframe):
    # Select the relevant columns from the dataframe
    SelectedColumns = ['Semester_Name', 'TotalMark', 'Courses_CourseCode']
    SemestersType_Stat = dataframe[SelectedColumns].dropna()

    # Group the courses by category
    semesters = SemestersType_Stat.groupby("Semester_Name")

    # Calculate the mean, median, and standard deviation of the grades for each Semester
    means = semesters["TotalMark"].mean()
    medians = semesters["TotalMark"].median()
    stds = semesters["TotalMark"].std()
    print(means)
    # Test for significant differences in the grades between the different Semester Types using ANOVA
    f_value, p_value = f_oneway(*[group["TotalMark"] for name, group in semesters])

    # Find the Semester with the highest mean grade
    best_semester_type = means.idxmax()

    # Determine the conclusion based on the P-value
    if p_value < 0.05:
        conclusion = f"- There is a significant difference in your performance among different semesters\n" \
                     f"You Are Doing Very Well {best_semester_type} Courses"
    else:
        conclusion = "- Your performance does not differ by semester types (spring, autumn, summer)\n" \
                     "You Performance is approximately the same"

    # Return the analysis results
    return conclusion


def calculate_stats_mode(data):
    mode, count = stats.mode(data)
    conclusion = f"You got '{mode[0]}' and it appears {count[0]} times\n This is the most repeated Grade."

    # Return the conclusion
    return conclusion


def studying_courses_in_not_same_ay(student_data):
    """
    Performs a two-sample t-test to determine if there is a significant difference in the mean total mark between rows
    with courses in the same academic year and those without.

    Returns a message indicating whether there is a significant difference or not. Returns None if all rows have courses
    in the same academic year.
    """
    grouped_courses22 = student_data.groupby('AcademicYear_idAcademicYear').agg(
        {'Courses_CourseCode': list, 'TotalMark': 'mean'}) \
        .rename(columns={'TotalMark': 'MeanTotalMark'})
    grouped_courses22 = grouped_courses22.dropna()  # drop rows with missing values

    def all_same_semester(course_codes):
        """
        Returns True if all course codes in the given list are in the same semester, and False otherwise.
        """
        semesters = set(int(c[5]) for c in course_codes)
        return len(semesters) == 1

    # apply the all_same_semester function to the Courses_CourseCode column
    grouped_courses22['In/NotIn Same Academic Year'] = grouped_courses22['Courses_CourseCode'].apply(all_same_semester)

    # replace True/False with "Same Academic Year"/"Not Same Academic Year"
    replacement_dict = {True: "Same Academic Year", False: "Not Same Academic Year"}
    grouped_courses22['In/NotIn Same Academic Year'] = grouped_courses22['In/NotIn Same Academic Year'].replace(
        replacement_dict)

    if 'Not Same Academic Year' not in grouped_courses22['In/NotIn Same Academic Year'].values:
        return None

    same_semester_mask = grouped_courses22['In/NotIn Same Academic Year'] == 'Same Academic Year'
    same_semester_marks = grouped_courses22.loc[same_semester_mask, 'MeanTotalMark']
    diff_semester_marks = grouped_courses22.loc[~same_semester_mask, 'MeanTotalMark']

    t_stat, p_value = ttest_ind(same_semester_marks, diff_semester_marks, equal_var=False)

    if p_value < 0.05:
        conclusion = "- There is a significant difference in Your Performance When You Register Courses From Different " \
                     "Academic years than when you Register Courses of the same academic year. "
    else:
        conclusion = "- There is NO significant difference in Your Performance When You Register Courses From Different " \
                     "Academic years than when you Register Courses of the same academic year. "

    return conclusion


########################################################################################################################
##### Lotifies #####
PassedHours = "https://assets3.lottiefiles.com/packages/lf20_oUGnCsAuf0.json"
InProgress = "https://assets2.lottiefiles.com/packages/lf20_d1oevcgk.json"
Warnings = "https://assets2.lottiefiles.com/packages/lf20_uRS1yeVDdH.json"
Ranking = "https://assets1.lottiefiles.com/packages/lf20_cv6rdeii.json"
Level = "https://assets6.lottiefiles.com/packages/lf20_o2hGVm.json"
CGPA = "https://assets7.lottiefiles.com/packages/lf20_UnKxTmoDGU.json"

options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
########################################################################################################################

##################################################### Graphs Definition ################################################
fig1 = px.sunburst()
fig2 = px.bar()
fig3 = go.Figure()

####### Define Sidebar #########
sidebar1 = dbc.Nav(
    children=[
        dbc.NavLink(
            [
                html.I(className="bi bi-graph-up-arrow"),
                html.Div("Performance", className="ms-2 text-black-50 d-inline", style={'font-weight': '600'}),
            ],
            href='/StudentInterface/home/pages/pg1?user_id=2v2nN3vhzK',
            active="exact",
        ),
        dbc.NavLink(
            [
                html.I(className="fa-solid fa-graduation-cap"),
                html.Div("Registration", className="ms-2 text-black-50 d-inline", style={'font-weight': '600'}),
            ],
            href='/StudentInterface/home/pages/pg2?user_id=2v2nN3vhzK',
            active="exact",
        ),
        dbc.NavLink(
            [
                html.I(className="bi bi-door-closed-fill"),
                html.Div("Logout", className="ms-2 text-black-50 d-inline", style={'font-weight': '600'}),
            ],
            href='/',
            active="exact",
        )
    ],
    vertical=True,
    pills=True,
    className="bg-light",
    style={
        'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
        'height': '765px',
        'position': 'fixed',
        'width': '171px'
    }
)
sidebar1.children[-1].style = {'order': '1', 'margin-top': '608px', 'font-size': '19px'}

# page 2
# dash.register_page(__name__, path='/performance', name='Tip Analysis')
layout1 = html.Div([
    dcc.Store(id='store_uid_student'),
    # html.Div(id='user-id'),
    # html.Div(id='passed-hours-output'),
    dbc.Row([
        dbc.Col([
            sidebar1
        ], xs=4, sm=4, md=1, lg=2, xl=2, xxl=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(Lottie(options=options, width="36%", height="67%", url=PassedHours),
                                       style={'background': 'white'}),
                        dbc.CardBody([
                            html.H6('Passed Hours',
                                    style={'font-weight': '900', 'color': 'white', 'font-size': '19px',
                                           'margin-top': '5px'}),
                            html.H2(id='PassedHours-value', style={'color': 'white'})
                        ], style={'textAlign': 'center', 'background': '#007bff'})
                    ]),
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(Lottie(options=options, width="58%", height="67%", url=InProgress),
                                       style={'background': 'white'}),
                        dbc.CardBody([
                            html.H6('In Progress',
                                    style={'font-weight': '900', 'color': 'white', 'font-size': '19px',
                                           'margin-top': '5px'}),
                            html.H2(id='InProgress-value', style={'color': 'white'})
                        ], style={'textAlign': 'center', 'background': '#007bff'})
                    ]),
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(Lottie(options=options, width="37%", height="53%", url=Ranking),
                                       style={'background': 'white'}),
                        dbc.CardBody([
                            html.H6('Rank', style={'font-weight': '900', 'color': 'white', 'font-size': '19px',
                                                   'margin-top': '5px'}),
                            html.H2(id='Rank-value', style={'color': 'white'})
                        ], style={'textAlign': 'center', 'background': '#007bff'})
                    ]),
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(
                            Lottie(options=options, width="37%", height="25%", url=Warnings),
                            style={'padding': '0px', 'background': 'white'}
                        ),
                        dbc.CardBody([
                            html.H6('Warnings', style={'font-weight': '900', 'color': 'white', 'font-size': '19px',
                                                       'margin-top': '5px'}),
                            html.H2(id='Warnings-value', style={'color': 'white'})
                        ], style={'textAlign': 'center', 'background': '#007bff'})
                    ]),
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(Lottie(options=options, width="37%", height="53%", url=Level),
                                       style={'background': 'white'}),
                        dbc.CardBody([
                            html.H6('Level', style={'color': 'white'}),
                            html.H2(id='level-value', style={'color': 'white'})
                        ], style={'textAlign': 'center', 'background': '#007bff'})
                    ]),
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(Lottie(options=options, width="37%", height="53%", url=CGPA),
                                       style={'background': 'white'}),
                        dbc.CardBody([
                            html.H6('CGPA', style={'color': 'white'}),
                            html.H2(id='CGPA-value', style={'color': 'white'})
                        ], style={'textAlign': 'center', 'background': '#007bff'})
                    ]),
                ], width=2),
            ], className='cards-row'),

            dbc.Row([
                dbc.Card([
                    dbc.CardHeader([
                        dbc.Row([
                            dbc.Col([
                                html.Div(children=[
                                    html.I(className="bi bi-calendar4-range", style={'color': '#007bff'}),
                                    html.Label("Year", style={'padding': '5px', 'font-weight': '600'}),
                                ]),
                            ], width=2),
                            dbc.Col([
                                dcc.RangeSlider(
                                    id='year-range-slider_performance',
                                    min=year_min, max=year_max,
                                    step=1,
                                    marks=year_marks,
                                    value=year_value,
                                ),
                            ])
                        ], style={'display': 'flex'}),

                        dbc.Row([
                            dbc.Col([
                                html.Div(children=[
                                    html.I(className="bi bi-calendar4-range", style={'color': '#007bff'}),
                                    html.Label("Semester", style={'padding': '5px', 'font-weight': '600'}),
                                ]),
                            ], width=2),
                            dbc.Col([
                                dcc.RangeSlider(
                                    id='semester-range-slider_performance',
                                    min=semester_min, max=semester_max,
                                    step=1,
                                    marks=semester_marks,
                                    value=semester_value
                                )
                            ])
                        ], style={'display': 'flex'}),

                        dbc.Row([
                            dbc.Col([
                                html.Div(children=[
                                    html.I(className="fa-solid fa-book", style={'color': '#007bff'}),
                                    html.Label("Course Category",
                                               style={'padding': '5px', 'font-weight': '600', 'font-size': '17px'})
                                ], className="d-inline"),

                                dcc.Dropdown(
                                    id='course-category-dpdn_performance',
                                    options=[],
                                    style={'width': '418px'}
                                )
                            ], style={'display': 'flex', 'align-items': 'center',
                                      'justify-content': 'space-evenly'}),
                            dbc.Col([
                                html.Div(children=[
                                    html.I(className="fa-solid fa-book", style={'color': '#007bff'}),
                                    html.Label("Course Type",
                                               style={'padding': '5px', 'font-weight': '600', 'font-size': '17px'})
                                ], className="d-inline"),

                                dcc.Dropdown(
                                    id='course-type-dpdn_performance',
                                    options=[],
                                    style={'width': '392px'}
                                )
                            ], style={'display': 'flex', 'align-items': 'center',
                                      'justify-content': 'space-evenly'}),
                        ]),
                    ], style={'background': '#f7fcff'}),
                    dbc.CardBody([
                        dbc.Card([
                            html.Div([html.H3('Tracking Grades')],
                                     style={'text-align': 'center', 'padding-top': '15px'}),
                            dbc.CardBody([
                                dcc.Graph(id='Graph1_performance',
                                          figure=fig1)
                            ]),
                            dbc.CardFooter([
                                html.Div(id='graph1_stats_performance')
                            ], style={
                                'background': '#f7fcff',
                                "white-space": "pre-wrap",
                                "height": "177px",
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center"
                            })
                        ], style={"width": "33.3%", "padding": "0px", "margin": "0px"}),

                        dbc.Card([
                            html.Div([html.H3('Course Categories')],
                                     style={'text-align': 'center', 'padding-top': '15px'}),
                            dbc.CardBody([
                                dcc.Graph(id='Graph2_performance', figure=fig2)
                            ]),

                            dbc.CardFooter([
                                html.Div(id='graph2_stats_performance')
                            ], style={
                                'background': '#f7fcff',
                                "white-space": "pre-wrap",
                                "height": "177px",
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center"
                            })
                        ], style={"width": "33.3%", "padding": "0px", "margin": "0px"}),

                        dbc.Card([
                            html.Div([html.H3('Tracking Semester GPA')],
                                     style={'text-align': 'center', 'padding-top': '15px'}),
                            dbc.CardBody([
                                dcc.Graph(id='Graph3-linechart', figure=fig3)
                            ]),
                            dbc.CardFooter([
                                html.Div(id='graph3_stats_performance')
                            ], style={
                                'background': '#f7fcff',
                                "white-space": "pre-wrap",
                                "height": "177px",
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center"
                            })
                        ], style={"width": "33.3%", "padding": "0px", "margin": "0px"})
                    ], style={"display": "flex", "padding": "0px"})
                ], className="Card-change-style")

            ], className='graphs-row'),
        ], md=10, lg=10, xl=10, xxl=10, style={'height': '100%'})
    ])
])


# ############################ codes For Passing ID in URL ###########################
# @callback(Output('user-id', 'children'),
#           [Input('url', 'search')],
#           [State('user-id', 'children')])
# def update_user_id(search, current_user_id):
#     # Extract the user_id value from the URL query string
#     query_dict = urllib.parse.parse_qs(search[1:])
#     user_id = query_dict.get('user_id', [None])[0]
#
#     # If the user_id has changed, return the new value, otherwise return the current value
#     if user_id != current_user_id:
#         print('bbbbb', user_id)
#         return user_id
#     else:
#         return dash.no_update


@callback(
    [
        Output('PassedHours-value', 'children'),
        Output('InProgress-value', 'children'),
        Output('Rank-value', 'children'),
        Output('Warnings-value', 'children'),
        Output('level-value', 'children'),
        Output('CGPA-value', 'children')
    ],
    Input('url', 'search'),
)
def update_student_info(search):
    # Extract the user_id value from the URL query string
    query_dict = urllib.parse.parse_qs(search[1:])
    user_id = query_dict.get('user_id', [None])[0]

    if user_id is None:
        return [dash.no_update] * 6  # Return no updates if user_id is None

    query = f"""
    SELECT StudentID, PassedHours, RankValue, HoursInProgress, WarningsNumber, CGPA, Level
    FROM student
    WHERE StudentID = '{user_id}'
    """
    results = pd.read_sql_query(query, engine)
    passed_hours_value = results.iloc[0]['PassedHours']
    hours_in_progress_value = results.iloc[0]['HoursInProgress']
    rank_value = results.iloc[0]['RankValue']
    warnings_number_value = results.iloc[0]['WarningsNumber']
    LevelValue = results.iloc[0]['Level']
    cgpa_value = results.iloc[0]['CGPA']

    return passed_hours_value, hours_in_progress_value, rank_value, warnings_number_value, LevelValue, cgpa_value


# Define the callback function to update the year range
@callback(
    [Output(component_id='year-range-slider_performance', component_property='min'),
     Output(component_id='year-range-slider_performance', component_property='max'),
     Output(component_id='year-range-slider_performance', component_property='marks'),
     Output(component_id='year-range-slider_performance', component_property='value')],
    [Input(component_id='url', component_property='search')]
)
def update_year_range(search):
    # Extract the user_id value from the URL query string
    query_dict = urllib.parse.parse_qs(search[1:])
    user_id = query_dict.get('user_id', [None])[0]

    # Modify the SQL query to include the user ID parameter
    query3 = f"""
    SELECT DISTINCT shc.Student_StudentID, shs.SGPA ,shc.Courses_CourseCode, shc.TotalMark ,shc.Grade,shc.CourseCategory, shc.CourseType,shc.AcademicYear_idAcademicYear, shp.Program_ProgramID, p.ProgramName, ay.Academic_Year_Name, ay.Semester_Name, ay.Academic_Year_INT, ay.Semester_INT
    FROM student_has_courses shc
    INNER JOIN student_has_program shp ON shc.Student_StudentID = shp.Student_StudentID
    INNER JOIN program p ON p.ProgramID = shp.Program_ProgramID
    INNER JOIN academicyear ay ON shc.AcademicYear_idAcademicYear = ay.idAcademicYear
    INNER JOIN student_has_semester shs ON shs.Student_StudentID = shc.Student_StudentID AND shs.AcademicYear_idAcademicYear = shc.AcademicYear_idAcademicYear
    where shc.Student_StudentID = '{user_id}'
    """
    results3 = pd.read_sql_query(query3, engine)
    print(results3)
    print(results3.columns)

    query2 = f"""
    SELECT *
    FROM student_has_semester shs
    INNER JOIN academicyear ay ON shs.AcademicYear_idAcademicYear = ay.idAcademicYear
    WHERE Student_StudentID = '{user_id}'
    """
    results2 = pd.read_sql_query(query2, engine)

    # Get the minimum and maximum values of the year range
    year_min = results3['Academic_Year_INT'].min()
    year_max = results3['Academic_Year_INT'].max()

    year_marks = {
        int(results2['Academic_Year_INT'].loc[i]): results2['Academic_Year_Name'].loc[i]
        for i in results2.index
    }

    # Set the initial value of the year range to be the minimum and maximum values
    year_value = [year_min, year_max]

    return year_min, year_max, year_marks, year_value


# Define the callback function to update the course type dropdown
@callback(
    [Output(component_id='course-type-dpdn_performance', component_property='options'),
     Output(component_id='course-category-dpdn_performance', component_property='options')],
    [Input(component_id='url', component_property='search')]
)
def update_course_type_options(search):
    # Extract the user_id value from the URL query string
    query_dict = urllib.parse.parse_qs(search[1:])
    user_id = query_dict.get('user_id', [None])[0]

    # Modify the SQL query to include the user ID parameter
    query3 = f"""
    SELECT DISTINCT shc.Student_StudentID, shs.SGPA ,shc.Courses_CourseCode, shc.TotalMark ,shc.Grade,shc.CourseCategory, shc.CourseType,shc.AcademicYear_idAcademicYear, shp.Program_ProgramID, p.ProgramName, ay.Academic_Year_Name, ay.Semester_Name, ay.Academic_Year_INT, ay.Semester_INT
    FROM student_has_courses shc
    INNER JOIN student_has_program shp ON shc.Student_StudentID = shp.Student_StudentID
    INNER JOIN program p ON p.ProgramID = shp.Program_ProgramID
    INNER JOIN academicyear ay ON shc.AcademicYear_idAcademicYear = ay.idAcademicYear
    INNER JOIN student_has_semester shs ON shs.Student_StudentID = shc.Student_StudentID AND shs.AcademicYear_idAcademicYear = shc.AcademicYear_idAcademicYear
    where shc.Student_StudentID = '{user_id}'
    """
    results3 = pd.read_sql_query(query3, engine)
    print(results3)
    print(results3.columns)

    # Get the unique course types for the selected course category
    course_types = sorted(results3.CourseType.astype(str).unique())
    course_categories = sorted(results3.CourseCategory.astype(str).unique())
    # Create the options list for the course type dropdown
    course_type_options = [{'label': course_type, 'value': course_type} for course_type in course_types]
    course_categories_options = [{'label': course_category, 'value': course_category} for course_category in
                                 course_categories]

    return course_type_options, course_categories_options


@callback(
    [Output(component_id='semester-range-slider_performance', component_property='min'),
     Output(component_id='semester-range-slider_performance', component_property='max'),
     Output(component_id='semester-range-slider_performance', component_property='marks'),
     Output(component_id='semester-range-slider_performance', component_property='value')],
    [Input(component_id='url', component_property='search')]
)
def update_semester_range(search):
    # Extract the user_id value from the URL query string
    query_dict = urllib.parse.parse_qs(search[1:])
    user_id = query_dict.get('user_id', [None])[0]

    # Modify the SQL query to include the user ID parameter
    query3 = f"""
    SELECT DISTINCT shc.Student_StudentID, shs.SGPA ,shc.Courses_CourseCode, shc.TotalMark ,shc.Grade,shc.CourseCategory, shc.CourseType,shc.AcademicYear_idAcademicYear, shp.Program_ProgramID, p.ProgramName, ay.Academic_Year_Name, ay.Semester_Name, ay.Academic_Year_INT, ay.Semester_INT
    FROM student_has_courses shc
    INNER JOIN student_has_program shp ON shc.Student_StudentID = shp.Student_StudentID
    INNER JOIN program p ON p.ProgramID = shp.Program_ProgramID
    INNER JOIN academicyear ay ON shc.AcademicYear_idAcademicYear = ay.idAcademicYear
    INNER JOIN student_has_semester shs ON shs.Student_StudentID = shc.Student_StudentID AND shs.AcademicYear_idAcademicYear = shc.AcademicYear_idAcademicYear
    where shc.Student_StudentID = '{user_id}'
    """
    results3 = pd.read_sql_query(query3, engine)
    print(results3)
    print(results3.columns)

    query2 = f"""
    SELECT *
    FROM student_has_semester shs
    INNER JOIN academicyear ay ON shs.AcademicYear_idAcademicYear = ay.idAcademicYear
    WHERE Student_StudentID = '{user_id}'
    """
    results2 = pd.read_sql_query(query2, engine)

    # Get the minimum and maximum values of the semester range
    semester_min = results3['Semester_INT'].min()
    semester_max = results3['Semester_INT'].max()

    # Create the marks dictionary for the semester range
    semester_marks = {
        int(results2['Semester_INT'].loc[i]): results2['Semester_Name'].loc[i]
        for i in results2.index
    }
    # Set the initial value of the semester range to be the minimum and maximum values
    semester_value = [semester_min, semester_max]

    return semester_min, semester_max, semester_marks, semester_value


@callback(
    [
        Output(component_id='Graph1_performance', component_property='figure'),
        Output(component_id='Graph2_performance', component_property='figure'),
        Output(component_id='Graph3-linechart', component_property='figure'),
        Output(component_id='graph1_stats_performance', component_property='children'),
        Output(component_id='graph2_stats_performance', component_property='children'),
        Output(component_id='graph3_stats_performance', component_property='children'),
    ],
    [
        Input(component_id='year-range-slider_performance', component_property='value'),
        Input(component_id='semester-range-slider_performance', component_property='value'),
        Input(component_id='course-category-dpdn_performance', component_property='value'),
        Input(component_id='course-type-dpdn_performance', component_property='value'),
        State(component_id='url', component_property='search')
    ]
)
def update_Graphs(year_range, semester_range, course_category_value, course_type_value, search):
    # Extract the user_id value from the URL query string
    query_dict = urllib.parse.parse_qs(search[1:])
    user_id = query_dict.get('user_id', [None])[0]

    if user_id is None:
        return [dash.no_update] * 6  # Return no updates if user_id is None

    query3 = f"""
    SELECT DISTINCT shc.Student_StudentID, shs.SGPA ,shc.Courses_CourseCode, shc.TotalMark ,shc.Grade,shc.CourseCategory, shc.CourseType,shc.AcademicYear_idAcademicYear, shp.Program_ProgramID, p.ProgramName, ay.Academic_Year_Name, ay.Semester_Name, ay.Academic_Year_INT, ay.Semester_INT
    FROM student_has_courses shc
    INNER JOIN student_has_program shp ON shc.Student_StudentID = shp.Student_StudentID
    INNER JOIN program p ON p.ProgramID = shp.Program_ProgramID
    INNER JOIN academicyear ay ON shc.AcademicYear_idAcademicYear = ay.idAcademicYear
    INNER JOIN student_has_semester shs ON shs.Student_StudentID = shc.Student_StudentID AND shs.AcademicYear_idAcademicYear = shc.AcademicYear_idAcademicYear
    where shc.Student_StudentID = '{user_id}'
    """
    results3 = pd.read_sql_query(query3, engine)
    print(results3)
    print(results3.columns)

    Student_Query_data = f"""
    SELECT DISTINCT shc.Student_StudentID, shs.SGPA ,shc.Courses_CourseCode, shc.TotalMark ,shc.Grade,shc.AcademicYear_idAcademicYear, ay.Academic_Year_Name, ay.Semester_Name
    FROM student_has_courses shc
    INNER JOIN student_has_program shp ON shc.Student_StudentID = shp.Student_StudentID
    INNER JOIN program p ON p.ProgramID = shp.Program_ProgramID
    INNER JOIN academicyear ay ON shc.AcademicYear_idAcademicYear = ay.idAcademicYear
    INNER JOIN student_has_semester shs ON shs.Student_StudentID = shc.Student_StudentID AND shs.AcademicYear_idAcademicYear = shc.AcademicYear_idAcademicYear
    where shc.Student_StudentID = '{user_id}' AND Semester_Name != "summer"
    """
    student_data = pd.read_sql_query(Student_Query_data, engine)

    ########### Special Data Frame For The First Graph to be affected only by Year and Semester Filters ###################
    dfe2 = results3[(results3['Academic_Year_INT'] >= year_range[0]) &
                    (results3['Academic_Year_INT'] <= year_range[1])]

    dfe2 = dfe2[(dfe2['Semester_INT'] >= semester_range[0]) &
                (dfe2['Semester_INT'] <= semester_range[1])]

    if course_category_value:
        dfe2 = dfe2[dfe2['CourseCategory'] == course_category_value]

    if course_type_value:
        dfe2 = dfe2[dfe2['CourseType'] == course_type_value]

    ############ Special Data Frame For The Third Graph to be affected only by Year and Semester Filters ###################

    dfe2_For_3Graph = results3[(results3['Academic_Year_INT'] >= year_range[0]) &
                               (results3['Academic_Year_INT'] <= year_range[1])]

    dfe2_For_3Graph = dfe2_For_3Graph[(dfe2_For_3Graph['Semester_INT'] >= semester_range[0]) &
                                      (dfe2_For_3Graph['Semester_INT'] <= semester_range[1])]
    count_course_of_each_sem = results3.groupby(['AcademicYear_idAcademicYear', 'SGPA'])[
        'Courses_CourseCode'].count().reset_index()
    print(count_course_of_each_sem)
    dfe2_subset = dfe2_For_3Graph[[
        'Academic_Year_INT',
        'Semester_INT',
        'SGPA',
        'Semester_Name',
        'Academic_Year_Name',
        'AcademicYear_idAcademicYear'
    ]].drop_duplicates().sort_values(by=['Academic_Year_INT', 'Semester_INT'])

    dfe2_subset = dfe2_subset.merge(count_course_of_each_sem, on=['AcademicYear_idAcademicYear', 'SGPA'], how='left')

    dfe2_subset = dfe2_subset.dropna()

    dfe2_subset['New_Index'] = range(1, len(dfe2_subset) + 1)

    print(dfe2_subset)
    merged_list = dfe2_subset.apply(lambda row: row['Academic_Year_Name'] + ' ' + row['Semester_Name'], axis=1).tolist()
    print(merged_list)
    # #######################################################################################################################
    # ########################## For Second Graph ###########################
    dfe2_For_2Graph = results3[(results3['Academic_Year_INT'] >= year_range[0]) &
                               (results3['Academic_Year_INT'] <= year_range[1])]

    dfe2_For_2Graph = dfe2_For_2Graph[(dfe2_For_2Graph['Semester_INT'] >= semester_range[0]) &
                                      (dfe2_For_2Graph['Semester_INT'] <= semester_range[1])]

    if course_type_value:
        dfe2_For_2Graph = dfe2_For_2Graph[dfe2_For_2Graph['CourseType'] == course_type_value]

    fig1 = px.sunburst(dfe2, path=['Grade', 'Courses_CourseCode'], color='Grade',
                       color_discrete_map={
                           'A': 'rgb(99, 110, 250)',
                           'A-': 'rgb(25, 211, 243)',
                           'B+': 'rgb(230, 25, 110)',
                           'B': 'rgb(245 192 207)',
                           'C+': 'rgb(142, 27, 201, 89%)',
                           'C': 'rgb(199, 90, 255, 62%)',
                           'D': 'rgb(0, 204, 150)',
                           'P': 'rgb(182, 232, 128)',
                           'F': 'red'
                       },
                       )
    fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    # Define the numeric values for the letter grades
    grade_values = {
        "A": 5,
        "A-": 4.5,
        "B+": 4,
        "B": 3.5,
        "C+": 3,
        "C": 2.5,
        "D": 2,
        "F": 1,
        "P": np.nan
    }

    # Define the letter grades for the numeric values
    value_grades = {
        5: "A",
        4.5: "A-",
        4: "B+",
        3.5: "B",
        3: "C+",
        2.5: "C",
        2: "D",
        1: "F",
        np.nan: "P"
    }

    # # Define the colors for each grade
    color_map = {
        "A": "rgb(99, 110, 250)",
        "A-": "rgb(25, 211, 243)",
        "B+": "rgb(230, 25, 110)",
        "B": "rgb(245, 192, 207)",
        "C+": "rgba(142, 27, 201, 0.89)",
        "C": "rgba(199, 90, 255, 0.62)",
        "D": "rgb(0, 204, 150)",
        "P": "rgb(182, 232, 128)",
        "F": "red",
    }

    fig2 = px.box(dfe2_For_2Graph, x="CourseCategory", y="TotalMark", color="CourseCategory")
    fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                       plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       )

    fig3 = go.Figure(
        data=[go.Scatter(x=dfe2_subset['New_Index'],
                         y=dfe2_subset['SGPA'],
                         text='number of courses: ' + dfe2_subset['Courses_CourseCode'].astype(str)
                         )],
        layout=go.Layout(
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis={
                'tickvals': [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0],  # Set the tick values in order
                'range': [0, 4.0]  # Set the y-axis range to a fixed range
            },
            xaxis={
                'tickvals': dfe2_subset['New_Index'].values,
                'ticktext': merged_list
            }
        )
    )

    print(dfe2['Grade'])
    # Calculate statistical analysis and conclusion for Graph 1
    graph1_stats = calculate_stats_mode(dfe2['Grade'])
    print(graph1_stats)
    # graph1_conclusion = calculate_conclusion(graph1_stats)

    # Calculate statistical analysis and conclusion for Graph 2
    graph2_stats = perform_course_category_analysis(dfe2_For_2Graph)
    print(graph2_stats)
    # graph2_conclusion = calculate_conclusion(graph2_stats)

    graph3_stats = perform_semester_type_analysis(results3) + "\n" + studying_courses_in_not_same_ay(student_data)
    return fig1, fig2, fig3, graph1_stats, graph2_stats, graph3_stats
