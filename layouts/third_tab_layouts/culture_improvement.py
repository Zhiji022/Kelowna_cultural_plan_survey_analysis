# module to create callback for age group filter for cultural participation
import dash_table
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from itertools import product

# data loaders
from dataloaders.CultureImprovement import culture_improvement

# configs
from configs.DashConfigs import graph_config_style
from configs.MLPredictionLabels import improvement_labels

#############################################################
# Data Preparation
#############################################################
def get_grouped_improvement():
    df = culture_improvement.dropna().copy()
    df = df[df['Age'] != 'Prefer not to disclose']
    df = df[df['Gender'] != 'Prefer not to disclose']
    df = df[df['Topic'].astype(str).str.isnumeric()]
    df = df.groupby(['Gender', 'Age', 'Topic']).size()
    df = df.reset_index().rename(columns = {0: 'Count'})
    df = df.astype({'Gender': 'object', 'Age': 'object', 'Topic': 'int64', 'Count': 'int64'})

    female_df = df[df['Gender'] == 'Female']
    male_df = df[df['Gender'] == 'Male']

    Age = list(df.Age.unique())
    Topic = list(df['Topic'].unique())
    all_gender_df = pd.DataFrame(list(product(Age, Topic)), columns = ['Age', 'Topic'])

    male_df = all_gender_df.merge(male_df, how = 'left', on = ['Age', 'Topic'])
    male_df = male_df[['Age', 'Topic', 'Count']]
    male_df = male_df.fillna(0)
    male_df.sort_values(by = 'Age', inplace = True)

    female_df = all_gender_df.merge(female_df, how='left', on=['Age', 'Topic'])
    female_df = female_df[['Age', 'Topic', 'Count']]
    female_df = female_df.fillna(0)
    female_df.sort_values(by = 'Age', inplace = True)

    return (male_df.copy(), female_df.copy())

#############################################################
# Figure Creation Functions
#############################################################
def get_culture_improvement_table():
    data_table = dash_table.DataTable(
                            columns=[{'name': 'How can arts, culture and heritage be improved in Kelowna?', 'id': 'Topic'}],
                            data = [{'Topic': item} for item in improvement_labels],
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

    return html.Div([data_table], style={'padding-left': 120, 'padding-top': 17})

def get_culture_improvement_scatterplot():
    data = []
    colours = ['#A60808', '#0229A8', '#038D08', '#676250', '#AC25B6']

    for i in sorted(culture_improvement['Topic'].unique()):
        cluster = culture_improvement[culture_improvement['Topic'] == i]
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
                text = cluster['Response'].str.capitalize(),
                showlegend = True,
                name = improvement_labels[i - 1]
            )
        ]
        data = data + trace

    layout = go.Layout(
                autosize = True,
                hovermode = 'closest',
                title = go.layout.Title(text = 'Groupings based on suggestions for improvements'),
                margin = dict(t = 40, l = 0, r = 0, b = 0),
                legend = dict(
                            x = 0.7,
                            y = 1,
                            bgcolor = '#E2E2E2',
                            bordercolor = '#FFFFFF',
                            borderwidth = 2,
                        ),
                xaxis = dict(zeroline = False, showline = False),
                yaxis = dict(zeroline = False, showline = False)
             )

    fig = dcc.Graph(figure = go.Figure(data = data, layout = layout), config = graph_config_style)
    return html.Div([html.Hr(), fig], style={'padding-left': 15, 'width': '70vw', 'height': '60vh', 'padding-top': 30, 'padding-bottom': 100})

def get_culture_improvement_bars():
    colours = ['#A60808', '#0229A8', '#1F9910', '#BB14C0', '#D1D021']
    genders = ['Males', 'Females']
    df_list = get_grouped_improvement()
    graph_outputs = []

    for i, df in enumerate(df_list):
        data = []
        x = list(df['Age'].unique())
        label_list = sorted(list(df['Topic'].unique()))
        y_list = [list(df[df['Topic'] == i]['Count']) for i in label_list]

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
                            name = improvement_labels[label_list[j] - 1],
                            opacity = 0.9
                    )
            )

        layout = go.Layout(
                    autosize = True,
                    hovermode = 'closest',
                    title = f'Suggestions for improvements by Age Groups for {genders[i]}',
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
                    margin = dict(t = 80, l = 60, r = 0, b = 50),
                    legend = dict(
                                x = 0.7,
                                y = 1.1,
                                bgcolor = '#E2E2E2',
                                bordercolor = '#FFFFFF',
                                borderwidth = 2,
                            ),
                    showlegend = True
                 )

        graph_outputs.append(dcc.Graph(figure = go.Figure(data = data, layout = layout), config = graph_config_style))

    div_style = {'padding-left': 15, 'width': '70vw', 'height': '60vh', 'padding-top': 30, 'padding-bottom': 100}
    return [html.Div([html.Hr(), item], style = div_style) for item in graph_outputs]
