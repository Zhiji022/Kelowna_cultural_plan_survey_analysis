# module to create callback for travel distance range slider
from dash.dependencies import Input, Output
import sys

# app server
sys.path.append('../..')
from server import app

#############################################################
# Callback Function
#############################################################

@app.callback(Output('distance_slider_text', 'children'),
              [Input('travel_distance_slider', 'value')])
def distance_slider_callback(travel_distance_range):
    return f"Range: {travel_distance_range[0]} - {travel_distance_range[1]} kms"
