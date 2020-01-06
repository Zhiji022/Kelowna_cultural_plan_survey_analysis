# Kelowna Culture Analysis Dashboard
# Authors: Vaghul Aditya Balaji, Zhiji Ding and Tom Qu

# built-in modules
import os
import flask
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime

# server
from server import app, server

# configs
from configs.UserAuthentication import get_user_login_keys

# dash layouts
from layouts import first_tab, second_tab, third_tab, fourth_tab

#############################
# Dash Layout
#############################
app.title = "Kelowna Culture Analysis"

@server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(server.root_path, 'static'), 'favicon.ico')

# user login authentication
user_login_keys = get_user_login_keys()
auth = dash_auth.BasicAuth(app, user_login_keys)

app.layout = html.Div([

    html.Img(src = 'assets/city_of_kelowna_logo.png', height = '60vh', width = '280vw', style = {'display': 'inline-block', 'padding-bottom': 8}),

    dcc.Tabs(id = 'tabs',
             children = [first_tab.get_tab_layout(),
                         second_tab.get_tab_layout(),
                         third_tab.get_tab_layout(),
                         fourth_tab.get_tab_layout()],
             style = {'height': '6vh', 'borderBottom': '1px solid #d6d6d6', 'fontWeight': 'bold'}),

    html.Hr(),
    html.Div([f"Copyright © {datetime.now().year}. Created by ",
              html.A("Zhiji Ding", href = "https://www.linkedin.com/in/zhiji-ding-97824610/", target = '_blank'), ", ",
              html.A("Tom Qu", href = "mailto:yizhe.qu@gmail.com", target = '_blank'), " and ",
              html.A("Vaghul Aditya Balaji", href = "https://www.linkedin.com/in/vaghulb1992/", target = '_blank')],
    style = {'font-size': '9pt'})
])

#############################################################
# Importing call-back functions
#############################################################
from callbacks.first_tab import map_callback
from callbacks.first_tab import slider_callback
from callbacks.first_tab import visitdist_callback
from callbacks.first_tab import decay_callback
from callbacks.first_tab import activity_callback

from callbacks.second_tab import stacked_bar
from callbacks.second_tab import locality_map
from callbacks.second_tab import remove_clickData
from callbacks.second_tab import table_style
from callbacks.second_tab import localities_value

from callbacks.third_tab import facility_scatterplot_callback
from callbacks.third_tab import facility_clusters_callback

from callbacks.fourth_tab import feedback_table_callback
from callbacks.fourth_tab import feedback_participate_callback
from callbacks.fourth_tab import feedback_needs_callback
from callbacks.fourth_tab import feedback_progress_callback
from callbacks.fourth_tab import feedback_improve_callback
from callbacks.fourth_tab import feedback_definition_callback
from callbacks.fourth_tab import feedback_missing_callback
from callbacks.fourth_tab import feedback_facilities_callback

#############################
# Launching the server
#############################
if __name__ == '__main__':
    app.run_server(debug=True)

#############################################################
#############################################################
