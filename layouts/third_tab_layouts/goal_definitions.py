# module to create callback for age group filter for cultural participation
import dash_table
import pandas as pd
import dash_html_components as html

#############################################################
# Data Preparation
#############################################################

goal_definitions = pd.DataFrame({'Goal':['Enhance existing cultural support programs',
                                         'Optimize existing cultural facilities',
                                         'More and different kinds of affordable cultural spaces',
                                         'Integrate heritage as part of cultural vitality',
                                         'Enhance cultural vitality at the street level',
                                         'Build personal connections to cultural vitality',
                                         'Improve data collection and issue a cultural report card',
                                         'Capitalize on culture for tourism and the economy',
                                         'Convene and connect the cultural community',
                                         'Walk the talk and integrate culture into plans and process',
                                         'Others'],
                                'Responses':['Parking availability; Spaces for cultural activities and market involvement',
                                             'Facilities need investments from business organizations',
                                             'Extension of cultural activities to outdoor/downtown; Need more publicity',
                                             'Grants required for heritage buildings, social media and local business involvement',
                                             'Support for those participating in outdoor/street arts performances',
                                             'Funding, advertising and volunteers required for some unaffordable programs',
                                             'Public availability of culture data',
                                             'More subsidies to encourage attendance for cultural events',
                                             'Support and promotions required to encourage participation in diversified cultural activities',
                                             'Grants and marketing needed to achieve cultural diversity',
                                             'Planning of Kelowna\'s culture from an ethical standpoint']})

#############################################################
# Figure Creation Functions
#############################################################
def get_goal_definitions_table():
    data_table = dash_table.DataTable(
                            columns=[{'name': 'Goal', 'id': 'Goal'}, {'name': 'Community\'s Needs', 'id': 'Definition'}],
                            data = [{'Goal': item[1], 'Definition': item[2]} for item in goal_definitions.itertuples()],
                            style_cell = {'textAlign': 'left','padding': '5px', 'font-size': 14},
                            style_as_list_view = False,
                            style_header = {
                                    'fontWeight': 'bold',
                                    'font-size':14,
                                    'backgroundColor': '#7BE0F1',
                                    'textAlign': 'center'
                            },
                            style_table={'width': '60vw'},
                        )

    return html.Div([data_table], style={'padding-left': 15, 'padding-top': 17})
