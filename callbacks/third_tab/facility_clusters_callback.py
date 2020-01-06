# module to create callback for age group filter for cultural participation
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import sys

# app server
sys.path.append('../..')
from server import app

# data loaders
from dataloaders.FacilityNeeds import facility_needs

# configs
from configs.MLPredictionLabels import facility_needs_labels

#############################################################
# Callback Functions
#############################################################
@app.callback(Output('facility_clusters_scatterplot', 'figure'),
              [Input('facility_sentiment_map', 'clickData')])
def facility_scatterplot_callback(click_data):
    if(click_data != None):
        df_required = facility_needs[facility_needs['Organization'] == str(click_data['points'][0]['text'].split('<br>')[0])]
    else:
        df_required = facility_needs

    data = []
    colours = ['#A60808', '#0229A8', '#038D08', '#676250']

    for i in sorted(df_required['Cluster'].unique()):
        cluster = df_required[df_required['Cluster'] == i]
        trace = [
            go.Scatter(
                x = cluster['X'],
                y = cluster['Y'],
                mode = 'markers',
                marker = dict(
                            size = 12,
                            opacity = 0.6,
                            color = colours[i - 1]),
                hoverinfo = 'text',
                text = '<b>' + cluster['Organization'] + '</b>' + '<br><br>' + cluster['Response'].str.capitalize(),
                showlegend = True,
                name = facility_needs_labels[i - 1]
            )
        ]
        data = data + trace

    layout = go.Layout(
                autosize = True,
                hovermode = 'closest',
                title = go.layout.Title(text = 'Groupings based on responses'),
                margin = dict(t = 40, l = 0, r = 0, b = 0),
                legend = dict(
                            x = 0.6,
                            y = 1,
                            bgcolor = '#E2E2E2',
                            bordercolor = '#FFFFFF',
                            borderwidth = 2,
                        ),
                xaxis = dict(zeroline = False, showline = False),
                yaxis = dict(zeroline = False, showline = False)
             )

    return go.Figure(data = data, layout = layout)

@app.callback(Output('reset_facility_clusters_scatterplot', 'style'),
              [Input('facility_sentiment_map', 'clickData')])
def facility_clusters_reset_button_callback(click_data):
    if click_data == None:
        return {'background-color': 'white', 'color': 'black', 'visibility': 'hidden'}
    else:
        return {'background-color': 'white', 'color': 'black'}
