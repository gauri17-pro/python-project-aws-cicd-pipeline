import pandas as pd
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import sys
import argparse

class CrashData():
    def __init__(self, csvfile):
        try:
            self.df = pd.read_csv(csvfile, index_col=0)
            print(f'The shape before cleansing {self.df.shape}')
            self.df = self.df.loc[self.df['Loc_Local_Government_Area'] != 'Unknown', 
                ['Crash_Year','Crash_Type','Crash_Longitude','Crash_Latitude']]
            print(f'The shape after cleansing {self.df.shape}')
        except:
            sys.exit('Unable to load data file')
        self.year_min, self.year_max = self.df['Crash_Year'].min().item(), self.df['Crash_Year'].max().item()
        self.center_long, self.center_lat = self.df['Crash_Longitude'].mean().item(), self.df['Crash_Latitude'].mean().item()
        self.center_long, self.center_lat = 153.0260, -27.4705
        self.crashtype_list = self.df['Crash_Type'].unique().tolist()

parser = argparse.ArgumentParser(description = "Dash application arguments")
parser.add_argument("-f", "--File", help = "The CSV data file", required = False, default = "crash_data.csv")     
argument = parser.parse_args()
data_file = argument.File

data = CrashData(data_file)  # load the data and compute metadata
df = data.df        # the dataframe containing the crash data

# create the dash application using the above layout definition
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# mapping each crash type to a colour using the predefined palette
color_discrete_map = dict(zip(data.crashtype_list, px.colors.qualitative.Plotly[:len(data.crashtype_list)]))

""" Create a figure containing the map layer superimposed with the car crashes data
    Parameters are for the data filtering according to the year range (year_range)
    and the crash type (type_list)
"""
@app.callback(
    Output('mapbox', 'figure'),
    [
        Input('year-range-slider', 'value'),
        Input('type-check-list', 'value')
    ])
def plot_crash_location(year_range, type_list):
    # filter
    pdf = df[(df['Crash_Year'] >= year_range[0]) & (df['Crash_Year'] <= year_range[1]) & (df['Crash_Type'].isin(type_list))]
    # create the interactive map
    fig = px.scatter_mapbox(pdf, lat=pdf['Crash_Latitude'], lon=pdf['Crash_Longitude'], color='Crash_Type', 
        zoom=8, height=600, title=None, opacity=.5, 
        color_discrete_map=color_discrete_map,
        center={'lat': data.center_lat, 'lon': data.center_long}
        )
    fig.update_layout(mapbox_style='open-street-map', margin={"r": 0, "l": 0, "b": 20})
    fig['layout']['uirevision'] = 'unchanged' # to preseve the ui setting such as zoom and panning in the update
    return fig 

""" Create the layout of the web-based dashboard using dash bootstrap components and dash core components
"""
rows = html.Div(
    [
        dbc.Row(dbc.Col(html.Div([
            html.H3(id = 'title', children = 'Crash Locations'),
            html.H5(id = 'subtitle', children = 'Based on dataset from Department of Transport and Main Roads, Queensland Government'),
        ], style = {'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}))),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    id='div-sidebar', children = [
                        dbc.Card(dbc.CardBody([
                            html.H6(children = 'Years'),
                            dcc.RangeSlider(data.year_min, data.year_max, 1,
                            value=[data.year_min, data.year_max],
                            marks={data.year_min: str(data.year_min), data.year_max: str(data.year_max)},
                            id='year-range-slider'),
                            html.Div(id='year-range-text')])
                        ),
                        dbc.Card(dbc.CardBody(
                            [
                            html.H6(children = 'Crash Types'),
                            dbc.Checklist(data.crashtype_list, data.crashtype_list, id ='type-check-list')
                            ])
                        )
                    ], style={'marginLeft': 20, 'marginRight': 20}), width=3),
                dbc.Col(html.Div(id='div-body',children = [
                    dcc.Graph(id = 'mapbox')
                ]), width=9),
            ]
        ),
    ]
)
app.layout = dbc.Container(rows, fluid=True) # the dbc container is essential as the root for other dbc layout

""" the callback function for updating the year range slider
"""
@app.callback(
    Output('year-range-text', 'children'),
    [Input('year-range-slider', 'value')])
def update_output(value):
    return 'From {} to {}'.format(value[0], value[1])

""" start the web application
    the host IP 0.0.0.0 is needed for dockerized version of this dash application
"""
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)
    server = app.server # required for some deployment environment like Heroku