# layout for the first tab of the dashboard

# built-in modules
import dash_core_components as dcc
import dash_html_components as html

# configs
from configs.DashConfigs import graph_config_style, selected_tab_style

# dataloaders
from dataloaders.CultureCentreDistances import culture_centre_distances

#############################################################
# Data Preparation
#############################################################
genders = [dict(label = item, value = item) for item in culture_centre_distances['Gender'].unique().tolist() if item != 'Undisclosed']
age_groups = [dict(label = item, value = item) for item in sorted(culture_centre_distances['Age'].unique().tolist()) if item != 'Undisclosed']

cultural_centres = [dict(label = item, value = item) for item in sorted(culture_centre_distances['Culture Centre'].dropna().unique().tolist())]
cultural_centres.insert(0, dict(label = 'All', value = 'All'))

localities = [dict(label = item, value = item) for item in sorted(culture_centre_distances['Postal Code'].str.slice(0, 3).unique().tolist())]
localities.insert(0, dict(label = 'All', value = 'All'))

min_distance = float(culture_centre_distances['Distance (kms)'].min())
max_distance = float(culture_centre_distances['Distance (kms)'].max())

#############################
# Layout Functions
#############################
def get_tab_layout():
    return dcc.Tab(label = "Cultural Participation",
                   children = [
                              html.Div([
                                html.Div([
                                    html.Div([
                                            html.B("Zoom"),
                                            dcc.Slider(id = 'zoom_slider',
                                                       min = 1,
                                                       max = 6,
                                                       step = 0.5,
                                                       marks = {str(value): str(value) for value in list(range(1, 7))},
                                                       value = 3)
                                            ], style={'padding-bottom': 45}),

                                    html.Div([
                                            html.B("Gender"),
                                            dcc.Checklist(id = 'gender_checklist',
                                                          options = genders,
                                                          values = list())
                                            ], style={'float': 'left', 'display': 'inline-block', 'padding-right': 20}),

                                    html.Div([
                                            html.B("Age Group"),
                                            dcc.Checklist(id = 'age_checklist',
                                                          options = age_groups,
                                                          values = list())
                                            ], style={'float': 'left', 'display': 'inline-block', 'padding-bottom': 30}),

                                    html.Div([
                                            html.B("Culture Centre"),
                                            dcc.Dropdown(id = 'cultural_centre_dropdown',
                                                         options = cultural_centres,
                                                         value = 'All',
                                                         clearable = False)
                                            ]),

                                    html.Div([
                                            html.B("Locality"),
                                            dcc.Dropdown(id = 'locality_dropdown',
                                                         options = localities,
                                                         value='All',
                                                         clearable = False)
                                            ], style={'padding-top': 30}),

                                    html.Div([
                                            html.B("Travel Distance (kms)"),
                                            dcc.RangeSlider(id = 'travel_distance_slider',
                                                            min = min_distance,
                                                            max = max_distance,
                                                            value = [5, 50],
                                                            marks = {str(dist): str(dist) for dist in list(range(int(min_distance), int(max_distance), 60))}),
                                            html.Div(id = 'distance_slider_text', style={'padding-top': 25, 'font-size': 12, 'color': '#5C5C5C'})
                                             ], style={'padding-top': 30})

                                        ], style={'display': 'inline-block', 'border-radius': 5, 'background-color':'#F9F9F9',
                                                  'box-shadow': 'inset 1px 1px #EDEDED', 'padding-top': 5, 'padding-right': 25,
                                                  'padding-left': 15, 'padding-bottom': 15, 'width': '14vw', 'float': 'left'}),

                                dcc.Graph(id = 'culture_participation_map',
                                          style = {'width': '50vw', 'height': '80vh', 'float': 'left', 'display': 'inline-block'},
                                          config = graph_config_style),

                                html.Div([
                                        html.Div([
                                                dcc.Graph(id = "visitors_distances",
                                                          config = graph_config_style),
                                                ], style={'padding-left': 15, 'width': '25vw', 'height': 200, 'padding-bottom': 0}),
                                        html.Hr(style = {'padding-top': 0, 'padding-bottom': 0}),

                                        html.Div([
                                                dcc.Graph(id = "decay_plot",
                                                          config = graph_config_style),
                                                ], style={'padding-left': 15, 'width': '25vw', 'height': 200, 'padding-top': 0}),
                                        html.Hr(style = {'padding-top': 0, 'padding-bottom': 0}),

                                        html.Div([
                                                dcc.Graph(id = "topic_distribution",
                                                          config = graph_config_style)
                                                ], style={'padding-left': 15, 'width': '25vw', 'height': 40, 'padding-top': 0})
                                        ], style = {'float': 'right', 'display': 'inline-block', 'padding-bottom': 150})

                                    ], style={'display': 'inline-block', 'padding-top': 15})

                                ], selected_style = selected_tab_style)

#############################################################
#############################################################
