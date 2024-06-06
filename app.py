from dash import Dash
app = Dash(__name__)
from project.home import app


app1 = Dash(__name__)
from DoctorInterface.home import app1

if __name__ == "__main__":
    app.run_server(debug=True)
    app1.run_server(debug=True)

