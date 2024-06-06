# Dash Libraries
import dash
from dash import html, dcc, Input, Output, callback, State, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
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

# Create a database engine
engine = create_engine(f'mysql+mysqlconnector://root@127.0.0.1:3306/mydb')

########################## Definition of the Second Figure ##########################################
fig2 = go.Figure()
fig2.add_annotation(
    text="<b>Select the courses You are thinking to Register in</b><br>",
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0.5,
    y=0.5,
    font=dict(size=13),
    align='center',
    bordercolor='#777',
    borderwidth=1,
    borderpad=10,
    bgcolor='rgba(255, 255, 255, 0.7)'
)

########################################################################################################################
######## Queries ###########
## UNKNOWN Query مش فاكره ما الهدف منها
# dbf_doctor_analysis = None  # Define the variable outside the if statement
query = """
        SELECT s.StudentID, s.CGPA, s.Level, s.ProgramName, shc.Courses_CourseCode, shc.Grade, shc.AcademicYear_idAcademicYear, ay.Academic_Year_Name, ay.Academic_Year_INT, ay.Semester_INT, ay.Semester_Name, dtc.Doctor_idDoctor, d.DoctorName
        From student s
        INNER JOIN student_has_courses shc ON  s.StudentID = shc.Student_StudentID
        INNER JOIN academicyear ay ON shc.AcademicYear_idAcademicYear = ay.idAcademicYear
        INNER JOIN doctor_teach_courses dtc ON dtc.AcademicYear_idAcademicYear = shc.AcademicYear_idAcademicYear AND dtc.Courses_CourseCode = shc.Courses_CourseCode
        INNER JOIN doctor d ON d.idDoctor = dtc.Doctor_idDoctor
        where shc.Courses_CourseCode = 'COMP 201'
"""
results = pd.read_sql_query(query, engine)

################################################################
################################################################
# Query 1: Each Student Get Courses that he has not Completed
Query1 = """
    SELECT DISTINCT phc.Courses_CourseCode, phc.Program_ProgramID, d.DoctorName
    FROM student_has_program shp
    LEFT JOIN program_has_courses phc ON phc.Program_ProgramID = shp.Program_ProgramID
    INNER JOIN doctor_teach_courses dtc ON dtc.Courses_CourseCode = phc.Courses_CourseCode
    INNER JOIN doctor d ON d.idDoctor = dtc.Doctor_idDoctor
    WHERE phc.Courses_CourseCode NOT IN(
        SELECT shc.Courses_CourseCode
        FROM student_has_courses shc
        INNER JOIN student_has_program shp ON shc.Student_StudentID = shp.Student_StudentID AND shc.AcademicYear_idAcademicYear = shp.AcademicYear_idAcademicYear
        WHERE shc.Student_StudentID = 'ff0ab61d-909f-4a51-ba7f-4c50c11baac7'
    )
"""
Query1_result = pd.read_sql_query(Query1, engine)

# Query2: Each Student Get Courses that he has Completed
Query2 = """
    SELECT shc.Courses_CourseCode
    FROM student_has_courses shc
    WHERE shc.Student_StudentID = "2v2nN3vhzK"
"""
Query2_courses_result = pd.read_sql_query(Query2, engine)

################################################################
# # Query 2:
# # Replace these values with the list of course codes from your Dash application
course_codes = ['COMP 303', 'COMP 305']


############################################### Statistical Analysis ###################################################

# Calculate The success and Fail Percentage For each Doctor
def calculate_pass_fail_percentage(df):
    # Define function to classify grades as pass/fail
    def classify_grade(grade):
        if grade == 'F':
            return 'Fail'
        else:
            return 'Pass'

    # Apply function to create a new column 'Pass/Fail'
    df['Pass/Fail'] = df['Grade'].apply(classify_grade)

    # Group by doctor and 'Pass/Fail', count the number of occurrences, and calculate percentages
    grouped = df.groupby(['DoctorName', 'Pass/Fail']).size().reset_index(name='Count')
    grouped['Percentage'] = grouped['Count'] / grouped.groupby('DoctorName')['Count'].transform('sum') * 100
    print(grouped)

    # Return the result
    return grouped


