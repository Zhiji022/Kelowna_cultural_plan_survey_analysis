# module to create callback for age group filter for cultural participation
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table

# data loaders
from dataloaders.FacilityNeeds import facility_needs

# configs
from configs.DashConfigs import graph_config_style, mapbox_access_token
from configs.MLPredictionLabels import facility_needs_labels

#############################################################
# Data Preparation
#############################################################
def get_sentiment(score):
    if(score > 0):
        return "Positive"
    elif(score == 0):
        return "Neutral"
    else:
        return "Negative"

grouped_facility_sentiment = pd.DataFrame(facility_needs.groupby(['Organization', 'Postal Code', 'Latitude', 'Longitude'])['Score'].mean().sort_values()).reset_index()
grouped_facility_sentiment['Sentiment'] = grouped_facility_sentiment['Score'].apply(get_sentiment)

#############################################################
# Figure Creation Functions
#############################################################
def get_facility_sentiment_map():
    # colourscale
    scl = [[0.0, '#E12A0A'], [0.1, '#E12A0A'], [0.2, '#E09006'], [0.3, '#E09006'],
           [0.4, '#E0D806'], [0.5, '#E0D806'], [0.6, '#89F972'],
           [0.7, '#89F972'], [0.8, '#27BC14'], [0.9, '#27BC14'], [1.0, '#27BC14']]

    tick_vals = [-0.8, -0.60, -0.45, -0.3, -0.15, 0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.95]
    tick_labels = ["<b>Negative</b>", "-0.60", "-0.45", "-0.30", "-0.15", "0", "0.15", "0.30", "0.45", "0.60", "0.75", "<b>Positive</b>"]

    data = [
        go.Scattermapbox(
            lat = grouped_facility_sentiment['Latitude'],
            lon = grouped_facility_sentiment['Longitude'],
            mode = 'markers',
            marker = dict(
                        size = 12,
                        opacity = 1,
                        colorscale = scl,
                        autocolorscale = False,
                        color = grouped_facility_sentiment['Score'],
                        colorbar = dict(title = 'Satisfaction',
                                        tickmode = "array",
                                        tickvals = tick_vals,
                                        ticktext = tick_labels),
                        cmin = -0.82,
                        cmax = 0.98
                    ),
            hoverinfo = 'text',
            text = grouped_facility_sentiment['Organization'] + '<br>Sentiment: ' + grouped_facility_sentiment['Sentiment'] + '<br>Score: ' + grouped_facility_sentiment['Score'].apply(lambda x: round(x, 3)).astype(str),
            showlegend = False
        )
    ]

    layout = go.Layout(
        autosize = True,
        hovermode = 'closest',
        title = go.layout.Title(text = 'How satisfied are organizations with cultural facilities?'),
        mapbox = go.layout.Mapbox(
            accesstoken = mapbox_access_token,
                center = go.layout.mapbox.Center(
                    lat = 49.8866,
                    lon = -119.4788,
            ),
            style = 'light',
            pitch = 0,
            zoom = 13,
            bearing = 0
        ),
        margin = dict(t = 40, l = 0, r = 0, b = 0)
    )

    fig = dcc.Graph(id = 'facility_sentiment_map', figure = go.Figure(data = data, layout = layout), config = graph_config_style)
    return html.Div([fig], style={'padding-left': 15, 'width': '70vw', 'height': '60vh', 'padding-top': 17})

def get_sentiment_scatterplot():
    fig = dcc.Graph(id = 'facility_sentiment_scatterplot', config = graph_config_style)
    return html.Div([html.Hr(), html.Button('RESET', id = 'reset_facility_sentiment_scatterplot'), fig], style={'padding-left': 15, 'width': '70vw', 'height': '60vh', 'padding-top': 40})

def get_clusters_table():
    data_table = dash_table.DataTable(
                            columns = [{'name': 'What are the main facility needs of cultural organizations?', 'id': 'Cluster'}],
                            data = [{'Cluster': item} for item in facility_needs_labels],
                            style_cell = {'textAlign': 'center','padding': '5px', 'font-size': 17},
                            style_as_list_view = True,
                            style_header = {
                                    'fontWeight': 'bold',
                                    'font-size':17,
                                    'backgroundColor': '#7BE0F1',
                                    'textAlign': 'center'
                            },
                            style_table={'width': '60vw'},
                        )

    return html.Div([html.Hr(), data_table], style={'padding-left': 120, 'padding-top': 125})

def get_clusters_scatterplot():
    fig = dcc.Graph(id = 'facility_clusters_scatterplot', config = graph_config_style)
    return html.Div([html.Hr(), html.Button('RESET', id = 'reset_facility_clusters_scatterplot'), fig], style={'padding-left': 15, 'width': '70vw', 'height': '60vh', 'padding-top': 30, 'padding-bottom': 130})
