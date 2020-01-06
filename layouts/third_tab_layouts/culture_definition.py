# module to create callback for age group filter for cultural participation
import dash_table
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html

# data loaders
from dataloaders.CultureDefinition import culture_definition

# configs
from configs.DashConfigs import graph_config_style
from configs.MLPredictionLabels import definition_labels

#############################################################
# Figure Creation Functions
#############################################################
def get_culture_def_table():
    data_table = dash_table.DataTable(
                            columns=[{'name': 'How does the community define culture?', 'id': 'Topic'}],
                            data = [{'Topic': item} for item in definition_labels],
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

def get_culture_def_scatterplot():
    data = []
    colours = ['#A60808', '#0229A8', '#038D08', '#676250', '#AC25B6']

    for i in sorted(culture_definition['Topic_LDA'].unique()):
        cluster = culture_definition[culture_definition['Topic_LDA'] == i]
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
                name = definition_labels[i - 1]
            )
        ]
        data = data + trace

    layout = go.Layout(
                autosize = True,
                hovermode = 'closest',
                title = go.layout.Title(text = 'Groupings based on how the community defines culture'),
                margin = dict(t = 40, l = 0, r = 0, b = 0),
                legend = dict(
                            x = 0.7,
                            y = 0.8,
                            bgcolor = '#E2E2E2',
                            bordercolor = '#FFFFFF',
                            borderwidth = 2,
                        ),
                xaxis = dict(zeroline = False, showline = False),
                yaxis = dict(zeroline = False, showline = False)
             )

    fig = dcc.Graph(figure = go.Figure(data = data, layout = layout), config = graph_config_style)
    return html.Div([html.Hr(), fig], style={'padding-left': 15, 'width': '70vw', 'height': '60vh', 'padding-top': 30, 'padding-bottom': 100})