# Calculate The success and Fail Percentage For each Doctor For Each Year
def calculate_pass_fail_percentage2(df):
    # Define function to classify grades as pass/fail
    def classify_grade(grade):
        if grade == 'F':
            return 'Fail'
        else:
            return 'Pass'

    # Apply function to create a new column 'Pass/Fail'
    df['Pass/Fail'] = df['Grade'].apply(classify_grade)

    # Group by year, doctor, and 'Pass/Fail', count the number of occurrences, and calculate percentages
    grouped = df.groupby(['Academic_Year_INT', 'DoctorName', 'Pass/Fail']).size().reset_index(name='Count')
    grouped['Percentage'] = grouped['Count'] / grouped.groupby(['Academic_Year_INT', 'DoctorName'])['Count'].transform(
        'sum') * 100
    print(grouped)

    # Return the result
    return grouped


def calc_success_rates_forEachDoc_and_corr_analysis(df):
    # Define function to classify grades as pass/fail
    def classify_grade(grade):
        if grade == 'F':
            return 'Fail'
        else:
            return 'Pass'

    # Apply function to create a new column 'Pass/Fail'
    df['Pass/Fail'] = df['Grade'].apply(classify_grade)

    # Group by year, doctor, and 'Pass/Fail', count the number of passes, and calculate success rates
    grouped = df[df['Pass/Fail'] == 'Pass'].groupby(['DoctorName', 'Academic_Year_INT'])[
        'Pass/Fail'].count().reset_index(name='Pass Count')
    grouped['Success Rate'] = grouped['Pass Count'] / \
                              df.groupby(['DoctorName', 'Academic_Year_INT'])['Pass/Fail'].count().reset_index(
                                  name='Count')['Count'] * 100
    print(grouped)

    DoctorNames = grouped['DoctorName'].unique().tolist()
    SuccessRates = grouped.groupby('DoctorName')['Success Rate'].apply(list).tolist()

    # print the two lists
    print(DoctorNames)
    print(SuccessRates)

    # Return the result
    return grouped


def write_conclusion(df):
    # Initialize an empty string to store the conclusion
    conclusion = ""

    # Loop over each academic year
    for year in df['Academic_Year_INT'].unique():
        # Filter the dataframe to keep only the rows for the current year
        year_df = df[df['Academic_Year_INT'] == year]

        # Calculate the total number of non-F grades for the current year
        total_non_f_grades = year_df[year_df['Grade'] != 'F']['counts'].sum()

        # Calculate the total number of grades for the current year
        total_grades = year_df['counts'].sum()

        # Calculate the probability of success and failure for the current year
        prob_success = total_non_f_grades / total_grades
        prob_failure = 1 - prob_success

        # Convert the probabilities to percentages for the current year
        success_percentage = prob_success * 100
        fail_percentage = prob_failure * 100

        conclusion += f"\nIn {year}: {success_percentage:.1f}% of students who are similar to you and Passed in this " \
                      f"course and  {fail_percentage:.1f}% of students Failed in this course"

    return conclusion


################################# Defrinition Of Side bar ##############################################################
sidebar2 = dbc.Nav(
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
        'width': '171px',
        'display': 'flex',
        'flex-direction': 'column'

    }
)

sidebar2.children[-1].style = {'order': '1', 'margin-top': '608px', 'font-size': '19px'}

