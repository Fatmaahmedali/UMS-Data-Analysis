# import dash
# import pandas as pd
# from dash import Dash, html, dcc, Input, Output, callback, ctx, State, ClientsideFunction
# from dash.exceptions import PreventUpdate
# import plotly.express as px
# import dash_bootstrap_components as dbc
# from dash import clientside_callback
# import plotly.graph_objects as go
# import base64
# import datetime
# from google.cloud import firestore
# import io
# import plotly.graph_objs as go
# import mysql.connector
# from sqlalchemy import create_engine
# from sqlalchemy import text
# #Create a connection to the MySQL database
# mydb = mysql.connector.connect(
#     host="127.0.0.1",
#     user="root",
#     database="mydb"
# )
# engine = create_engine(f'mysql+mysqlconnector://root@127.0.0.1:3306/mydb')
#
# query1 = """
# SELECT idDoctor ,Doctor_idDoctor ,idAcademicYear ,Academic_Year_Name ,Semester_Name ,CourseCode,CourseName
# FROM doctor , doctor_teach_courses ,academicyear , courses
# where idDoctor = Doctor_idDoctor And idAcademicYear = AcademicYear_idAcademicYear and CourseCode = Courses_CourseCode
# ;
# """
#
# results = pd.read_sql_query(query1,engine)
# print(results)
# dash.register_page(__name__, name='DOCTOR')  # '/' is home page
# df = pd.read_csv("student.csv")
# layout =dbc.Container([
#     dbc.Row([
#         html.Header("choose year"),
#
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([
#                     dbc.Row([
#                         dbc.Col([html.P("choose year"),
#                             dcc.Dropdown(id='animal-type', clearable=False,
#                                  value="df",
#                                  options=[{'label': x, 'value': x} for x in
#                                           results.Academic_Year_Name.unique()],
#                                  className="m-3")]),
#                         dbc.Col([html.P("choose semester"),
#                      dcc.Dropdown(id='animal', clearable=False,
#                              value="df",
#                              options=[{'label': x, 'value': x} for x in
#                                       results.Semester_Name.unique()],
#                              className="m-3"),]),]),
#
#
#                     dcc.Graph(id='line-chart', figure={} ,config={'displayModeBar': False}, className='dcc_compon',),
#                 ])
#             ]),
#         ], width=6 , ),
#         html.Br(),
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([
#                     html.P("Choose Course"),
#                     dcc.Dropdown(id='dpdn2', value="df",
#                                  options=[{'label': x, 'value': x} for x in
#                                           results.CourseName.unique()], className="m-3"),
#                      dcc.Graph(id='my-graph3', figure={}, config={'displayModeBar': False}, className='dcc_compon'
#                                )
#
#                 ]
#                 )
#             ]),
#         ], width=6,
#                 )
#     ], className='mb-2'),
#
# ], fluid=True)
#
# @callback(
#     Output('line-chart','figure'),
#      Input(component_id="animal-type", component_property="value"),
#      Input(component_id="animal", component_property="value"),
# )
# def update_graph(choose_year,choose_semester):
#     query2 = """
#              SELECT d.Doctor_idDoctor,d.Courses_CourseCode,d.AcademicYear_idAcademicYear , DoctorName ,cs.CourseName,a.Academic_Year_Name,s.Grade , a.Semester_Name
#             FROM( (doctor_teach_courses d
#             join Doctor on Doctor_idDoctor= idDoctor
#             join courses cs on d.Courses_CourseCode=cs. CourseCode
#             join academicyear a on d.AcademicYear_idAcademicYear =a.idAcademicYear )
#             join student_has_courses s on s.Courses_CourseCode =  d.Courses_CourseCode )
#             Where Grade IS NOT NULL;
#                               """
#
#     dfb2 = pd.read_sql_query(query2, engine)
#     df_hist = dfb2[dfb2["Academic_Year_Name"] == choose_year]
#     dff = df_hist[df_hist['Semester_Name'] == choose_semester]
#     dff3 = dff[dff['Grade'] == "F" ]
#     dfQ1 = dff3.groupby(by=["CourseName" , "Grade"],).size().reset_index(name="counts")
#     dff4 = dff[dff['Grade'] == "A"]
#     dfQ2 = dff4.groupby(by=["CourseName", "Grade"], ).size().reset_index(name="counts")
#     dff5 = dff[dff['Grade'] == "B+"]
#     dfQ3 = dff5.groupby(by=["CourseName", "Grade"], ).size().reset_index(name="counts")
#     dff6 = dff[dff['Grade'] == "C"]
#     dfQ4 = dff6.groupby(by=["CourseName", "Grade"], ).size().reset_index(name="counts")
#     dff7 = dff[dff['Grade'] == "D"]
#     dfQ5 = dff7.groupby(by=["CourseName", "Grade"], ).size().reset_index(name="counts")
#     dff8 = dff[dff['Grade'] == "A-"]
#     dfQ6 = dff8.groupby(by=["CourseName", "Grade"], ).size().reset_index(name="counts")
#     dff9 = dff[dff['Grade'] == "B"]
#     dfQ7 = dff9.groupby(by=["CourseName", "Grade"], ).size().reset_index(name="counts")
#     dff0 = dff[dff['Grade'] == "C"]
#     dfQ8 = dff0.groupby(by=["CourseName", "Grade"], ).size().reset_index(name="counts")
#
#     fig = go.Figure(
#
#         data=[
#
#             go.Bar(x=dfQ1['CourseName'], y=dfQ1["counts"], offsetgroup=0, name='fail',textposition='auto',),
#             go.Bar(x=dfQ2['CourseName'], y=dfQ2["counts"], offsetgroup=1, name='A',textposition='auto',),
#             go.Bar(x=dfQ6['CourseName'], y=dfQ6["counts"], offsetgroup=1, base=dfQ2["counts"], name='A-',textposition='auto',),
#             go.Bar(x=dfQ3['CourseName'], y=dfQ3["counts"], offsetgroup=1, base=dfQ6["counts"], name='B+',textposition='auto',),
#             go.Bar(x=dfQ7['CourseName'], y=dfQ7["counts"], offsetgroup=1, base=dfQ3["counts"], name='B',textposition='auto',),
#             go.Bar(x=dfQ4['CourseName'], y=dfQ4["counts"], offsetgroup=1, base=dfQ7["counts"], name='C+',textposition='auto',),
#             go.Bar(x=dfQ8['CourseName'], y=dfQ8["counts"], offsetgroup=1, base=dfQ4["counts"], name='C+',textposition='auto',),
#             go.Bar(x=dfQ5['CourseName'], y=dfQ5["counts"], offsetgroup=1, base=dfQ8["counts"], name='D',textposition='auto'),
#             #go.Bar(x=dfQ4['CourseName'], y=dfQ4["counts"], offsetgroup=1, base=dfQ3["counts"], name='F')
#
#         ],
#
#
#     )
#     #fig = df.iplot(asFigure=True, kind='bar', mode='lines+markers', size=1)
#     fig.update_Figure(height = 750,)
#     my_layout = {
#         'title': 'Most starred Python Projects on GitHub',
#         'title_x': 0.5,
#         'xaxis': {'title': 'Repository'},
#         'yaxis': {'title': 'Stars'},
#     }
#
#     #fig = go.Figure(data=trace, layout=my_layout)
#     # fig = go.Figure(data=data3, layout=layout)
#     # Plot the plot and save the file in your Python script directory
#     # py.plot(fig, filename='subplot_pie_chart.html')
#     fig.update_yaxes(tickprefix="%")
#
#     return fig
#
# @callback(
#     Output(component_id='my-graph3', component_property='figure'),
#     Input(component_id='dpdn2', component_property='value'),
# )
# def update_graph(country_chosen):
#     query2 = """
#                            SELECT Student_StudentID ,  Courses_CourseCode,CourseName,CourseCode,Grade,ProgramName , Academic_Year_Name
#                         FROM student_has_courses
#                         join courses on CourseCode =Courses_CourseCode
#     			        join  student on Student_StudentID = StudentID
#                         join academicyear on AcademicYear_idAcademicYear = idAcademicYear
#                         Where Grade IS NOT NULL;
#                           """
#
#     dfb2 = pd.read_sql_query(query2, engine)
#     dff2 = dfb2[dfb2.CourseName==(country_chosen)]
#     num_a = []
#     num_b = []
#     num_c = []
#     num_d = []
#     num_f = []
#     dff3 = dfb2["Grade"]
#     print(dff3)
#     for grade in dff3:
#         if grade == 'A':
#             num_a.append(grade,)
#         elif grade == 'B':
#             num_b.append(grade,)
#         elif grade == 'C':
#             num_c.append(grade,)
#         elif grade == 'D':
#             num_d.append(grade,)
#         elif grade == 'F':
#             num_f.append(grade,)
#
#     total_students = len(num_a) + len(num_b) + len(num_c) + len(num_d) + len(num_f)
#     percent_a = (len(num_a) / total_students) * 100
#     percent_b = (len(num_b) / total_students) * 100
#     percent_c = (len(num_c) / total_students) * 100
#     percent_d = (len(num_d) / total_students) * 100
#     percent_f = (len(num_f) / total_students) * 100
#
#     # print("Percentage of A's:", percent_a)
#     # print("Percentage of B's:", percent_b)
#     # print("Percentage of C's:", percent_c)
#     # print("Percentage of D's:", percent_d)
#     # print("Percentage of F's:", percent_f)
#
#     total_percent = percent_a + percent_b + percent_c + percent_d + percent_f
#     print("Total percentage:", total_percent)
#     dfQ1 = dff2.groupby(by=["Academic_Year_Name" , "Grade"],).size().reset_index(name=total_percent)
#     fig2 = px.bar(dfQ1, x='Academic_Year_Name', y=total_percent, color='Grade',text_auto=True,
#
#                 height=750,)
#     colors = ['orange', '#dd1e35', 'green', '#e55467']
#     fig2.update_yaxes(tickprefix="%")
#     return fig2

import dash
import pandas as pd
from dash import Dash, html, dcc, Input, Output, callback, ctx, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import clientside_callback
import plotly.graph_objects as go
import base64
import datetime
from openpyxl import Workbook
from google.cloud import firestore
import io
import plotly.graph_objs as go
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
filter_year_sem_query = """
  SELECT idDoctor ,Doctor_idDoctor ,idAcademicYear ,Academic_Year_Name ,Semester_INT,Academic_Year_INT,Semester_Name ,CourseCode,CourseName,Courses_CourseCode
FROM doctor , doctor_teach_courses ,academicyear , courses
where idDoctor = Doctor_idDoctor And idAcademicYear = AcademicYear_idAcademicYear and CourseCode = Courses_CourseCode
;

"""
filter_year_sem_result = pd.read_sql_query(filter_year_sem_query, engine)

year_marks = {
    int(filter_year_sem_result['Academic_Year_INT'].loc[i]): filter_year_sem_result['Academic_Year_Name'].loc[i]
    for i in filter_year_sem_result.index
}

semester_marks = {
    int(filter_year_sem_result['Semester_INT'].loc[i]): filter_year_sem_result['Semester_Name'].loc[i]
    for i in filter_year_sem_result.index
}

print(year_marks)
print(semester_marks)
query1 = """
 SELECT d.Doctor_idDoctor,s.Courses_CourseCode,s.AcademicYear_idAcademicYear , DoctorName ,c.CourseName,a.Academic_Year_Name,s.Grade , a.Semester_Name ,Academic_Year_INT ,Semester_INT,c.CourseCode
            FROM( (student_has_courses s
                       join courses c on c.CourseCode =s.Courses_CourseCode
    			        join  student ss on s.Student_StudentID = ss.StudentID
                        join academicyear a on s.AcademicYear_idAcademicYear = a.idAcademicYear )
            join  Doctor_Teach_Courses d on s.Courses_CourseCode =  d.Courses_CourseCode
            join Doctor dd on d.Doctor_idDoctor= dd.idDoctor )
            Where NOT Grade =  "NULL" AND idDoctor="4470"; 
"""

results = pd.read_sql_query(query1, engine)
print(results)
grades = ['A', 'B', 'C', 'D', "A-", "B+", "C+"]
grouped = results.groupby(['Semester_Name', 'Grade', "Academic_Year_Name", "CourseCode"])['Grade'].count().reset_index(name='Count')
grouped['Pass/Fail'] = grouped['Grade'].apply(lambda x: 'Pass' if x in grades[:7] else 'Fail', )
pivot_table = pd.pivot_table(grouped, values='Count', index=['Academic_Year_Name', "Semester_Name", "CourseCode"],
                             columns=['Pass/Fail'], aggfunc=sum, fill_value=0)
pivot_table['Success Rate'] = (pivot_table['Pass'] / (pivot_table['Pass'] + pivot_table['Fail'])) * 100
print(pivot_table)
fig2 = px.line(x=pivot_table.reset_index()['Academic_Year_Name'] + ' ' + pivot_table.reset_index()['Semester_Name'],
               y=pivot_table['Success Rate'], hover_name=pivot_table.reset_index()['CourseCode'], markers=True)
fig2.update_layout(
    xaxis_title='Academic Year AND Semeter',
    yaxis_title='Success Rate (%)'
)
fig2.update_yaxes(tickprefix="%")

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

sidebar.children[-1].style = {'order': '1', 'margin-top': '608px', 'font-size': '19px', 'color': 'rgb(99 21 167)'}

# fig2 = px.line( x=results[x_axis_column], y=results[pivot_table],markers=True)
# dash.register_page(__name__, name='DOCTOR')  # '/' is home page
# df = pd.read_csv("student.csv")
layout5 = html.Div([
    dbc.Row([
        dbc.Col([
            sidebar
        ], xs=4, sm=4, md=1, lg=2, xl=2, xxl=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Label("Success Rate by Course and Academic Year",
                                       style={'font-weight': '600', 'color': 'white', 'padding': '10px'}),
                        ], style={'background': 'rgb(99 21 167)'}),
                        dbc.CardBody([
                            dcc.Graph(id='my-graph5', figure=fig2, config={'displayModeBar': False},
                                      className='dcc_compon')
                        ])
                    ]),
                ], width=10),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(children=[
                                        html.I(className="bi bi-calendar4-range", style={'color': 'rgb(99 21 167)'}),
                                        html.Label("Year", style={'padding': '5px', 'font-weight': '600'}),
                                    ]),
                                ], width=2),
                                dbc.Col([
                                    dcc.Dropdown(
                                        id='year-range-slider',
                                        options=[{'label': x, 'value': x} for x in results.Academic_Year_Name.unique()],
                                        style={'width': '392px'},
                                        className="m-3"
                                    ),
                                ])
                            ], style={'display': 'flex'}),

                            dbc.Row([
                                dbc.Col([
                                    html.Div(children=[
                                        html.I(className="bi bi-calendar4-range", style={'color': 'rgb(99 21 167)'}),
                                        html.Label("Semester", style={'padding': '5px', 'font-weight': '600'}),
                                    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
                                ], width=2),
                                dbc.Col([
                                    dcc.Dropdown(
                                        id='semester-range-slider',
                                        options=[{'label': x, 'value': x} for x in results.Semester_Name.unique()],
                                        style={'width': '392px'},
                                        className="m-3"
                                    )
                                ])
                            ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
                        ], style={'background': 'none'}),
                        dbc.CardBody([
                            dcc.Graph(id='line-chart', figure={}, config={'displayModeBar': False},
                                      className='dcc_compon'),
                        ])
                    ])
                ]),

                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            dbc.Col([
                                html.Div(children=[
                                    html.I(className="fa-solid fa-book", style={'color': 'rgb(99 21 167)'}),
                                    html.Label("Courses", style={'padding': '5px', 'font-weight': '600'})
                                ], className="d-inline"),

                                dcc.Dropdown(
                                    id='filter-dpdn1',
                                    options=[{'label': x, 'value': x} for x in
                                             sorted(results.Courses_CourseCode.astype(str).unique())],
                                ),
                                html.Button("Download CSV", id="btn_csv"),
                                dcc.Download(id="download-dataframe-csv"),
                            ]),
                        ], style={'background': 'none'}),
                        dbc.CardBody([
                            dcc.Graph(id='my-graph3', figure={}, config={'displayModeBar': False},
                                      className='dcc_compon')
                        ])
                    ]),
                ])
            ])
        ], xs=4, sm=4, md=1, lg=2, xl=10, xxl=10)
    ])
]),


