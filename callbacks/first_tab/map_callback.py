# module to create callback for age group filter for cultural participation
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import sys

# app server
sys.path.append('../..')
from server import app

# data loaders
from dataloaders.CultureCentreDistances import culture_centre_distances

# Access token for mapbox plots
mapbox_access_token = 'pk.eyJ1IjoidmFnaHVsYjE5OTIiLCJhIjoiY2p2Nzhuc3l1MDZwMzN5bjdoenZvN3NreCJ9.ymf9C1epcbzgyak9ZZAIuQ'

#############################################################
# Callback Function
#############################################################

@app.callback(Output('culture_participation_map', 'figure'),
              [Input('gender_checklist', 'values'),
               Input('age_checklist', 'values'),
               Input('cultural_centre_dropdown', 'value'),
               Input('locality_dropdown', 'value'),
               Input('travel_distance_slider', 'value'),
               Input('zoom_slider', 'value')])
def map_plot_callback(genders, age_groups, cul_centre, locality, travel_distance_range, zoom_value):
    # filtering by gender
    if(len(genders)):
        df = culture_centre_distances[culture_centre_distances['Gender'].isin(genders)]
    else:
        df = culture_centre_distances

    # filtering by age-group
    if(len(age_groups)):
        df = df[df['Age'].isin(age_groups)]

    # filtering by cultural centre
    if(cul_centre != 'All'):
        df = df[df['Culture Centre'] == cul_centre]

    # filtering by locality
    if(locality != 'All'):
        df = df[df['Postal Code'].str.startswith(locality)]

    # filtering by travel distance
    df = df[df['Distance (kms)'].between(int(travel_distance_range[0]), int(travel_distance_range[1]), inclusive = True)]

    data = [
        go.Scattermapbox(
            lat = df['Latitude'],
            lon = df['Longitude'],
            mode = 'markers',
            marker = go.scattermapbox.Marker(
                        size = 5,
                        color = '#031884'
                    ),
            hoverinfo = 'text',
            text = df['Postal Code'] + '<br>' + df['Latitude'].astype(str) + ', ' + df['Longitude'].astype(str),
            showlegend = True,
            name = '<b>Individuals</b>'
        )
    ]

    culture_centres = [go.Scattermapbox(
                            lat = df['C_Latitude'],
                            lon = df['C_Longitude'],
                            mode = 'markers',
                            marker = go.scattermapbox.Marker(
                                        size = 8,
                                        color = '#C83F34'
                                    ),
                            hoverinfo = 'text',
                            text = df['Culture Centre'] + '<br>' + df['C_Postal_Code'] + '<br>' + df['C_Latitude'].astype(str) + ", " + df['C_Longitude'].astype(str),
                            showlegend = True,
                            name = '<b>Culture Centres</b>'
                        )]

    paths = []
    for i in df.itertuples():
        paths.append(
        go.Scattermapbox(
                lat = [getattr(i, 'Latitude'), getattr(i, 'C_Latitude')],
                lon = [getattr(i, 'Longitude'), getattr(i, 'C_Longitude')],
                mode = 'lines',
                line = go.scattermapbox.Line(
                            color = "black"
                    ),
                showlegend = False,
                opacity = 0.1
                )
        )

    data = paths + data + culture_centres

    layout = go.Layout(
        autosize = True,
        hovermode = 'closest',
        mapbox = go.layout.Mapbox(
            accesstoken = mapbox_access_token,
                center = go.layout.mapbox.Center(
                    lat = 49.897135,
                    lon = -119.478413,
            ),
            style = 'light',
            pitch = 0,
            zoom = float(zoom_value) + 7,
            bearing = 0
        ),
        margin = dict(t = 0, l = 0, r = 0, b = 0),
        legend=dict(
            x = 0,
            y = 1,
            bgcolor = '#E2E2E2',
            bordercolor = '#FFFFFF',
            borderwidth = 2,
        )
    )

    return go.Figure(data=data, layout=layout)