# dash.register_page(__name__, path='/register', name='For Registration')  # '/' is home page-+
layout2 = html.Div([
    dbc.Row([
        dbc.Col([
            sidebar2
        ], xs=4, sm=4, md=1, lg=2, xl=2, xxl=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            "For More Information through Registration Process",
                        ], style={'color': '#007bff', 'font-weight': '600', 'font-size': '18px', "background": "none"}),
                        dbc.CardBody([
                            html.Div(children=[
                                html.Div(id='graphs-section', children=[
                                    dcc.Graph(id='Graph1_Track',
                                              style={'width': '691px', 'height': '370px'})])
                            ])
                        ], style={'padding': '0px'}),
                        dbc.CardFooter([
                            html.Label("Conclusion",
                                       style={'color': '#007bff', 'font-weight': '600', 'font-size': '18px'}),
                            html.Div(children=[],
                                     id="conclusion1_track",
                                     style={
                                         "white-space": "pre-wrap",
                                         "width": "668pxx",  # set to the desired width
                                         "height": "100px",  # set to the desired height
                                         "overflow-y": "auto",
                                         # add this property to enable vertical scrolling when the content exceeds the height
                                         "scrollbar-color": "gray #f0f0f0",
                                         # set the color of the scrollbar track and thumb
                                         "scrollbar-width": "thin",  # set the width of the scrollbar track and thumb

                                     })
                        ], style={"background": "none"})
                    ], style={
                        "border-top": "0px",
                        "border-radius": "0px",
                        "border-left": "0px",
                        "border-right": "0px"
                    })
                ], md=7, lg=7, xl=7, xxl=7, style={'height': '100%'}),

                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.Div(children=[
                                html.I(className="fa-solid fa-book", style={'color': '#007bff'}),
                                html.Label("Course", style={'padding': '5px', 'font-weight': '600'})
                            ], className="d-inline"),

                            dcc.Dropdown(
                                id='filter1-dpdn_track',
                                options=[{'label': x, 'value': x} for x in
                                         sorted(Query1_result.Courses_CourseCode.astype(str).unique())],
                                value="COMP 104"
                            ),
                        ], style={'height': '100%', }),
                        dbc.Col([
                            html.Div(children=[
                                html.I(className="fa-solid fa-user-group", style={'color': '#007bff'}),
                                html.Label("Doctor", style={'padding': '5px', 'font-weight': '600'})
                            ], className="d-inline"),

                            dcc.Dropdown(
                                id='filter2-dpdn_track',
                                options=[{'label': x, 'value': x} for x in
                                         sorted(Query1_result.DoctorName.astype(str).unique())],
                                style={'width': '230px'}
                            ),
                        ])
                    ], style={'flex-wrap': 'nowrap', }),
                    dbc.Row([
                        html.Div(
                            children=[
                                html.I(className="bi bi-mortarboard-fill", style={'color': '#007bff'}),
                                html.Label("GPA Range", style={'padding': '5px', 'font-weight': '600'}),
                            ], className="d-inline"),

                        dcc.RangeSlider(
                            id='gpa-range-slider-track',
                            min=0, max=4, step=0.01,
                            marks={0: '0', 1: '1', 2: '2', 3: '3', 4: '4'},
                            value=[0, 4]
                        ),
                        html.Div(id='slider-output-container'),

                    ]),
                    dbc.Row([
                        html.Div(
                            children=[
                                html.I(className="bi bi-calendar4-range", style={'color': '#007bff'}),
                                html.Label("Year Range", style={'padding': '5px', 'font-weight': '600'}),
                            ]
                        ),

                        dcc.RangeSlider(
                            id='year-range-slider-track',
                            min=2017, max=2022, step=1,
                            marks={2017: '2017', 2018: '2018', 2019: '2019', 2020: '2020', 2021: '2021', 2022: '2022'},
                            value=[2017, 2022]
                        ),
                    ]),
                    dbc.Row([
                        html.Div(children=[
                            html.Div(id='add-course', children=[
                                dbc.Button("Filter By Completed Course", outline=True, color="primary",
                                           className="me-1",
                                           id="add-btn", n_clicks=0,
                                           style={'margin-top': '10px',
                                                  }),

                            ], style={'margin-top': '17px'}),
                            dbc.Button('Clear', outline=True, color="primary", className="me-1",
                                       id='clear-btn', n_clicks=0,
                                       style={
                                           'margin-bottom': '10px',
                                           'margin-top': '-57px',
                                           'margin-left': '253px',
                                           'width': '100px',
                                       }),
                            html.Div(id="dropdown-container-output-div"),
                            html.Div(id='container', children=[]),
                        ])
                    ])
                ]),
            ], style={'border': '2px solid #ededed', 'box-shadow': '4px 5px 21px -7px rgb(31 84 173)',
                      'margin-bottom': '20px'}),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            "Student Who Register in Courses in Same Semester"
                        ], style={'color': '#007bff', 'font-weight': '600', 'font-size': '18px', "background": "none"}),
                        dbc.CardBody([
                            html.Div(children=[
                                html.Div(id='graphs-section', children=[
                                    dcc.Graph(id='Graph2_Track', figure=fig2,
                                              style={'width': '691px', 'height': '370px'})])
                            ])
                        ], style={'padding': '0px'}),
                        # dbc.CardFooter([
                        #     html.Label("Conclusion",
                        #                style={'color': '#007bff', 'font-weight': '600', 'font-size': '18px'}),
                        # ], style={"background": "none"})
                    ], style={
                        "border-top": "0px",
                        "border-radius": "0px",
                        "border-left": "0px",
                        "border-right": "0px"
                    })
                ], md=7, lg=7, xl=7, xxl=7, style={'height': '100%'}),

                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.Div(children=[
                                html.I(className="fa-solid fa-book", style={'color': '#007bff'}),
                                html.Label("Course", style={'padding': '5px', 'font-weight': '600'})
                            ], className="d-inline"),

                            dcc.Dropdown(
                                id='filter1-dpdn2_track',
                                options=[{'label': x, 'value': x} for x in
                                         sorted(Query1_result.Courses_CourseCode.astype(str).unique())],
                                multi=True
                            ),
                        ], style={'height': '100%'}),
                    ], style={'flex-wrap': 'nowrap', }),

                    dbc.Row([
                        dbc.Button("Update", outline=True, color="primary", className="me-1", id="update-btn",
                                   style={'width': '208px', 'margin-left': '11px', 'margin-top': '15px',
                                          'margin-bottom': '13px'})
                    ]),
                    dbc.Row([
                        html.Div(
                            children=[
                                html.I(className="bi bi-mortarboard-fill", style={'color': '#007bff'}),
                                html.Label("GPA Range", style={'padding': '5px', 'font-weight': '600'}),
                            ], className="d-inline"),

                        dcc.RangeSlider(
                            id='gpa-range-slider2-track',
                            min=0, max=4, step=0.01,
                            marks={0: '0', 1: '1', 2: '2', 3: '3', 4: '4'},
                            value=[0, 4]
                        ),
                        html.Div(id='slider-output-container2'),

                    ]),
                    dbc.Row([
                        html.Div(
                            children=[
                                html.I(className="bi bi-calendar4-range", style={'color': '#007bff'}),
                                html.Label("Year Range", style={'padding': '5px', 'font-weight': '600'}),
                            ]
                        ),

                        dcc.RangeSlider(
                            id='year-range-slider2-track',
                            min=2017, max=2022, step=1,
                            marks={2017: '2017', 2018: '2018', 2019: '2019', 2020: '2020', 2021: '2021', 2022: '2022'},
                            value=[2017, 2022]
                        ),
                    ])
                ]),
            ], style={'border': '2px solid #ededed', 'box-shadow': 'rgb(31 84 173) -5px -3px 13px -7px'}),

        ])
    ])
])


