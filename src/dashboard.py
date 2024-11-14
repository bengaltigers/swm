from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import mysql.connector
import pandas as pd
from config import DB_CONFIG

# Function to fetch data for fullness levels (for table display)
def fetch_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    query = "SELECT * FROM readings"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to fetch devices list from the database
def fetch_devices():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices;")
    devices = cursor.fetchall()
    cursor.close()
    conn.close()

    # Format devices list into a list of dictionaries for Dash table
    devices_list = [
        {
            "device_id": device[0],
            "device_name": device[1],
            "latitude": device[2],
            "longitude": device[3],
        }
        for device in devices
    ]

    return devices_list

# Fetch average daily fullness
def fetch_average_fullness():
    conn = mysql.connector.connect(**DB_CONFIG)
    query = "SELECT DATE(timestamp) as date, AVG(fullness_level) as avg_fullness FROM readings GROUP BY date"
    df_avg = pd.read_sql(query, conn)
    conn.close()
    return df_avg


# Function to initialize the Dash app
def init_dashboard(server):
    # Initialize Dash app and bind it to the Flask server
    dash_app = Dash(__name__, server=server, url_base_pathname='/dashboard/')

    # Layout of the Dash app
    dash_app.layout = html.Div([
        html.H1("Waste Management Dashboard"),
        html.Div("Displays fullness levels of compactors from MQTT data."),

        # Devices List Table
        html.H2("Devices List"),
        dash_table.DataTable(
            id='devices-table',
            columns=[
                {"name": "Device ID", "id": "device_id"},
                {"name": "Device Name", "id": "device_name"},
                {"name": "Latitude", "id": "latitude"},
                {"name": "Longitude", "id": "longitude"},
            ],
            data=fetch_devices(),  # Pass the fetched devices data
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={
                'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                'textAlign': 'center', 'padding': '5px',
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
            },
        ),

        # Average Daily Fullness
        # Table component for displaying fullness data
        html.H2("Average Fullness Levels of All Compactors"),
        dash_table.DataTable(
            id='average-table',
            columns=[{"name": "Date", "id": "date"}, {"name": "Avg Fullness", "id": "avg_fullness"}],
            data=fetch_average_fullness().to_dict('records')
        ),

        # Table component for displaying fullness data
        html.H2("Fullness Levels of Compactors"),
        dash_table.DataTable(
            id='data-table',
            columns=[{"name": i, "id": i} for i in fetch_data().columns],
            data=fetch_data().to_dict('records'),
            style_data_conditional=[
                {
                    'if': {'filter_query': '{fullness_level} >= 80'},
                    'backgroundColor': 'red',
                    'color': 'white',
                }
            ]
        ),

        # Button to refresh data
        html.Button("Refresh Data", id="refresh-button", n_clicks=0),
    ])

    # Update fullness levels table on button click
    @dash_app.callback(
        Output("data-table", "data"),
        [Input("refresh-button", "n_clicks")]
    )
    def update_table(n_clicks):
        df = fetch_data()
        return df.to_dict("records")

    return dash_app