@callback(
    Output('line-chart', 'figure'),
    Input(component_id="year-range-slider", component_property="value"),
    Input(component_id="semester-range-slider", component_property="value"),
)
def update_graph(choose_year, choose_semester):
    query2 = """
             SELECT d.Doctor_idDoctor,d.Courses_CourseCode,d.AcademicYear_idAcademicYear , DoctorName ,cs.CourseName,a.Academic_Year_Name,s.Grade , a.Semester_Name ,Academic_Year_INT ,Semester_INT,cs.CourseCode
            FROM( (doctor_teach_courses d
            join Doctor on Doctor_idDoctor= idDoctor
            join courses cs on d.Courses_CourseCode=cs. CourseCode
            join academicyear a on d.AcademicYear_idAcademicYear =a.idAcademicYear )
            join student_has_courses s on s.Courses_CourseCode =  d.Courses_CourseCode )
            Where NOT Grade =  "NULL";            
                              """

    dfb2 = pd.read_sql_query(query2, engine)
    df_hist = dfb2[dfb2["Academic_Year_Name"] == choose_year]
    dff = df_hist[df_hist['Semester_Name'] == choose_semester]
    dff3 = dff[dff['Grade'] == "F"]
    dfQ1 = dff3.groupby(by=["Grade"], ).size().reset_index(name="counts")
    dff4 = dff[dff['Grade'] == "A"]
    dfQ2 = dff4.groupby(by=["Grade"], ).size().reset_index(name="counts")
    dff5 = dff[dff['Grade'] == "B+"]
    dfQ3 = dff5.groupby(by=["Grade"], ).size().reset_index(name="counts")
    dff6 = dff[dff['Grade'] == "C"]
    dfQ4 = dff6.groupby(by=["Grade"], ).size().reset_index(name="counts")
    dff7 = dff[dff['Grade'] == "D"]
    dfQ5 = dff7.groupby(by=["Grade"], ).size().reset_index(name="counts")
    dff8 = dff[dff['Grade'] == "A-"]
    dfQ6 = dff8.groupby(by=["Grade"], ).size().reset_index(name="counts")
    dff9 = dff[dff['Grade'] == "B"]
    dfQ7 = dff9.groupby(by=["Grade"], ).size().reset_index(name="counts")
    dff0 = dff[dff['Grade'] == "C"]
    dfQ8 = dff0.groupby(by=["Grade"], ).size().reset_index(name="counts")

    fig = go.Figure(

        data=[

            go.Bar(x=dff['CourseCode'], y=dfQ1["counts"], offsetgroup=0, name='fail'),
            go.Bar(x=dff['CourseCode'], y=dfQ2["counts"], offsetgroup=1, name='A'),
            go.Bar(x=dff['CourseCode'], y=dfQ6["counts"], offsetgroup=1, base=dfQ2["counts"], name='A-'),
            go.Bar(x=dff['CourseCode'], y=dfQ3["counts"], offsetgroup=1, base=dfQ6["counts"], name='B+'),
            go.Bar(x=dff['CourseCode'], y=dfQ7["counts"], offsetgroup=1, base=dfQ3["counts"], name='B'),
            go.Bar(x=dff['CourseCode'], y=dfQ4["counts"], offsetgroup=1, base=dfQ7["counts"], name='C+'),
            go.Bar(x=dff['CourseCode'], y=dfQ8["counts"], offsetgroup=1, base=dfQ4["counts"], name='C+'),
            go.Bar(x=dff['CourseCode'], y=dfQ5["counts"], offsetgroup=1, base=dfQ8["counts"], name='D'),
            # go.Bar(x=dfQ4['CourseName'], y=dfQ4["counts"], offsetgroup=1, base=dfQ3["counts"], name='F')

        ],

    )
    # fig = df.iplot(asFigure=True, kind='bar', mode='lines+markers', size=1)
    fig.update_yaxes(tickprefix="%")
    # Update the layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    # fig = go.Figure(data=trace, layout=my_layout)
    # fig = go.Figure(data=data3, layout=layout)
    # Plot the plot and save the file in your Python script directory
    # py.plot(fig, filename='subplot_pie_chart.html')

    return fig


