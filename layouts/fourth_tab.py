# layout for the fourth tab of the dashboard

# built-in modules
import dash_table
import dash_core_components as dcc
import dash_html_components as html

# configs
from configs.DashConfigs import graph_config_style, selected_tab_style, selected_side_tab_style

#############################
# Dash Layout
#############################
def get_tab_layout():
    return dcc.Tab(label = "Community Feedback",
                   children = [dash_table.DataTable(
                                                    id = 'feedback_table',
                                                    columns = [],
                                                    data = [],
                                                    style_as_list_view = False,
                                                    sorting=True,
                                                    style_header = {
                                                        'fontWeight': 'bold',
                                                        'fontSize': '15',
                                                        'backgroundColor': '#7BE0F1',
                                                        'textAlign': 'center'
                                                    },
                                                    style_table={'overflowX': 'scroll', 'overflowY': 'scroll', 'maxHeight': '50vh', 'padding-top': 15},
                                                    style_cell={
                                                        'minWidth': '0px', 'maxWidth': '500px',
                                                        'whiteSpace': 'normal', 'textAlign': 'left'
                                                    },
                                                    css=[{
                                                        'selector': '.dash-cell div.dash-cell-value',
                                                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                                    }]
                                                    ),

                               html.Div([html.Button('REFRESH', id = 'refresh_feedback_table_button'),
                                         html.A(html.Button('DOWNLOAD', id = 'download_feedback_table_button'), href = '/feedback_table/')
                                         ]),

                               dcc.Tabs(vertical = True,
                                        children = [dcc.Tab(label = "Status of Facilities",
                                                            children = [dcc.Graph(id = 'feedback_facilities_map',
                                                                                  config = graph_config_style,
                                                                                  style = {'padding-left': 15, 'width': '70vw', 'height': '60vh'}),
                                                                        html.Div([html.Hr()]),
                                                                        dcc.Graph(id = 'feedback_facilities_male_bar',
                                                                                  config = graph_config_style,
                                                                                  style = {'padding-left': 15, 'width': '70vw', 'height': '60vh'}),
                                                                        html.Div([html.Hr()]),
                                                                        dcc.Graph(id = 'feedback_facilities_female_bar',
                                                                                  config = graph_config_style,
                                                                                  style = {'padding-left': 15, 'width': '70vw', 'height': '60vh'})
                                                                        ],
                                                            selected_style = selected_side_tab_style),

                                                    dcc.Tab(label = "Needs of the Community",
                                                            children = [dcc.Graph(id = 'feedback_needs_male_bar',
                                                                                  config = graph_config_style,
                                                                                  style = {'padding-left': 15, 'width': '70vw', 'height': '60vh'}),
                                                                        html.Div([html.Hr()]),
                                                                        dcc.Graph(id = 'feedback_needs_female_bar',
                                                                                  config = graph_config_style,
                                                                                  style = {'padding-left': 15, 'width': '70vw', 'height': '60vh'})
                                                                        ],
                                                            selected_style = selected_side_tab_style),

                                                    dcc.Tab(label = "Cultural Participation",
                                                            children = [dcc.Graph(id = 'feedback_participate_male_bar',
                                                                                  config = graph_config_style,
                                                                                  style={'padding-left': 15, 'width': '70vw', 'height': '60vh'}),
                                                                        html.Div([html.Hr()]),
                                                                        dcc.Graph(id = 'feedback_participate_female_bar',
                                                                                  config = graph_config_style,
                                                                                  style = {'padding-left': 15, 'width': '70vw', 'height': '60vh'})
                                                                        ],
                                                            selected_style = selected_side_tab_style),

                                                    dcc.Tab(label = "Areas making Good Progress",
                                                            children = [dcc.Graph(id = 'feedback_progress_male_bar',
                                                                                  config = graph_config_style,
                                                                                  style={'padding-left': 15, 'width': '70vw', 'height': '60vh'}),
                                                                        html.Div([html.Hr()]),
                                                                        dcc.Graph(id = 'feedback_progress_female_bar',
                                                                                  config = graph_config_style,
                                                                                  style={'padding-left': 15, 'width': '70vw', 'height': '60vh'})
                                                                        ],
                                                            selected_style = selected_side_tab_style),

                                                    dcc.Tab(label = "Areas for Improvement",
                                                            children = [dcc.Graph(id = 'feedback_improve_male_bar',
                                                                                  config = graph_config_style,
                                                                                  style = {'padding-left': 15, 'width': '70vw', 'height': '60vh'}),
                                                                        html.Div([html.Hr()]),
                                                                        dcc.Graph(id = 'feedback_improve_female_bar',
                                                                                  config = graph_config_style,
                                                                                  style={'padding-left': 15, 'width': '70vw', 'height': '60vh'})
                                                                        ],
                                                            selected_style = selected_side_tab_style),

                                                    dcc.Tab(label = "Community's Definiton \n of Culture",
                                                            children = [dcc.Graph(id = 'feedback_definition_male_bar',
                                                                                  config = graph_config_style,
                                                                                  style={'padding-left': 15, 'width': '70vw', 'height': '60vh'}),
                                                                        html.Div([html.Hr()]),
                                                                        dcc.Graph(id = 'feedback_definition_female_bar',
                                                                                  config = graph_config_style,
                                                                                  style={'padding-left': 15, 'width': '70vw', 'height': '60vh'})
                                                                        ],
                                                            selected_style = selected_side_tab_style),

                                                    dcc.Tab(label = "Missing Cultural Goals",
                                                            children = [dcc.Graph(id = 'feedback_missing_male_bar',
                                                                                  config = graph_config_style,
                                                                                  style={'padding-left': 15, 'width': '70vw', 'height': '60vh'}),
                                                                        html.Div([html.Hr()]),
                                                                        dcc.Graph(id = 'feedback_missing_female_bar',
                                                                                  config = graph_config_style,
                                                                                  style={'padding-left': 15, 'width': '70vw', 'height': '60vh'})
                                                                        ],
                                                            selected_style = selected_side_tab_style)
                                                    ], style={'padding-top': 15})
                                        ], selected_style = selected_tab_style)

#############################################################
#############################################################
