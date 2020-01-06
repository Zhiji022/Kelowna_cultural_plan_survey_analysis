import plotly.graph_objs as go
import sys
from itertools import product
import pandas as pd
from dash.dependencies import Input, Output

# app server
sys.path.append('../..')

# configs
from server import app
from configs.GoogleSpreadsheets import get_feedback_table_data
from configs.MLPredictionLabels import facility_needs_labels
from configs.DashConfigs import mapbox_access_token

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

def format_hover_text(response):
    text = ""
    for i, word in enumerate(response.split()):
        text = text + word + " "
        if(i % 10 == 0 and i != 0):
            text = text + "<br>"
    return text

def get_grouped_facility_needs():
    df = pd.DataFrame(get_feedback_table_data())
    df = df[df['Age'] != 'Undisclosed']
    df = df[df['Gender'] != 'Undisclosed']
    df = df[df['Facility Label'].astype(str).str.isnumeric()]
    df = df.groupby(['Gender', 'Age', 'Facility Label']).size()
    df = df.reset_index().rename(columns = {0: 'Count'})
    df = df.astype({'Gender': 'object', 'Age': 'object', 'Facility Label': 'int64', 'Count': 'int64'})

    female_df = df[df['Gender'] == 'Female']
    male_df = df[df['Gender'] == 'Male']

    Age = list(df.Age.unique())
    Cluster = list(df['Facility Label'].unique())
    all_gender_df = pd.DataFrame(list(product(Age, Cluster)), columns = ['Age', 'Facility Label'])

    male_df = all_gender_df.merge(male_df, how = 'left', on = ['Age', 'Facility Label'])
    male_df = male_df[['Age', 'Facility Label', 'Count']]
    male_df = male_df.fillna(0)
    male_df.sort_values(by = 'Age', inplace = True)

    female_df = all_gender_df.merge(female_df, how='left', on=['Age', 'Facility Label'])
    female_df = female_df[['Age', 'Facility Label', 'Count']]
    female_df = female_df.fillna(0)
    female_df.sort_values(by = 'Age', inplace = True)

    return (male_df.copy(), female_df.copy())

#############################################################
# Callback Functions
#############################################################
@app.callback(Output('feedback_facilities_map', 'figure'),
              [Input('refresh_feedback_table_button', 'n_clicks')])
def feedback_facility_map_callback(n_clicks):
    df = pd.DataFrame(get_feedback_table_data())
    df = df[df['Facility Sentiment'].apply(lambda x: isinstance(x, (float, int)))]

    # colourscale
    scl = [[0.0, '#E12A0A'], [0.1, '#E12A0A'], [0.2, '#E09006'], [0.3, '#E09006'],
           [0.4, '#E0D806'], [0.5, '#E0D806'], [0.6, '#89F972'],
           [0.7, '#89F972'], [0.8, '#27BC14'], [0.9, '#27BC14'], [1.0, '#27BC14']]

    tick_vals = [-0.96, -0.75, -0.60, -0.45, -0.3, -0.15, 0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.96]
    tick_labels = ["<b>Negative</b>", "-0.75", "-0.60", "-0.45", "-0.30", "-0.15", "0", "0.15", "0.30", "0.45", "0.60", "0.75", "<b>Positive</b>"]

    data = [
        go.Scattermapbox(
            lat = df['Latitude'],
            lon = df['Longitude'],
            mode = 'markers',
            marker = dict(
                        size = 12,
                        opacity = 1,
                        colorscale = scl,
                        autocolorscale = False,
                        color = df['Facility Sentiment'],
                        colorbar = dict(title = 'Satisfaction',
                                        tickmode = "array",
                                        tickvals = tick_vals,
                                        ticktext = tick_labels),
                        cmin = -1.0,
                        cmax = 1.0
                    ),
            hoverinfo = 'text',
            text = 'Sentiment: ' + df['Facility Sentiment'].apply(get_sentiment) + '<br>Score: ' + df['Facility Sentiment'].apply(lambda x: round(x, 3)).astype(str) + \
                        '<br>Postal Code: ' + df['Postal Code'] + '<br>Gender: ' + df['Gender'] + '<br>Age Group: ' + df['Age'] + '<br><br>' + df['Status of Facilities'].apply(format_hover_text),
            showlegend = False
        )
    ]

    layout = go.Layout(
        autosize = True,
        hovermode = 'closest',
        title = go.layout.Title(text = 'How satisfied is the community with cultural facilities?'),
        mapbox = go.layout.Mapbox(
            accesstoken = mapbox_access_token,
                center = go.layout.mapbox.Center(
                    lat = 49.8866,
                    lon = -119.4788,
            ),
            style = 'light',
            pitch = 0,
            zoom = 10,
            bearing = 0
        ),
        margin = dict(t = 40, l = 0, r = 0, b = 0)
    )

    return go.Figure(data = data, layout = layout)

@app.callback([Output('feedback_facilities_male_bar', 'figure'),
               Output('feedback_facilities_female_bar', 'figure')],
              [Input('refresh_feedback_table_button', 'n_clicks')])
def feedback_facilities_bars_callback(n_clicks):
    colours = ['#A60808', '#0229A8', '#1F9910', '#BB14C0', '#D1D021']
    genders = ['Males', 'Females']
    df_list = get_grouped_facility_needs()
    callback_outputs = []

    for i, df in enumerate(df_list):
        data = []
        x = list(df['Age'].unique())
        label_list = sorted(list(df['Facility Label'].unique()))
        y_list = [list(df[df['Facility Label'] == i]['Count']) for i in label_list]

        for j, y in enumerate(y_list):
            data.append(
                    go.Bar(
                            x = x,
                            y = y,
                            hoverinfo = 'text',
                            text = [int(item) for item in y],
                            textposition = 'auto',
                            marker = dict(
                                         color = colours[label_list[j] - 1],
                                         line = dict(
                                                    color = '#726F6D',
                                                    width = 1.5
                                                    ),
                                         ),
                            name = facility_needs_labels[label_list[j] - 1],
                            opacity = 0.9
                    )
            )

        layout = go.Layout(
                    autosize = True,
                    hovermode = 'closest',
                    title = f'Facility Needs by Age Groups for {genders[i]}',
                    xaxis=dict(
                            tickfont=dict(
                                    size=14,
                                    color='rgb(107, 107, 107)'
                                    ),
                                    title = 'Age Groups'
                            ),
                    yaxis=dict(
                            tickfont=dict(
                                    size=14,
                                    color='rgb(107, 107, 107)'
                                    ),
                                    title = 'Count'
                            ),
                    margin = dict(t = 170, l = 60, r = 0, b = 50),
                    legend = dict(
                                x = 0.7,
                                y = 1.35,
                                bgcolor = '#E2E2E2',
                                bordercolor = '#FFFFFF',
                                borderwidth = 2,
                            ),
                    showlegend = True
                 )

        callback_outputs.append(go.Figure(data = data, layout = layout))

    return callback_outputs