@callback(
    Output(component_id='my-graph3', component_property='figure'),
    Output("download-dataframe-csv", "data"),
    Input(component_id='filter-dpdn1', component_property='value'),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,

)
def update_graph(country_chosen, n_clicks):
    query2 = """
                           SELECT Student_StudentID ,  Courses_CourseCode,CourseName,CourseCode,Grade,ProgramName , Academic_Year_Name ,Semester_Name , Semester_INT
                        FROM student_has_courses
                        join courses on CourseCode =Courses_CourseCode
    			        join  student on Student_StudentID = StudentID
                        join academicyear on AcademicYear_idAcademicYear = idAcademicYear
                        Where NOT Grade =  "NULL";
                          """

    dfb2 = pd.read_sql_query(query2, engine)
    dff2 = dfb2[dfb2.Courses_CourseCode == (country_chosen)]
    grades = ['A', 'B', 'C', 'D', "A-", "B+", "C+"]
    grouped = dff2.groupby(["CourseCode", 'Semester_Name', 'Grade', "Academic_Year_Name"])[
        'Grade'].count().reset_index(name='Count')
    grouped['Pass/Fail'] = grouped['Grade'].apply(lambda x: 'Pass' if x in grades[:7] else 'Fail', )
    pivot_table = pd.pivot_table(grouped, values='Count',
                                 index=['Academic_Year_Name', "Semester_Name", "CourseCode"],
                                 columns=['Pass/Fail'], aggfunc=sum, fill_value=0)
    pivot_table['Success Rate'] = (pivot_table['Pass'] / (pivot_table['Pass'] + pivot_table['Fail'])) * 100
    print(pivot_table)
    fig2 = px.bar(x=pivot_table.reset_index()['Academic_Year_Name'] + ' ' + pivot_table.reset_index()['Semester_Name'],
                  y=pivot_table['Success Rate'], color=pivot_table.reset_index()['Success Rate'], text_auto=True, )
    fig2.update_layout(
        title='Success Rate by Course and Academic Year',
        xaxis_title='Academic Year AND Semeter',
        yaxis_title='Success Rate (%)'
    )
    fig2.update_yaxes(tickprefix="%")

    # fig2 = px.bar(dfQ1, x=dfQ1.reset_index()['Academic_Year_Name']+ ' ' +dfQ1.reset_index()['Semester_Name'], y=total_percent, color='Grade',text_auto=True,
    #
    #             height=500,)
    #
    # fig2.update_yaxes(tickprefix="%")
    # if n_clicks is None:
    #     raise dash.exceptions.PreventUpdate
    # else:
    #  dict(dcc.send_data_frame(dff2.to_excel, "mydf.xlsx", sheet_name="Sheet_name_1",))
    return fig2, dict(dcc.send_data_frame(dff2.to_excel, "mydf.xlsx", sheet_name="Sheet_name_1", ))
