from dash.dependencies import Input, Output
from server import app

@app.callback(Output('localities_options', 'value'),
              [Input('stacked_bar', 'clickData')])
def remove_clickData(click_data):
    return 'All'
