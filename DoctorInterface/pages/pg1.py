# Dash Libraries
import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_extensions as de
import plotly.express as px
import plotly.graph_objects as go

# Pandas Library
import pandas as pd

# Numpy Library
import numpy as np

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

# DoctorID = ""

############################################################################################

# Query 1: To Get Doctor ID And Doctor Name
Query1 = """
    SELECT idDoctor, DoctorName FROM doctor
    WHERE idDoctor = 4471
"""

Query1_result = pd.read_sql_query(Query1, engine)
DoctorName = Query1_result.iloc[0]['DoctorName']
print(DoctorName)
############################################################################################


############################################################################################

# Query 2: For First DropDown To get Courses That Doctor usually Teach
Query2 = """
    SELECT dtc.Courses_CourseCode, d.DoctorName
    FROM doctor d
    INNER JOIN doctor_teach_courses dtc ON idDoctor = Doctor_idDoctor
    WHERE idDoctor = 4471
"""
Query2_result = pd.read_sql_query(Query2, engine)
print(Query2_result)
############################################################################################


############################################################################################
# Queries 3 : For The Second DropDown To get The Courses before it
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
############################################################################################

sidebar = dbc.Nav(
    children=[
        dbc.NavLink(
            [
                html.I(className="bi bi-graph-down-arrow", style={'color': 'rgb(99 21 167)'}),
                html.Div("Taught Courses", className="ms-2 text-black-50 d-inline", style={'font-weight': '600', 'color': 'rgb(225 18 133)'}),
            ],
            href='/DoctorInterface/home/pages/pg1',
            active="exact",
        ),
        dbc.NavLink(
            [
                html.I(className="fa-solid fa-chart-simple", style={'color': 'rgb(99 21 167)'}),
                html.Div("Tracking", className="ms-2 text-black-50 d-inline",
                         style={'font-weight': '600', 'color': 'rgb(225 18 133)'}),
            ],
            href='/DoctorInterface/home/pages/pg2',
            active="exact",
        ),
        dbc.NavLink(
            [
                html.I(className="bi bi-door-closed-fill", style={'color': 'rgb(99 21 167)'}),
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

sidebar.children[-1].style = {'order': '1','margin-top': '608px', 'font-size': '19px', 'color': 'rgb(99 21 167)'}

# @callback([Output('welcome-msg', 'children')],
# Input('url', 'search')
#           )
# def update_student_info(search):
# # Extract the user_id value from the URL query string
# query_dict = urllib.parse.parse_qs(search[1:])
# user_id = query_dict.get('user_id', [None])[0]
#
#
# if user_id is None:
#     return [dash.no_update] * 6  # Return no updates if user_id is None
#
# # Query 1: To Get Doctor ID And Doctor Name
# Query1 = f"""
#     SELECT idDoctor, DoctorName FROM doctor
#     WHERE idDoctor = '{user_id}'
# """
#
# Query1_result = pd.read_sql_query(Query1, engine)
# DoctorName = Query1_result.iloc[0]['DoctorName']
# welcome_msg = f"Welcome Back, Dr/ {DoctorName}"
#
# return welcome_msg
# dash.register_page(__name__, path='/', name='Home')  # '/' is home page

df2 = px.data.tips()
fig1 = px.sunburst()
fig2 = px.sunburst()
fig3 = px.sunburst()
fig4 = px.sunburst()

layout3 = html.Div([
    dbc.Row([
        dbc.Col([
            sidebar
        ], xs=4, sm=4, md=1, lg=2, xl=2, xxl=2),
        dbc.Col([
            dbc.Row([
                html.Div(de.Lottie(options=options, width="12%", height="25%", url=hello_url),
                         style={'width': '50%', 'float': 'left'}),
                html.H6(f"Welcome Back, Dr/ {DoctorName}",
                        style={'width': '50%', 'float': 'left', 'font-size': '22px', 'font-weight': '600',
                               'color': '#fff'})
            ], style={'width': '106%',
                      'display': 'flex',
                      'flex-direction': 'column',
                      'background': 'rgb(99 21 167)',
                      'height': '61px',
                      'border-radius': '2px',
                      'align-items': 'center',
                      'justify-content': 'center'
                      }),
            dbc.Row([
                dbc.Col([
                    html.Div(children=[
                        html.Div(id='graphs-section', children=[
                            dcc.Graph(id='Graph1',
                                      style={'width': '721px', 'height': '370px',
                                             'box-shadow': 'rgb(99 21 167) -33px 34px 12px -37px'})
                        ])
                    ], style={'margin-bottom': '20px'})
                ], md=7, lg=7, xl=7, xxl=7, style={'height': '100%', 'margin': '-24px 61px 17px -20px'}),

                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.Div(children=[
                                html.I(className="fa-solid fa-book", style={'color': 'rgb(99 21 167)'}),
                                html.Label("Student Registered in", style={'padding': '5px', 'font-weight': '600'})
                            ], className="d-inline"),

                            dcc.Dropdown(
                                id='filter-dpdn1',
                                value="MATH 104",
                                options=[{'label': x, 'value': x} for x in
                                         sorted(Query2_result.Courses_CourseCode.astype(str).unique())],
                            ),
                        ], style={'height': '100%', 'margin-bottom': '33px', 'margin-top': '10px'}),
                    ]),

                    dbc.Row([
                        dbc.Col([
                            html.Div(children=[
                                html.I(className="fa-solid fa-book", style={'color': 'rgb(99 21 167)'}),
                                html.Label("Prerequest Course", style={'padding': '5px', 'font-weight': '600'})
                            ], className="d-inline"),

                            dcc.Dropdown(
                                id='filter-dpdn2',
                                options=[]
                            ),
                        ], style={'height': '100%'}),

                        html.Div(id='num_got_F', style={'padding-top': '20px',
                                                        'font-size': '17px',
                                                        'font-weight': '600'})
                    ]),
                ])
            ]),

            dbc.Row([
                dbc.Card([
                    dbc.CardHeader([
                        html.Label("Level ", style={'font-weight': '600', 'color': 'white', 'padding': '10px'}),
                        html.I(className="bi bi-1-circle-fill", style={'color': 'white'})
                    ], style={'background': 'rgb(99 21 167)'}),
                    dbc.CardBody([
                        dcc.Graph(id='my_pie1', figure=fig1)
                    ], style={'padding': '0px'}),

                    dbc.CardFooter([
                        html.Div(id='pie1_stats')
                    ], style={'background': 'none'}),
                ], id='card-1', style={'width': '25%'}),

                dbc.Card([
                    dbc.CardHeader([
                        html.Label("Level ", style={'font-weight': '600', 'color': 'white', 'padding': '10px'}),
                        html.I(className="bi bi-2-circle-fill", style={'color': 'white'})
                    ], style={'background': 'rgb(99 21 167)'}),
                    dbc.CardBody([
                        dcc.Graph(id='my_pie2', figure=fig2)
                    ], style={'padding': '0px'}),

                    dbc.CardFooter([
                        html.Div(id='pie2_stats')
                    ], style={'background': 'none'}),
                ], id='card-2', style={'width': '25%'}),

                dbc.Card([
                    dbc.CardHeader([
                        html.Label("Level ", style={'font-weight': '600', 'color': 'white', 'padding': '10px'}),
                        html.I(className="bi bi-3-circle-fill", style={'color': 'white'})
                    ], style={'background': 'rgb(99 21 167)'}),
                    dbc.CardBody([
                        dcc.Graph(id='my_pie3', figure=fig3)
                    ], style={'padding': '0px'}),

                    dbc.CardFooter([
                        html.Div(id='pie3_stats')
                    ], style={'background': 'none'}),
                ], id='card-3', style={'width': '25%'}),

                dbc.Card([
                    dbc.CardHeader([
                        html.Label("Level ", style={'font-weight': '600', 'color': 'white', 'padding': '10px'}),
                        html.I(className="bi bi-4-circle-fill", style={'color': 'white'})
                    ], style={'background': 'rgb(99 21 167)'}),
                    dbc.CardBody([
                        dcc.Graph(id='my_pie4', figure=fig4)
                    ], style={'padding': '0px'}),

                    dbc.CardFooter([
                        html.Div(id='pie4_stats')
                    ], style={'background': 'none'}),
                ], id='card-4', style={'width': '25%'}),
            ], style={'width': '100%', 'display': 'flex', 'margin-bottom': '20px',
                      'box-shadow': 'rgb(224, 72, 170) 2px 2px 14px -5px'})
        ])
    ]),
])

