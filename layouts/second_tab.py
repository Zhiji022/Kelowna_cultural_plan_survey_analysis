# layout for the second tab of the dashboard

# built-in modules
import dash_table
import dash_core_components as dcc
import dash_html_components as html

# configs
from configs.DashConfigs import graph_config_style, selected_tab_style

# dataloaders
from dataloaders.CultureCentreDistances import culture_centre_distances
from dataloaders.GoalImportance import goal_importance
from dataloaders.GoalDescription import df_goal

#############################################################
# Data Preparation
#############################################################
genders = [dict(label = item, value = item) for item in culture_centre_distances['Gender'].unique().tolist() if item != 'Undisclosed']
age_groups = [dict(label = item, value = item) for item in sorted(culture_centre_distances['Age'].unique().tolist()) if item != 'Undisclosed']

cultural_centres = [dict(label = item, value = item) for item in sorted(culture_centre_distances['Culture Centre'].dropna().unique().tolist())]
cultural_centres.insert(0, dict(label = 'All', value = 'All'))

localities_options = goal_importance['Postal Code'].unique().tolist()
localities_options.remove('Other')
localities_options.insert(0, 'All')
localities_options = [dict(label = item, value = item) for item in localities_options]

min_distance = float(culture_centre_distances['Distance (kms)'].min())
max_distance = float(culture_centre_distances['Distance (kms)'].max())

#############################
# Layout Functions
#############################
def get_tab_layout():
    return dcc.Tab(label = "Cultural Goal Importance",
                   children = [
                              html.Div([
                                   html.Div([
                                           html.Div([
                                                   html.B("Zoom"),
                                                   dcc.Slider(id = 'zoom_slider_map2',
                                                              min = 1,
                                                              max = 6,
                                                              step = 0.25,
                                                              marks = {str(value): str(value) for value in list(range(1, 7))},
                                                              value = 2)
                                                   ], style={'padding-bottom': 45}),

                                            html.Div([
                                                    html.B("Gender"),
                                                    dcc.Checklist(id = 'gender_option',
                                                                  options = genders,
                                                                  values = [])
                                                    ], style = {'float': 'left', 'display': 'inline-block', 'padding-right': 20}),

                                            html.Div([
                                                    html.B("Age Group"),
                                                    dcc.Checklist(id = 'age_option',
                                                                  options = age_groups,
                                                                  values = [])
                                                    ], style = {'float': 'left', 'display': 'inline-block', 'padding-bottom': 20}),

                                            html.Div([
                                                    html.B("Locality"),
                                                    dcc.Dropdown(id = 'localities_options',
                                                                 options = localities_options,
                                                                 clearable = False)
                                                    ], style={'padding-bottom': 20}),

                                            html.Div(children = ["Please select a bar from the graph to view the spatial distribution of its goal importance"],
                                                     style={'padding-bottom':20})

                                        ], style={'display': 'inline-block', 'border-radius': 5, 'background-color':'#F9F9F9',
                                                  'box-shadow': 'inset 1px 1px #EDEDED', 'padding-right': 25, 'padding-top': 5,
                                                  'padding-left': 15, 'padding-bottom': 15, 'width': '14vw', 'float': 'left'}),

                                   html.Div([
                                           dcc.Graph(id = 'stacked_bar',
                                                     style = {'width': '75vw', 'height': '35vh', 'float':'left'},
                                                     config = graph_config_style),


                                           html.Div([
                                                   html.Div([
                                                           dash_table.DataTable(id = 'goal_table',
                                                                                columns = [{'name': 'Goal', 'id': 'Goal'}, {'name': 'Description', 'id': 'Description'}],
                                                                                data = df_goal.to_dict('records'),
                                                                                style_cell = {'textAlign': 'left','padding': '5px'},
                                                                                style_as_list_view = True,
                                                                                style_header = {'fontWeight': 'bold',
                                                                                                'fontSize':'15',
                                                                                                'backgroundColor': '#7BE0F1',
                                                                                                'textAlign': 'center'},
                                                                                style_table = {'maxWidth': '45vw',
                                                                                               'overflowX': 'scroll'})
                                                           ], style={'display':'inline-block', 'float':'left', 'padding-top': 3}),

                                           html.Div([
                                                   dcc.Graph(id = 'map_plot2',
                                                             config = graph_config_style,
                                                             style = {'width': '25vw', 'height': '50vh', 'padding-left': 15, 'display': 'inline-block', 'float': 'left'}),
                                                   html.Button('RESET', id = 'remove_clickData')
                                                   ], style={'display':'inline-block', 'float':'left'}),
                                                   ])
                                           ], style={'display':'inline-block', 'float':'right', 'padding-left': 30})

                                ], style={'display': 'inline-block', 'padding-top': 15})

                            ], selected_style = selected_tab_style)

#############################################################
#############################################################
