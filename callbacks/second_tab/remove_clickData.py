from dash.dependencies import Input, Output
from server import app

@app.callback(Output('stacked_bar', 'clickData'),
              [Input('remove_clickData', 'n_clicks')])
def reset_click_data_callback(n_clicks):
    return None

@app.callback(Output('remove_clickData', 'style'),
              [Input('stacked_bar', 'clickData')])
def hide_reset_button_callback(click_data):
    if click_data == None:
        return {'background-color': 'white', 'color': 'black', 'display':'inline-block', 'float':'left', 'visibility': 'hidden'}
    else:
        return {'background-color': 'white', 'color': 'black', 'display':'inline-block', 'float':'left'}