# @callback(
#     Output('hidden_div_for_logout_doctor', 'children'),
#     Input('logout-button-doctor', 'n_clicks')
# )
# def logout(n_clicks):
#     if n_clicks == 0:
#         return ""
#     else:
#         return dcc.Location(pathname="/", id='url', refresh=False)

# Call back For Second DropDown
@callback(
    [Output(component_id='filter-dpdn2', component_property="options")],
    [Input(component_id='filter-dpdn1', component_property="value")]
)
def update_Sec_DPDN(CourseCode_To_Check):
    if CourseCode_To_Check is None:
        return [[]]

    if CourseCode_To_Check in level1Courses_autumn['CourseCode'].values:
        result = level1Courses_spring
        return [[{'label': option, 'value': option} for option in result['CourseCode']]]

    elif CourseCode_To_Check in level2Courses_spring['CourseCode'].values:
        result = pd.concat([level1Courses_spring, level1Courses_autumn])
        return [[{'label': option, 'value': option} for option in result['CourseCode']]]

    elif CourseCode_To_Check in level2Courses_autumn['CourseCode'].values:
        result = pd.concat([level1Courses_spring, level1Courses_autumn, level2Courses_spring])
        return [[{'label': option, 'value': option} for option in result['CourseCode']]]

    elif CourseCode_To_Check in level3Courses_spring['CourseCode'].values:
        result = pd.concat([level1Courses_spring, level1Courses_autumn, level2Courses_spring, level2Courses_autumn])
        return [[{'label': option, 'value': option} for option in result['CourseCode']]]

    elif CourseCode_To_Check in level3Courses_autumn['CourseCode'].values:
        result = pd.concat([level1Courses_spring, level1Courses_autumn, level2Courses_spring, level2Courses_autumn,
                            level3Courses_spring])
        return [[{'label': option, 'value': option} for option in result['CourseCode']]]

    elif CourseCode_To_Check in level4Courses_spring['CourseCode'].values:
        result = pd.concat([level1Courses_spring, level1Courses_autumn, level2Courses_spring, level2Courses_autumn,
                            level3Courses_spring, level3Courses_autumn])
        return [[{'label': option, 'value': option} for option in result['CourseCode']]]

    elif CourseCode_To_Check in level4Courses_autumn['CourseCode'].values:
        result = pd.concat([level1Courses_spring, level1Courses_autumn, level2Courses_spring, level2Courses_autumn,
                            level3Courses_spring, level3Courses_autumn, level4Courses_spring])
        return [[{'label': option, 'value': option} for option in result['CourseCode']]]

