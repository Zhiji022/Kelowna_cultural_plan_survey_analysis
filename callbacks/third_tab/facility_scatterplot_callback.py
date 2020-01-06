# module to create callback for age group filter for cultural participation
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import sys

# app server
sys.path.append('../..')
from server import app

# data loaders
from dataloaders.FacilityNeeds import facility_needs

#############################################################
# Callback Function
#############################################################

@app.callback(Output('facility_sentiment_scatterplot', 'figure'),
              [Input('facility_sentiment_map', 'clickData')])
def facility_scatterplot_callback(click_data):
    if(click_data != None):
        df_required = facility_needs[facility_needs['Organization'] == str(click_data['points'][0]['text'].split('<br>')[0])]
    else:
        df_required = facility_needs

    tick_vals = [-0.8, -0.60, -0.45, -0.3, -0.15, 0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.95]
    tick_labels = ["<b>Negative</b>", "-0.60", "-0.45", "-0.30", "-0.15", "0", "0.15", "0.30", "0.45", "0.60", "0.75", "<b>Positive</b>"]

    # colourscale
    scl = [[0.0, '#E12A0A'], [0.1, '#E12A0A'], [0.2, '#E09006'], [0.3, '#E09006'],
           [0.4, '#E0D806'], [0.5, '#E0D806'], [0.6, '#89F972'],
           [0.7, '#89F972'], [0.8, '#27BC14'], [0.9, '#27BC14'], [1.0, '#27BC14']]

    data = [
        go.Scatter(
            x = df_required['X'],
            y = df_required['Y'],
            mode = 'markers',
            marker = dict(
                        size = 12,
                        opacity = 1,
                        colorscale = scl,
                        autocolorscale = False,
                        color = df_required['Score'],
                        colorbar = dict(title = 'Satisfaction',
                                        tickmode = "array",
                                        tickvals = tick_vals,
                                        ticktext = tick_labels),
                        cmin = -0.82,
                        cmax = 0.98
                        ),
        hoverinfo = 'text',
        text = df_required['Organization'] + '<br>Sentiment: ' + df_required['Sentiment'] + '<br>Score: ' + \
                df_required['Score'].apply(lambda x: round(x, 3)).astype(str) + '<br><br>' + df_required['Response'].apply(lambda x: x.capitalize()),
        showlegend = False
        )
    ]

    layout = go.Layout(
                autosize = True,
                hovermode = 'closest',
                title = go.layout.Title(text = 'Sentiment based on responses'),
                margin = dict(t = 40, l = 0, r = 0, b = 0),
                xaxis = dict(zeroline = False, showline = False),
                yaxis = dict(zeroline = False, showline = False)
             )

    return go.Figure(data = data, layout = layout)

@app.callback(Output('reset_facility_sentiment_scatterplot', 'style'),
              [Input('facility_sentiment_map', 'clickData')])
def facility_sentiment_reset_button_callback(click_data):
    if click_data == None:
        return {'background-color': 'white', 'color': 'black', 'visibility': 'hidden'}
    else:
        return {'background-color': 'white', 'color': 'black'}

@app.callback(Output('facility_sentiment_map', 'clickData'),
              [Input('reset_facility_sentiment_scatterplot', 'n_clicks'),
               Input('reset_facility_clusters_scatterplot', 'n_clicks')])
def reset_click_data_callback(sentiment_nclicks, clusters_nclicks):
    return None