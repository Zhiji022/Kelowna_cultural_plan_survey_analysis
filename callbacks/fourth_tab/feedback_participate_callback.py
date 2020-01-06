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
from configs.MLPredictionLabels import how_participate_labels

#############################################################
# Data Preparation
#############################################################
def get_grouped_how_participate():
    df = pd.DataFrame(get_feedback_table_data())
    df = df[df['Age'] != 'Undisclosed']
    df = df[df['Gender'] != 'Undisclosed']
    df = df[df['Participate Label'].astype(str).str.isnumeric()]
    df = df.groupby(['Gender', 'Age', 'Participate Label']).size()
    df = df.reset_index().rename(columns = {0: 'Count'})
    df = df.astype({'Gender': 'object', 'Age': 'object', 'Participate Label': 'int64', 'Count': 'int64'})

    female_df = df[df['Gender'] == 'Female']
    male_df = df[df['Gender'] == 'Male']

    Age = list(df.Age.unique())
    Cluster = list(df['Participate Label'].unique())
    all_gender_df = pd.DataFrame(list(product(Age, Cluster)), columns = ['Age', 'Participate Label'])

    male_df = all_gender_df.merge(male_df, how = 'left', on = ['Age', 'Participate Label'])
    male_df = male_df[['Age', 'Participate Label', 'Count']]
    male_df = male_df.fillna(0)
    male_df.sort_values(by = 'Age', inplace = True)

    female_df = all_gender_df.merge(female_df, how='left', on=['Age', 'Participate Label'])
    female_df = female_df[['Age', 'Participate Label', 'Count']]
    female_df = female_df.fillna(0)
    female_df.sort_values(by = 'Age', inplace = True)

    return (male_df.copy(), female_df.copy())

#############################################################
# Callback Functions
#############################################################
@app.callback([Output('feedback_participate_male_bar', 'figure'),
               Output('feedback_participate_female_bar', 'figure')],
              [Input('refresh_feedback_table_button', 'n_clicks')])
def feedback_participate_bars_callback(n_clicks):
    colours = ['#A60808', '#0229A8', '#1F9910', '#BB14C0', '#D1D021']
    genders = ['Males', 'Females']
    df_list = get_grouped_how_participate()
    callback_outputs = []

    for i, df in enumerate(df_list):
        data = []
        x = list(df['Age'].unique())
        label_list = sorted(list(df['Participate Label'].unique()))
        y_list = [list(df[df['Participate Label'] == i]['Count']) for i in label_list]

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
                            name = how_participate_labels[label_list[j] - 1],
                            opacity = 0.9
                    )
            )

        layout = go.Layout(
                    autosize = True,
                    hovermode = 'closest',
                    title = f'Cultural participation by Age Groups for {genders[i]}',
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
                    margin = dict(t = 120, l = 60, r = 0, b = 50),
                    legend = dict(
                                x = 0.5,
                                y = 1.21,
                                bgcolor = '#E2E2E2',
                                bordercolor = '#FFFFFF',
                                borderwidth = 2,
                            ),
                    showlegend = True
                 )

        callback_outputs.append(go.Figure(data = data, layout = layout))

    return callback_outputs