@callback(
    [Output(component_id="Graph1", component_property="figure"),
     Output(component_id="my_pie1", component_property="figure"),
     Output(component_id="my_pie2", component_property="figure"),
     Output(component_id="my_pie3", component_property="figure"),
     Output(component_id="my_pie4", component_property="figure"),
     Output(component_id="num_got_F", component_property="children")],
    [Input(component_id="filter-dpdn1", component_property="value"),
     Input(component_id="filter-dpdn2", component_property="value")],
)
def update_graph1(RegisteredCourse, FilterByCourse):
    if RegisteredCourse is None:
        return [[]]

    # Query 4: For The Graph

    Query4 = f"""SELECT shc.Courses_CourseCode, shc.Grade, s.Level, s.ProgramName, shc.AcademicYear_idAcademicYear, d.DoctorName
        FROM student_has_courses shc
        INNER JOIN student s ON s.StudentID = shc.Student_StudentID
        INNER JOIN doctor_teach_courses dtc ON shc.AcademicYear_idAcademicYear= dtc.AcademicYear_idAcademicYear AND shc.Courses_CourseCode = dtc.Courses_CourseCode
        INNER JOIN doctor d ON dtc.Doctor_idDoctor = d.idDoctor
        WHERE shc.Courses_CourseCode = "{FilterByCourse}"  AND shc.Grade != 'F'
        AND shc.Student_StudentID IN (SELECT shc.Student_StudentID
                                        FROM student_has_courses shc
                                        WHERE shc.Courses_CourseCode = "{RegisteredCourse}")
    """
    Query4_result = pd.read_sql_query(Query4, engine)
    print(Query4)
    print(Query4_result)

    Query_student_get_F = f"""
    SELECT shc.Courses_CourseCode, shc.Grade, s.Level, s.ProgramName, shc.AcademicYear_idAcademicYear, d.DoctorName
            FROM student_has_courses shc
            INNER JOIN student s ON s.StudentID = shc.Student_StudentID
            INNER JOIN doctor_teach_courses dtc ON shc.AcademicYear_idAcademicYear= dtc.AcademicYear_idAcademicYear AND shc.Courses_CourseCode = dtc.Courses_CourseCode
            INNER JOIN doctor d ON dtc.Doctor_idDoctor = d.idDoctor
            WHERE shc.Courses_CourseCode = "{FilterByCourse}"  AND shc.Grade = 'F'
            AND shc.Student_StudentID IN (SELECT shc.Student_StudentID
                                            FROM student_has_courses shc
                                            WHERE shc.Courses_CourseCode = "{RegisteredCourse}")
    """
    Query2_result = pd.read_sql_query(Query_student_get_F, engine)
    num_students_with_f = Query2_result.query("Grade == 'F'").shape[0]
    message = f"The Number of Students Who got F before passing the Course: {num_students_with_f}"
    print(num_students_with_f)

    # This Query Will be Used To display more info about students
    Query5 = """
    SELECT shc.Courses_CourseCode, shc.Grade, s.Level, s.ProgramName, d.DoctorName,
		COUNT(CASE WHEN shc.Grade = 'F' THEN 1 END) as F_count,
        COUNT(CASE WHEN shc.Grade != 'F' THEN 1 END) as non_F_count, s.StudentID
        FROM student_has_courses shc
        INNER JOIN student s ON s.StudentID = shc.Student_StudentID
        INNER JOIN doctor_teach_courses dtc ON shc.AcademicYear_idAcademicYear= dtc.AcademicYear_idAcademicYear AND shc.Courses_CourseCode = dtc.Courses_CourseCode
        INNER JOIN doctor d ON dtc.Doctor_idDoctor = d.idDoctor
        WHERE shc.Courses_CourseCode = "MATH 101"
        AND shc.Student_StudentID IN (SELECT shc.Student_StudentID
                                        FROM student_has_courses shc
                                        WHERE shc.Courses_CourseCode = "COMP 307")
		GROUP BY shc.Courses_CourseCode, shc.Grade, s.Level, s.ProgramName, d.DoctorName
    """

    dftable = pd.DataFrame(Query4_result)

    dfQ1 = dftable.groupby(by=["Grade"]).size().reset_index(name="counts")

    # Create the bar chart
    figure = go.Figure(go.Bar(x=dfQ1['Grade'], y=dfQ1['counts']))

    # Add an initial annotation to guide the user to select values from the filters
    if RegisteredCourse is None or FilterByCourse is None:
        figure.add_annotation(
            text="<b>Select the course you are teaching</b><br> <b>and the courses you want to know the performance of students in.</b><br><br>"
                 "You will know their Grades in these courses",
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=0.5,
            font=dict(size=14),
            align='center',
            bordercolor='#777',
            borderwidth=1,
            borderpad=10,
            bgcolor='rgba(255, 255, 255, 0.7)'
        )
        filters_selected = False
    else:
        filters_selected = True

    # Update the annotation to show a message indicating that no data is available for the selected filters
    if filters_selected and len(dftable) == 0:
        figure.update_layout(
            annotations=[dict(text="No data available for the selected filters", showarrow=False)]
        )

    # Add the curve to the chart
    x_values = dfQ1['Grade']
    y_values = dfQ1['counts']
    figure.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines'))

    # Update the layout
    figure.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    # check if any filters have been selected
    if RegisteredCourse is None or FilterByCourse is None:
        fig1 = go.Figure()
        fig1.add_annotation(
            text="More Information about Students <br> in this course who are in level 1<br>",
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=0.5,
            font=dict(size=10),
            align='center',
            bordercolor='#777',
            borderwidth=1,
            borderpad=7,
            bgcolor='rgba(255, 255, 255, 0.7)'
        )
        fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                           plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)', )

        fig2 = go.Figure()
        fig2.add_annotation(
            text="More Information about Students <br> in this course who are in level 2<br>",
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=0.5,
            font=dict(size=10),
            align='center',
            bordercolor='#777',
            borderwidth=1,
            borderpad=7,
            bgcolor='rgba(255, 255, 255, 0.7)'
        )
        fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                           plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)', )

        fig3 = go.Figure()
        fig3.add_annotation(
            text="More Information about Students <br> in this course who are in level 3<br>",
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=0.5,
            font=dict(size=10),
            align='center',
            bordercolor='#777',
            borderwidth=1,
            borderpad=7,
            bgcolor='rgba(255, 255, 255, 0.7)'
        )
        fig3.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                           plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)', )

        fig4 = go.Figure()
        fig4.add_annotation(
            text="More Information about Students <br> in this course who are in level 4<br>",
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=0.5,
            font=dict(size=10),
            align='center',
            bordercolor='#777',
            borderwidth=1,
            borderpad=7,
            bgcolor='rgba(255, 255, 255, 0.7)'
        )
        fig4.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                           plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)', )
    else:
        dfQ2 = dftable[dftable['Level'] == 1]
        if len(dfQ2) == 0:
            fig1 = go.Figure()
            fig1.update_layout(
                annotations=[dict(text="No Registered Students in Level 1", showarrow=False)]
            )
        else:
            fig1 = px.sunburst(dfQ2, path=['ProgramName', 'Grade'], hover_data=['DoctorName'], color='Grade',
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
                               }
                               )
        fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                           plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)', )
        # concatenate doctor names with separator
        fig1.update_traces(
            customdata=dfQ2[['DoctorName']].fillna('None').values.tolist(),
            hovertemplate='<b>%{label}</b><br><br>Doctor Name(s): %{customdata[0]}<br>Value: %{value}<extra></extra>',
            text=['CS Program', 'Math Program', 'Stat Program']
        )

        dfQ3 = dftable[dftable['Level'] == 2]
        if len(dfQ3) == 0:
            fig2 = go.Figure()
            fig2.update_layout(
                annotations=[dict(text="No Registered Students in Level 2", showarrow=False)]
            )
        else:
            fig2 = px.sunburst(dfQ3, path=['ProgramName', 'Grade'], hover_data=['DoctorName'],
                               color='Grade',
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
        fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                           plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)', )
        # concatenate doctor names with separator
        fig2.update_traces(
            customdata=dfQ3[['DoctorName']].fillna('None').values.tolist(),
            hovertemplate='<b>%{label}</b><br><br>Doctor Name(s): %{customdata[0]}<br>Value: %{value}<extra></extra>',
        )

        dfQ4 = dftable[dftable['Level'] == 3]
        if len(dfQ4) == 0:
            fig3 = go.Figure()
            fig3.update_layout(
                annotations=[dict(text="No Registered Students in Level 3", showarrow=False)]
            )
        else:
            fig3 = px.sunburst(dfQ4, path=['ProgramName', 'Grade'], hover_data=['DoctorName'],
                               color='Grade',
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
        fig3.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                           plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)', )
        # concatenate doctor names with separator
        fig3.update_traces(
            customdata=dfQ4[['DoctorName']].fillna('None').values.tolist(),
            hovertemplate='<b>%{label}</b><br><br>Doctor Name(s): %{customdata[0]}<br>Value: %{value}<extra></extra>'
        )

        dfQ5 = dftable[dftable['Level'] == 4]
        if len(dfQ5) == 0:
            fig4 = go.Figure()
            fig4.update_layout(
                annotations=[dict(text="No Registered Students in Level 4", showarrow=False)]
            )
        else:
            fig4 = px.sunburst(dfQ5, path=['ProgramName', 'Grade'], hover_data=['DoctorName'],
                               color='Grade',
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
        fig4.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                           plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)', )

        # concatenate doctor names with separator
        fig4.update_traces(
            customdata=dfQ5[['DoctorName']].fillna('None').values.tolist(),
            hovertemplate='<b>%{label}</b><br><br>Doctor Name(s): %{customdata[0]}<br>Value: %{value}<extra></extra>'
        )

    return figure, fig1, fig2, fig3, fig4, message
