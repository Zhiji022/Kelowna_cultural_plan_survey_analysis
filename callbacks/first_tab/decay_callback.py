# module to create callback for visitors/distance scatter plot
from dash.dependencies import Input, Output, State
import sys
from plotly import graph_objs as go
# app server
sys.path.append('../..')
from server import app

# data loaders
from dataloaders.CultureCentreDistances import cumul_distances_visitor

#############################################################
# Callback Function
#############################################################

@app.callback(
    Output('decay_plot','figure'),
    [Input('culture_participation_map','clickData')],
    [State('decay_plot', 'figure')])
def decay_plot(centre, existing_state):
    if centre != None:
        text = centre['points'][0]['text'].split('<br>')[0]
        if (not text.startswith('V')) or (len(text) != 7):
            decay_centre = cumul_distances_visitor[cumul_distances_visitor['Culture Centre'] == text]
        else:
            return existing_state
    else:
        decay_centre = cumul_distances_visitor[cumul_distances_visitor['Culture Centre'] == 'Rotary Centre for the Arts']

    return {
        'data':[
            go.Scatter(
                x=decay_centre['Distance (kms)'],
                y=decay_centre['cumul#vistors'],
                text = 'Distance: ' + decay_centre['Distance (kms)'].apply(lambda x: round(x, 2)).astype(str) + ' kms<br>Total Visitors: ' + decay_centre['cumul#vistors'].astype(str),
                hoverinfo= 'text',
                mode = 'lines+markers',
                marker = {'color' : '#C83F34'}
            )
                    ],
        'layout': go.Layout(
            autosize = True,
            xaxis = {'title':'<b>Distance from Facility (kms)</b>', 'range': [0, 26], 'zeroline':False},
            yaxis = {'title': '<b>Cumulative No.<br>of Visitors</b>', 'range': [0, 50], 'zeroline':False},
            hovermode = 'closest',
            margin = dict(t = 5, l = 80, r = 5, b = 35),
            height = 220,
            width = 400,
            modebar = dict(orientation = 'v')
            )

    }
