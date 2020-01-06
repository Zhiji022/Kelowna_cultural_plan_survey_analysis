# module to create callback for visitors/distance scatter plot
from dash.dependencies import Input, Output, State
import sys
from plotly import graph_objs as go

# app server
sys.path.append('../..')
from server import app

# data loaders
from dataloaders.CultureCentreDistances import centre_distances_vistors

#############################################################
# Callback Function
#############################################################

@app.callback(
    Output('visitors_distances','figure'),
    [Input('culture_participation_map','clickData')],
    [State('visitors_distances', 'figure')])
def visitor_distances(centre, existing_state):
    if centre != None:
        text = centre['points'][0]['text'].split('<br>')[0]
        if (not text.startswith('V')) or (len(text) != 7):
            ctr = text
        else:
            return existing_state
    else:
        ctr = 'Rotary Centre for the Arts'


    return {
        'data': [
            go.Scatter(
                x = centre_distances_vistors[centre_distances_vistors['Culture Centre'] != ctr]['mean'],
                y = centre_distances_vistors[centre_distances_vistors['Culture Centre'] != ctr]['count'],
                hoverinfo = 'text',
                text = centre_distances_vistors[centre_distances_vistors['Culture Centre']!=ctr]['Culture Centre'] + '<br>Avg. Distance: ' + \
                        centre_distances_vistors[centre_distances_vistors['Culture Centre']!=ctr]['mean'].apply(lambda x: round(x, 2)).astype(str) + ' kms<br>No. of Visitors: ' + centre_distances_vistors[centre_distances_vistors['Culture Centre']!=ctr]['count'].astype(str),
                mode = 'markers',
                marker = {
                    'size' : 10,
                    'color' : '#031884',
                    'line' : {'width': 1}
                    },
                showlegend = False

            ),
            go.Scatter(
                x = centre_distances_vistors[centre_distances_vistors['Culture Centre']==ctr]['mean'],
                y = centre_distances_vistors[centre_distances_vistors['Culture Centre']==ctr]['count'],
                text = centre_distances_vistors[centre_distances_vistors['Culture Centre']==ctr]['Culture Centre'] + '<br>Avg. Distance: ' + \
                        centre_distances_vistors[centre_distances_vistors['Culture Centre']==ctr]['mean'].apply(lambda x: round(x, 2)).astype(str) + ' kms<br>No. of Visitors: ' + centre_distances_vistors[centre_distances_vistors['Culture Centre']==ctr]['count'].astype(str),
                hoverinfo = 'text',
                mode = 'markers',
                marker = {
                    'size' : 15,
                    'color' : '#C83F34',

                    },
                showlegend = False
            ),
        ],
        'layout': go.Layout(
            autosize = True,
            xaxis = {'title':'<b>Average Travel Distance (kms)</b>', 'range': [0, 26], 'zeroline':False},
            yaxis = {'title': '<b>Total No.<br>of Visitors</b>', 'range': [0, 65], 'zeroline':False},
            hovermode = 'closest',
            margin = dict(t = 8, l = 80, r = 5, b = 35),
            height = 220,
            width = 400
        )
    }
