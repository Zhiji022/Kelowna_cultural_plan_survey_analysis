# module to create callback for activity barplot
from dash.dependencies import Input, Output, State
import sys
from plotly import graph_objs as go

# app server
sys.path.append('../..')
from server import app

# data loaders
from dataloaders.CultureCentreVisitors import cul_topic

#############################################################
# Callback Function
#############################################################

@app.callback(
    Output('topic_distribution','figure'),
    [Input('culture_participation_map','clickData')],
    [State('topic_distribution', 'figure')])
def topic_distribution(centre, existing_state):
    if centre != None:
        text = centre['points'][0]['text'].split('<br>')[0]
        if (not text.startswith('V')) or (len(text) != 7):
            topic_centre = cul_topic[cul_topic['Culture Centre'] == text]
        else:
            return existing_state
    else:
        topic_centre = cul_topic[cul_topic['Culture Centre'] == 'Rotary Centre for the Arts']

    return {
        'data':[
            go.Bar(
                x=["Performing Arts","Concerts/<br>Outdoor Activities","Visual Arts"],
                y=topic_centre['#vistors'],
                width = 0.5,
                marker = {'color':'#031884'}
                )
                ],
        'layout': go.Layout(
            autosize = True,
            xaxis = {
                    'title':'<b>Activity</b>',
                    'showgrid':False
                    },
            yaxis = {
                    'title':'<b>No. of<br>Participants</b>',
                    'showticklabels':True,
                    'range':[0,25]
                    },
            margin = dict(t = 5, l = 80, r = 5, b = 110),
            height = 220,
            width = 400,
            )

    }
