from dash.dependencies import Input, Output
from server import app
from dataloaders.GoalDescription import df_goal

@app.callback(
    Output('goal_table', 'style_data_conditional'),
    [Input('stacked_bar', 'clickData')])
def update_style(click_data):
    if click_data != None:
        goal = click_data['points'][0]['x']
        goal = goal[:4]+' '+goal[4:]
        index = df_goal[df_goal['Goal']==goal].index.values[0]

        style_data_conditional=[
                {
            "if": {"row_index": index},
                "backgroundColor": "#93FFDD",
                'color': 'black',
                'fontWeight': 'bold',
                'textAlign': 'left'
        },
                {
            'if': {'column_id': 'Goal'},
                'fontWeight': 'bold',
                'backgroundColor':'#E0F9FF',
                'textAlign': 'center'}]

    else:
        style_data_conditional=[{
        'if': {'column_id': 'Goal'},
            'fontWeight': 'bold',
            'backgroundColor':'#E0F9FF',
            'textAlign': 'center',
        }]
    return style_data_conditional
