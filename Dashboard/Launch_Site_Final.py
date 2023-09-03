# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
df_baru=spacex_df[:]
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',  options=  [                        
                                {'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                ], value="ALL", placeholder="place holder here", searchable=True),
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0',
                                       100: '100'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# # Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# @app.callback(
#     Output(component_id='success-pie-chart',component_property="figure"),
#     Input(component_id='site-dropdown', component_property='value'))

# def get_pie_chart(drop):
#     if drop == 'ALL':
#         data=spacex_df.loc[spacex_df["class"]==1].groupby("Launch Site")["Flight Number"].count().reset_index()
#         figure = px.pie(data, values='Flight Number',names="Launch Site", 
#         title='successed-ALL')
#         return figure
#     else:
#         data=spacex_df.loc[spacex_df["Launch Site"]==drop].groupby("class").count().reset_index()
#         fig=px.pie(data,values='Flight Number',names='class',
#         title='successed vs failed "{value}"')
#         return figure

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(drop):
    if drop == 'ALL':
        data = spacex_df.loc[spacex_df["class"] == 1].groupby("Launch Site")["class"].sum().reset_index()
        fig = px.pie(data, values='class', names="Launch Site", title='Successes - ALL')
        return fig
    else:
        data = spacex_df.loc[spacex_df["Launch Site"] == drop].groupby("class")["Launch Site"].count().reset_index()
        fig = px.pie(data, values='Launch Site', names='class', title=f'Successes vs Failures - {drop}')
        return fig

# @app.callback(
#     Output(component_id="success-payload-scatter-chart",component_property="figure"),
#     [Input(component_id="site-dropdown",component_property="value"),Input(component_id="slider",component_property="value")])
# def scatter(site,slide):
#     if site=="ALL":
#         data=df_baru
#         fig=px.scatter(data,x="Payload Mass (kg)",y="class",color="Booster Version Category")
#         return fig
#     else:
#         data=df_baru.loc[df_baru["Launch Site"]==site].loc[df_baru["Payload Mass (kg)"]==slide]
#         fig=px.scatter(data,x="Payload Mass (kg)",y="class",color="Booster Version Category")
#         return fig
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [Input(component_id="site-dropdown", component_property="value"),
     Input(component_id="slider", component_property="value")])
def scatter(site, slide):
    if site == "ALL":
        data = df_baru
    else:
        data = df_baru.loc[df_baru["Launch Site"]==site].loc[df_baru["Payload Mass (kg)"]>=slide[0]].loc[df_baru["Payload Mass (kg)"]<=slide[1]]
    
    fig = px.scatter(data, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