# ########### CALLBACK : GPA Range Slider Content ####################
@callback(
    Output('slider-output-container', 'children'),
    Input('gpa-range-slider-track', 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(value)


############# CALLBACK : Filter By Courses ################
@callback(
    Output(component_id='container', component_property='children'),
    [Input(component_id='add-btn', component_property='n_clicks'),
     Input(component_id='clear-btn', component_property='n_clicks')],
    [State(component_id='container', component_property='children')]
)
def add_course_to_container(n_clicks, clear_clicks, container):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'add-btn':
            if n_clicks is None or n_clicks == 0:
                raise PreventUpdate
            else:
                return container + new_courses_container(n_clicks) + grades_checklists(n_clicks)
        elif button_id == 'clear-btn':
            return []
        else:
            raise PreventUpdate


def new_courses_container(n_clicks):
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate
    else:
        my_dpdn = dcc.Dropdown(
            id={"type": "Courses-filter-dropdown", "index": n_clicks},
            options=[{'label': x, 'value': x} for x in
                     sorted(Query2_courses_result.Courses_CourseCode.astype(str).unique())],
            value="COMP 303",
            style={'width': '150px',
                   'display': 'inline-block'
                   })
        return [my_dpdn]


def grades_checklists(n_clicks):
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate
    else:
        my_checklist = dcc.Checklist(
            id={"type": "Grades-filter-checklist", "index": n_clicks},
            options=[
                {'label': 'A', 'value': 'A'},
                {'label': 'A-', 'value': 'A-'},
                {'label': 'B+', 'value': 'B+'},
                {'label': 'B', 'value': 'B'},
                {'label': 'C+', 'value': 'C+'},
                {'label': 'C', 'value': 'C'},
                {'label': 'D', 'value': 'D'},
                {'label': 'F', 'value': 'F'}],
            value=['A', 'B', 'C'],
            style={
                'vertical-align': 'super',
                'padding-left': '4px',
                'display': 'inline-flex'
            }
        )
        return [my_checklist]


def clear_button():
    my_button = html.Button('Clear', id='clear-btn', style={'margin-left': '10px'})
    return my_button


# ############# CALLBACK : CHANGE First GRAPH From DB ################
@callback(
    [
        Output(component_id='Graph1_Track', component_property='figure'),
        Output(component_id='filter2-dpdn_track', component_property='options'),
        Output(component_id='conclusion1_track', component_property='children')
    ],
    [
        Input(component_id='filter1-dpdn_track', component_property='value'),
        Input(component_id='filter2-dpdn_track', component_property='value'),
        Input(component_id='gpa-range-slider-track', component_property='value'),
        Input(component_id='year-range-slider-track', component_property='value'),
        Input(component_id={"type": "Courses-filter-dropdown", "index": ALL}, component_property="value"),
        Input(component_id={"type": "Grades-filter-checklist", "index": ALL}, component_property="value")
    ]
)
def update_Graph(course_value, doctor_value, slider_range_value, slider_range_Year, course_codes_list, grades_list):
    if not course_value:
        raise PreventUpdate
    query1 = f"""
        SELECT s.StudentID, s.CGPA, s.Level, s.ProgramName, shc.Courses_CourseCode, shc.Grade, shc.AcademicYear_idAcademicYear, ay.Academic_Year_Name, ay.Academic_Year_INT, ay.Semester_INT, ay.Semester_Name, dtc.Doctor_idDoctor, d.DoctorName
        From student s
        INNER JOIN student_has_courses shc ON  s.StudentID = shc.Student_StudentID
        INNER JOIN academicyear ay ON shc.AcademicYear_idAcademicYear = ay.idAcademicYear
        INNER JOIN doctor_teach_courses dtc ON dtc.AcademicYear_idAcademicYear = shc.AcademicYear_idAcademicYear AND dtc.Courses_CourseCode = shc.Courses_CourseCode
        INNER JOIN doctor d ON d.idDoctor = dtc.Doctor_idDoctor
        where shc.Courses_CourseCode = %s
    """
    dbf = pd.read_sql_query(query1, engine, params=[course_value])
    dbf_doc_corr_analysis = pd.read_sql_query(query1, engine, params=[course_value])

    if course_codes_list and grades_list:
        print(course_codes_list)
        print(grades_list)
        # Create a dictionary that maps each course code to its list of grades
        course_grade_map = dict(zip(course_codes_list, grades_list))
        print(course_grade_map)

        # Generate a subquery for each course and grade combination
        subqueries = []
        for course_code in course_codes_list:
            if course_code in course_grade_map:
                grades = course_grade_map[course_code]
                grade_placeholders = ','.join(['%s'] * len(grades))
                subquery = f'SELECT shc.Student_StudentID FROM student_has_courses shc WHERE shc.Courses_CourseCode = ' \
                           f'%s AND shc.Grade IN ({grade_placeholders}) '
                params = [course_code] + grades
                subqueries.append((subquery, params))
            else:
                subquery = 'SELECT shc.Student_StudentID FROM student_has_courses shc WHERE shc.Courses_CourseCode = %s'
                params = [course_code]
                subqueries.append((subquery, params))

        # Combine the subqueries into a single query using nested SELECT statements
        subquery_string = ''
        for i, (subquery, params) in enumerate(subqueries):
            if i == 0:
                subquery_string += f'({subquery})'
            else:
                subquery_string += f' AND s.StudentID IN ({subquery})'
            subquery_string = subquery_string.replace('%s', '"{}"').format(*params)

        # Generate the final query by combining the subquery with the main query
        query = f"""
        SELECT s.StudentID, s.CGPA, s.Level, s.ProgramName, shc.Courses_CourseCode, shc.Grade, shc.AcademicYear_idAcademicYear, ay.Academic_Year_Name, ay.Academic_Year_INT, ay.Semester_INT, ay.Semester_Name, dtc.Doctor_idDoctor, d.DoctorName
        FROM student s
        INNER JOIN student_has_courses shc ON s.StudentID = shc.Student_StudentID
        INNER JOIN academicyear ay ON shc.AcademicYear_idAcademicYear = ay.idAcademicYear
        INNER JOIN doctor_teach_courses dtc ON dtc.AcademicYear_idAcademicYear = shc.AcademicYear_idAcademicYear AND dtc.Courses_CourseCode = shc.Courses_CourseCode
        INNER JOIN doctor d ON d.idDoctor = dtc.Doctor_idDoctor
        WHERE shc.Courses_CourseCode = "{course_value}" AND s.StudentID IN {subquery_string}
        """

        # Execute the query and store the results in a dataframe
        dbf = pd.read_sql_query(query, engine)

    if doctor_value:
        dbf = dbf[dbf.DoctorName == doctor_value]
        corr_analysis = calc_success_rates_forEachDoc_and_corr_analysis(dbf_doc_corr_analysis)
        print(corr_analysis)
    dbf = dbf[(dbf['CGPA'] >= slider_range_value[0]) & (dbf['CGPA'] <= slider_range_value[1])]
    dbf = dbf[(dbf['Academic_Year_INT'] >= slider_range_Year[0]) & (dbf['Academic_Year_INT'] <= slider_range_Year[1])]

    dbff = dbf.groupby(by=["Academic_Year_INT", "Grade"]).size().reset_index(name="counts")

    # Define the colors for each grade
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

    figure = px.bar(dbff, x='Academic_Year_INT', y='counts',
                    color='Grade',
                    category_orders={'Grade': ['A', 'A-', 'B+', 'B', 'C+', 'C', 'D', 'F', 'P']},
                    color_discrete_map=color_map)
    figure.update_layout(xaxis={'range': [2016, 2022]},
                         plot_bgcolor='rgba(0,0,0,0)',
                         paper_bgcolor='rgba(0,0,0,0)',
                         )
    conclusion1 = write_conclusion(dbff)

    if course_value is None:
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

    doctor_options = [{'label': option, 'value': option} for option in sorted(dbf.DoctorName.astype(str).unique())]
    return figure, doctor_options, conclusion1


# ########### CALLBACK : GPA Range Slider Content 2 ####################
@callback(
    Output('slider-output-container2', 'children'),
    Input('gpa-range-slider2-track', 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(value)


############ CALLBACK : CHANGE THE SECOND GRAPH By Excel ################
@callback(
    Output(component_id="Graph2_Track", component_property="figure"),
    [
        Input(component_id="update-btn", component_property="n_clicks"),
        Input(component_id="gpa-range-slider2-track", component_property="value"),
        Input(component_id='year-range-slider2-track', component_property='value')
    ],
    State(component_id="filter1-dpdn2_track", component_property="value")

)
def create_data_frame(n_clicks, slider_range_value, slider_range_Year, course_codes):
    if n_clicks is None or course_codes is None or len(course_codes) == 0:
        raise PreventUpdate
    # course_codes = ['COMP 303', 'COMP 307', 'COMP 309']  # replace with your list of course codes
    else:
        results = pd.DataFrame()
        if len(course_codes) == 1:
            query = """
                SELECT DISTINCT sh1.Student_StudentID, s.CGPA, ay.Academic_Year_INT, ay.Academic_Year_Name, sh1.Courses_CourseCode, sh1.Grade As Course1Grades
                FROM student_has_courses sh1
                INNER JOIN student s ON s.StudentID = sh1.Student_StudentID
                INNER JOIN academicyear ay ON ay.idAcademicYear = sh1.AcademicYear_idAcademicYear
                WHERE sh1.Courses_CourseCode = %s
            """
            results = pd.read_sql_query(query, engine, params=course_codes)
        elif len(course_codes) > 1:
            query = "SELECT DISTINCT sh1.Student_StudentID, s.CGPA, ay.Academic_Year_INT, ay.Academic_Year_Name, "
            for i in range(1, len(course_codes) + 1):
                query += f"sh{i}.Courses_CourseCode As Courses_CourseCode{i}, sh{i}.Grade As Course{i}Grades, "
            query = query[:-2]  # Remove the final comma and space

            query += "\nFROM student_has_courses sh1 "
            for i in range(2, len(course_codes) + 1):
                query += f"INNER JOIN student_has_courses sh{i} ON sh{i - 1}.Student_StudentID = sh{i}.Student_StudentID "

            query += "INNER JOIN student s ON s.StudentID = sh1.Student_StudentID "
            query += "INNER JOIN academicyear ay ON ay.idAcademicYear = sh1.AcademicYear_idAcademicYear "

            query += "WHERE "
            for i in range(1, len(course_codes) + 1):
                query += f"sh{i}.Courses_CourseCode = %s AND "
            query = query[:-5]  # Remove the final " AND "
            query += "AND " + " AND ".join(
                [f"sh{i}.AcademicYear_idAcademicYear = sh{i + 1}.AcademicYear_idAcademicYear" for i in
                 range(1, len(course_codes))])
            # Execute the query
            print(query)
            results = pd.read_sql_query(query, engine, params=course_codes)
        course_code_cols = [col for col in results.columns if col.startswith("Courses_CourseCode")]
        print(course_code_cols)
        # Get column names that match the pattern "Course{i}Grades"
        course_grade_cols = [col for col in results.columns if col.startswith("Course") and col.endswith("Grades")]
        print(course_grade_cols)

        # Select the Academic Year column and the course code columns from the original dataframe
        course_code_data = results.loc[:, ["Academic_Year_INT", "Student_StudentID", "CGPA"] + course_code_cols]

        # Select the Academic Year column and the course grade columns from the original dataframe
        course_grade_data = results.loc[:, ["Academic_Year_INT", "Student_StudentID", "CGPA"] + course_grade_cols]

        print(course_code_data)
        print(course_grade_data)

        if course_code_data.empty or course_grade_data.empty:
            # Return an empty figure with an annotation
            fig2 = go.Figure()
            fig2.add_annotation(
                text="<b>No Students Registered in These Courses together</b><br> <b>maybe you select courses from "
                     "spring and autumn.</b><br><br>",
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
            return fig2

        print("The Melted Graph")
        course_code_data_melted = pd.melt(course_code_data, id_vars=["Academic_Year_INT", "Student_StudentID", "CGPA"],
                                          var_name="Course",
                                          value_name="CourseCode").rename(
            columns={"Academic_Year_INT": "Years", "CGPA": "myCGPA"})
        print(course_code_data_melted)

        course_grade_data_melted = pd.melt(course_grade_data,
                                           id_vars=["Academic_Year_INT", "Student_StudentID", "CGPA"],
                                           var_name="Course",
                                           value_name="CourseGrade")
        print(course_grade_data_melted)

        # # Concatenate the two dataframes by columns
        df_concatenated = pd.concat([course_code_data_melted, course_grade_data_melted], axis=1)
        df_merged = df_concatenated[["Years", "CourseCode", "CourseGrade", "myCGPA"]]

        # # Print the merged dataframe
        print(df_merged)

        merged_df_2 = df_merged[
            (df_merged['myCGPA'] >= slider_range_value[0]) & (df_merged['myCGPA'] <= slider_range_value[1])]
        merged_df_3 = merged_df_2[
            (df_merged['Years'] >= slider_range_Year[0]) & (df_merged['Years'] <= slider_range_Year[1])]
        dbff = merged_df_3.groupby(by=["Years", "CourseGrade", "CourseCode"]).size().reset_index(name="counts")

        # Define the colors for each grade
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

        fig2 = px.bar(dbff, x="CourseCode", y="counts", facet_col="Years", color="CourseGrade",
                      category_orders={'CourseGrade': ['A', 'A-', 'B+', 'B', 'C+', 'C', 'D', 'F', 'P']},
                      color_discrete_map=color_map)
        return fig2
