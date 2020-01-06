import plotly.graph_objs as go
from dash.dependencies import Input, Output
from server import app
import pandas as pd
from dataloaders.GoalImportance import goal_importance
import numpy as np

data = [{'Postal Code': 'V1Y', 'Longitude': -119.4784, 'Latitude': 49.8857},
        {'Postal Code': 'V1W', 'Longitude': -119.4465, 'Latitude': 49.8329},
        {'Postal Code': 'V1X', 'Longitude': -119.3510, 'Latitude': 49.9491},
        {'Postal Code': 'V1V', 'Longitude': -119.4283, 'Latitude': 49.9501},
        {'Postal Code': 'V4T', 'Longitude': -119.6651, 'Latitude': 49.9401},
        {'Postal Code': 'V1Z', 'Longitude': -119.5716, 'Latitude': 50.1913}]
location = pd.DataFrame(data)

goal_map = goal_importance
importance = [['Very Important', 3], ['Important',2], ['Less Important',1], ['Not Important',0]]
importance_score = pd.DataFrame(importance, columns=['Goal','Score'])

mapbox_access_token = 'pk.eyJ1IjoicXl6cXl6MSIsImEiOiJjanNodXdsMG8wcnAxNDlxZzhiazE3cjk2In0.8_FK2gmApimPtbIbKYcIlQ'

@app.callback(
    Output('map_plot2', 'figure'),
    [Input('localities_options', 'value'),
    Input('stacked_bar', 'clickData'),
    Input('age_option', 'values'),
    Input('gender_option', 'values'),
    Input('zoom_slider_map2','value')]
    )

def locality_map(locality, click_data, age, gender, zoom_value):
    if click_data != None:
        if((len(age)==0) & (len(gender)==0)):
            map_temp = goal_map
        elif((len(age)==0) & (len(gender)>0)):
            map_temp = goal_map[goal_map['Gender'].isin(gender)]
        elif((len(age)>0) & (len(gender)==0)):
            map_temp = goal_map[goal_map['Age'].isin(age)]
        else:
            map_temp = goal_map[(goal_map['Age'].isin(age)) & (goal_map['Gender'].isin(gender))]
        goal = click_data['points'][0]['x']
        map_temp = map_temp.loc[:, ['Age','Postal Code','Gender',goal]]
        map_temp.rename(columns={goal:'Goal'}, inplace=True)
        map_temp = map_temp.merge(importance_score, how='left',on='Goal')
        map_temp = map_temp.groupby("Postal Code").mean()
        map_temp.reset_index(inplace=True)
        map_temp = map_temp.merge(location, how='left',on='Postal Code')
        map_temp.dropna(inplace=True)

        map_temp['round_score'] = map_temp['Score'].map(lambda x: round(x,2))
        data = [
            go.Scattermapbox(
                lat = map_temp['Latitude'],
                lon = map_temp['Longitude'],
                mode = 'markers',
                marker = go.scattermapbox.Marker(
                            size = np.power(map_temp['Score'], 4)*1.5,
                            color = '#B03F18',
                            opacity= 0.5
                        ),
                hoverinfo = 'text',
                text = '<b>' + goal[:4] + ' ' + goal[4:] + '</b>' + '<br>' + 'Importance: ' + map_temp['round_score'].astype(str) + '<br>' + \
                            'Locality: '+ map_temp['Postal Code'] + '<br>' + map_temp['Latitude'].astype(str) + ', ' + map_temp['Longitude'].astype(str),
                showlegend = True,
                name = '<b>' + goal[:4]+' '+goal[4:] + '</b>'+ '<br>Circle size denotes importance level'
            )
        ]

    else:

        if locality !='All':
            locality_map = location[location['Postal Code'] == locality]
        else:
            locality_map = location
        marker_size = (zoom_value+6)*3*22/24

        data = [
            go.Scattermapbox(
                lat = locality_map['Latitude'],
                lon = locality_map['Longitude'],
                mode = 'markers',
                marker = go.scattermapbox.Marker(
                            size = marker_size,
                            color = '#B03F18',
                            opacity= 0.5
                        ),
                hoverinfo = 'text',
                text = 'Locality: ' + locality_map['Postal Code'].astype(str) + '<br>' + locality_map['Latitude'].astype(str) + ', ' + locality_map['Longitude'].astype(str),
                showlegend = False,
            )
        ]

    layout = go.Layout(
        autosize = True,
        hovermode = 'closest',
        mapbox = go.layout.Mapbox(
            accesstoken = mapbox_access_token,
            bearing = 0,
            center = go.layout.mapbox.Center(
                lat = 50.0380,
                lon = -119.5005
            ),
            style = 'light',
            pitch = 0,
            zoom = zoom_value+6,
        ),
        margin=go.layout.Margin(
            l=0,
            r=0,
            t=0,
            b=0
        ),
        legend=dict(
            x = 0,
            y = 1,
            bgcolor = '#E2E2E2',
            bordercolor = '#FFFFFF',
            borderwidth = 2,
        )
    )
    return {
    'data':data,
    'layout':layout
    }
