import dash
import pandas as pd
from dash import Dash, html, dcc, Input, Output, callback, ctx, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import plotly.express as px
import numpy as np
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
import dash_extensions as de
import plotly.graph_objects as go
import plotly.colors as colors

import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy import text

# Create a connection to the MySQL database
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    database="mydb"
)
engine = create_engine(f'mysql+mysqlconnector://root@127.0.0.1:3306/mydb')

hello_url = "https://assets7.lottiefiles.com/packages/lf20_tvitrmm4.json"
options = dict(loop=True, autoplay=True, renderSettings=dict(preserveAspectRatio='xMidYMid slice'))

########################################################################################################################
# Define Sidebar
sidebar = dbc.Nav(
    children=[
        dbc.NavLink(
            [
                html.I(className="fa-solid fa-chart-simple", style={'color': 'rgb(89, 141, 188'}),
                html.Div("Performance", className="ms-2 text-black-50 d-inline", style={'font-weight': '600'}),
            ],
            href='/project/home/pages/pg1',
            active="exact",
        ),
        dbc.NavLink(
            [
                html.I(className="bi bi-door-closed-fill", style={'color': 'rgb(89, 141, 188'}),
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
        'width': '171px',
        'display': 'flex',
        'flex-direction': 'column'
    }
)
sidebar.children[-1].style = {'order': '1', 'margin-top': '660px', 'font-size': '17px'}


########################################################################################################################

########################################################################################################################
# Queries

############################################################################################
############################################################################################

# Query1: To get All Courses with doctor, year, semester, Grade,
Courses_list_Query = """
    SELECT distinct shc.Courses_CourseCode, shc.Grade, s.CGPA, s.ProgramName ,shc.TotalMark, d.DoctorName, ay.idAcademicYear, ay.Academic_Year_INT, ay.Academic_Year_Name, ay.Semester_INT, ay.Semester_Name, ay.AcademicYearSemester
    FROM student_has_courses shc
    INNER JOIN student s ON shc.Student_StudentID = s.StudentID
    INNER JOIN doctor_teach_courses dtc ON shc.AcademicYear_idAcademicYear = dtc.AcademicYear_idAcademicYear and shc.Courses_CourseCode = dtc.Courses_CourseCode
    INNER JOIN doctor d ON dtc.Doctor_idDoctor = d.idDoctor
    INNER JOIN academicyear ay ON shc.AcademicYear_idAcademicYear = ay.idAcademicYear
"""
dfb = pd.read_sql_query(Courses_list_Query, engine)
Courses_list = pd.read_sql_query(Courses_list_Query, engine)
Courses_list = Courses_list.dropna()
print(Courses_list)
print(Courses_list.columns)


# define a function to calculate the success and failure percentages
def calculate_success_failure_count(series):
    series = series.astype(str)
    success_grades = ['A', 'A-', 'B+', 'B', 'C+', 'C', 'D', 'P']
    success_count = series.isin(success_grades).sum()
    failure_count = len(series) - success_count
    total_count = len(series)
    success_percentage = success_count / total_count * 100
    failure_percentage = failure_count / total_count * 100

    return success_percentage, failure_percentage, total_count


# group the dataframe by Yearid, CourseCode, and DoctorName, and calculate the success and failure percentages and count of each group
grouped_df = Courses_list.groupby(['idAcademicYear', 'Courses_CourseCode', 'DoctorName', 'AcademicYearSemester'])[
    'Grade'].agg(calculate_success_failure_count).reset_index()

# extract the success percentage, failure percentage, and total count columns from the resulting dataframe
grouped_df[['Success Percentage', 'Failure Percentage', 'Total Count']] = pd.DataFrame(grouped_df['Grade'].tolist(),
                                                                                       index=grouped_df.index)

# drop the original Grade column
grouped_df = grouped_df.drop('Grade', axis=1)
print(grouped_df)


# Query2:
#######################################################################################################################
# Create a scatter plot using Plotly
fig_scatter = go.Figure()
for course in grouped_df['Courses_CourseCode'].unique():
    fig_scatter.add_trace(go.Scatter(x=grouped_df[grouped_df['Courses_CourseCode'] == course]['AcademicYearSemester'],
                                     y=grouped_df[grouped_df['Courses_CourseCode'] == course]['Success Percentage'],
                                     name=course,
                                     mode='markers',
                                     marker=dict(size=10)))
# Customize the scatter plot
fig_scatter.update_layout(
    xaxis_title='Academic Semester',
    yaxis_title='Success Percentage (%)',
    font=dict(size=12))
#####################################################################
# Create a bar chart showing the Average success percentage for each course
fig_bar_course = go.Figure()
for course in grouped_df['Courses_CourseCode'].unique():
    fig_bar_course.add_trace(go.Bar(x=[course],
                                    y=grouped_df[grouped_df['Courses_CourseCode'] == course]['Success Percentage'],
                                    name=course,
                                    marker=dict(color='#1f77b4')))

# Customize the bar chart
fig_bar_course.update_layout(
    xaxis_title='Course',
    yaxis_title='Success Percentage',
    font=dict(size=12))
#####################################################################
# fig_sunburst_new = px.sunburst()
# Create the initial sunburst chart
fig_sunburst_initial = px.sunburst(
    pd.DataFrame(),
)

cgpa_histogram_initial = px.histogram(pd.DataFrame(), title="Cumulative GPA")
####################################################################

# Create a dropdown menu with multi-select options to filter the courses displayed on the scatter plot
dropdown_options = [{'label': course, 'value': course} for course in grouped_df['Courses_CourseCode'].unique()]

dropdown_menu = dcc.Dropdown(id='course-dropdown',
                             options=dropdown_options,
                             value=['COMP 307', 'COMP 207'],
                             multi=True)
# Create a Dash app to display the charts and link them together
# dash.register_page(__name__, path='/', name='Decision Maker')  # '/' is home page
layout4 = html.Div([
    dbc.Row([
        dbc.Col([
            sidebar
        ], xs=4, sm=4, md=1, lg=2, xl=2, xxl=2),
        dbc.Col([
            dbc.Row([
                dbc.Row([
                    html.Div(children=[
                        html.I(className="fa-solid fa-book", style={'color': '#598dbc'}),
                        html.Label("Courses", style={'padding': '5px', 'font-weight': '600'})
                    ], className="d-inline"),

                    dropdown_menu
                ], style={'margin-bottom': '16px'}),

                dbc.Row([
                    dbc.Card([
                        dbc.CardHeader([
                            html.I(className="bi bi-graph-up-arrow",
                                   style={
                                       'color': 'white',
                                       'font-size': '18px'}
                                   ),
                            html.Label("Tracking Success Rates of Many Courses ", style={
                                'padding-left': '10px',
                                'font-weight': '600',
                                'color': 'white'
                            })
                        ], style={'background': '#598dbc'}),
                        dbc.CardBody([
                            html.Div(children=[
                                html.Div(id='graphs-section', children=[
                                    dcc.Graph(id='scatter-plot', figure=fig_scatter,
                                              style={'width': '100%', 'height': '485px', 'padding-top': '22px'})
                                ])
                            ], style={'margin-bottom': '20px'})
                        ], style={'padding': '0px'}),
                    ], style={'width': '50%', "padding": "0px", 'border-radius': '0'}),

                    dbc.Card([
                        dbc.CardHeader([
                            html.I(className="bi bi-graph-down-arrow",
                                   style={
                                       'color': 'white',
                                       'font-size': '18px'}
                                   ),
                            html.Label("Average Success Percentage by Course", style={'padding-left': '10px',
                                                                                      'font-weight': '600',
                                                                                      'color': 'white'
                                                                                      }),
                        ], style={'background': '#598dbc'}),
                        dbc.CardBody([
                            dcc.Graph(id='bar-chart', figure=fig_scatter)
                        ], style={'padding': '0px'}),
                    ], style={'width': '50%', "padding": "0px", 'border-radius': '0'}),
                ]),

                dbc.Row([
                    dbc.Card([
                        dbc.CardHeader([
                            html.I(className="bi bi-pie-chart-fill",
                                   style={
                                       'color': 'white',
                                       'font-size': '18px'
                                   }),
                            html.Label("Students Grades", style={'padding-left': '10px',
                                                                 'font-weight': '600',
                                                                 'color': 'white'
                                                                 })
                        ], style={'background': '#598dbc'}),
                        dbc.CardBody([
                            dcc.Graph(id='sunburst_course', figure=fig_sunburst_initial)
                        ], style={'padding': '0px'}),

                    ], style={'width': '50%', "padding": "0px", 'border-radius': '0'}),

                    dbc.Card([
                        dbc.CardHeader([
                            html.I(className="bi bi-bar-chart-fill",
                                   style={
                                       'color': 'white',
                                       'font-size': '18px'
                                   }),
                            html.Label("Student Cumulative GPA", style={'padding-left': '10px',
                                                                        'font-weight': '600',
                                                                        'color': 'white'
                                                                        })
                        ], style={'background': '#598dbc'}),
                        dbc.CardBody([
                            dcc.Graph(id='CGPA-histo', figure=cgpa_histogram_initial)
                        ], style={'padding': '0px'}),
                    ], style={'width': '50%', "padding": "0px", 'border-radius': '0'}),

                ], style={'padding-top': '9px'}),
                dcc.Store(id='df-filtered'),
                dcc.Store(id='colors_list')
            ])
        ])
    ])
])

x_tickvals = []
x_ticktext = []
# Define an empty dataframe to store the filtered data
df_filtered = pd.DataFrame()

course_colors = {}


# @callback(
#     Output('hidden_div_for_logout-decision-maker', 'children'),
#     Input('logout-button-decision-maker', 'n_clicks')
# )
# def logout(n_clicks):
#     if n_clicks == 0:
#         return ""
#     else:
#         return dcc.Location(pathname="/", id='url', refresh=False)


# Define a callback function to update the scatter plot based on the selected courses
@callback(
    [Output('scatter-plot', 'figure'),
     Output('bar-chart', 'figure'),
     Output('df-filtered', 'data'),
     Output('colors_list', 'data')],
    [Input('course-dropdown', 'value')])
def update_scatter_plot(selected_courses):
    # Use the global df_filtered dataframe
    global df_filtered
    # Filter the dataframe based on the selected courses
    color_palette = colors.qualitative.Dark24
    color_map = dict(zip(selected_courses, color_palette[:len(selected_courses)]))
    df_filtered = grouped_df[grouped_df['Courses_CourseCode'].isin(selected_courses)]
    print(df_filtered)

    fig_scatter_new = go.Figure()
    for course in selected_courses:
        df_filtered_course = df_filtered[df_filtered['Courses_CourseCode'] == course]
        print(df_filtered_course)
        x_tickvals.extend(df_filtered_course['idAcademicYear'].values)
        x_ticktext.extend(df_filtered_course['AcademicYearSemester'].values)
        fig_scatter_new.add_trace(
            go.Scatter(x=df_filtered_course['idAcademicYear'],
                       y=df_filtered_course[df_filtered_course['Courses_CourseCode'] == course]['Success Percentage'],
                       mode='markers',
                       name=course,
                       marker=dict(
                           size=15,
                           opacity=0.5,
                           color=color_map[course],
                           line=dict(width=1, color=color_map[course])

                       ),
                       customdata=df_filtered_course[df_filtered_course['Courses_CourseCode'] == course]['DoctorName'],
                       hovertemplate=(
                               '<b>Year:</b> %{x}<br>' +
                               '<b>Success Percentage:</b> %{y:.2f}%<br>' +
                               '<b>Doctor Name:</b> %{customdata}<br>'
                       )
                       )
        )
        course_colors[course] = color_map[course]
        print(course_colors)

    # Update the course_colors dictionary
    # Update the course_colors dictionary
    for course in course_colors.copy():
        if course not in selected_courses:
            del course_colors[course]
    course_colors.update(color_map)  # Customize the scatter plot
    fig_scatter_new.update_layout(
        xaxis_title='Academic Semester',
        yaxis_title='Success Percentage (%)',
        font=dict(size=12),
        xaxis={
            'tickvals': x_tickvals,
            'ticktext': x_ticktext
        },
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    df_avg_success_rate = df_filtered.groupby('Courses_CourseCode')['Success Percentage'].mean().reset_index()

    # Rename the columns of the resulting DataFrame
    df_avg_success_rate = df_avg_success_rate.rename(
        columns={'Success Percentage': 'Average Success Percentage'})
    # print("SSAAA", df_avg_success_rate)

    fig_bar_course_new = go.Figure(
        go.Bar(x=df_avg_success_rate['Courses_CourseCode'],
               y=df_avg_success_rate['Average Success Percentage'],
               marker=dict(
                   color=[color_map[course] for course in df_avg_success_rate['Courses_CourseCode']],
                   line=dict(width=1, color='black')
               ),
               text=df_avg_success_rate['Average Success Percentage'],
               texttemplate='%{text:.2f}%',
               textposition='auto')
    )
    # Customize the bar chart
    fig_bar_course_new.update_layout(
        xaxis_title='Course',
        yaxis_title='Success Percentage',
        font=dict(size=12))
    fig_bar_course_new.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                                     plot_bgcolor='rgba(0,0,0,0)',
                                     paper_bgcolor='rgba(0,0,0,0)', )

    # Return the new scatter plot
    return fig_scatter_new, fig_bar_course_new, df_filtered.to_json(date_format='iso', orient='split'), course_colors


@callback(
    [
        Output('sunburst_course', 'figure'),
        Output('CGPA-histo', 'figure')
    ],
    [Input('scatter-plot', 'clickData')],
    [State('sunburst_course', 'figure'),
     State('df-filtered', 'data'),
     State('scatter-plot', 'figure'),
     State('colors_list', 'data')
     ]
)
def update_sunburst(clickData, sunburst_course, df_filtered_json, scatter_fig, course_colors):
    if not clickData:
        return sunburst_course, {}

    # Extract the dataframe from the JSON string
    df_filtered = pd.read_json(df_filtered_json, orient='split')
    year = clickData['points'][0]['x']

    curve_num = clickData['points'][0]['curveNumber']
    color = scatter_fig['data'][curve_num]['marker']['color']
    course = None
    for key, value in course_colors.items():
        if value == color:
            course = key
            break

    if course is not None:
        course_index = list(df_filtered['Courses_CourseCode'].unique()).index(course)
    else:
        course_index = None

    if course_index is not None:
        course_name = df_filtered['Courses_CourseCode'].unique()[course_index]
        print(course_name)
    else:
        print("No matching course found.")

    # create a filtered dataframe for the selected year and course
    df_filtered = Courses_list[
        (Courses_list['idAcademicYear'] == year) & (Courses_list['Courses_CourseCode'] == course_name)]

    # Get the academic year and semester corresponding to year
    academic_year_semester = Courses_list.loc[Courses_list['idAcademicYear'] == year, 'AcademicYearSemester'].iloc[0]

    # create a new sunburst chart showing the distribution of course grades and programs
    fig_sunburst_new = px.sunburst(
        df_filtered,
        path=['ProgramName', 'Grade'],
        title='Distribution of Programs for {} in {}'.format(course_name, academic_year_semester),
    )
    fig_sunburst_new.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)', )

    # create a histogram of CGPA for the selected year and course
    fig_histogram = px.histogram(
        df_filtered,
        x='CGPA',
        nbins=3,
        title='Distribution of Students CGPA for {} in {}'.format(course_name, academic_year_semester),

        range_x=[0, 4],  # set the x-axis range to be constant
        histnorm='percent'
    )
    fig_histogram.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)', )
    # fig_histogram.update_yaxes(tickprefix="%")

    return fig_sunburst_new, fig_histogram