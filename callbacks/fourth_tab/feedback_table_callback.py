# module to create callback for age group filter for cultural participation
from dash.dependencies import Input, Output, State
import sys
import pandas as pd
import io
from flask import send_file

# app server
sys.path.append('../..')

# data loaders
from configs.GoogleSpreadsheets import get_feedback_table_columns, get_feedback_table_data
from server import app

#############################################################
# Callback Functions
#############################################################
@app.callback(Output('feedback_table', 'columns'),
              [Input('tabs', 'value'),
               Input('refresh_feedback_table_button', 'n_clicks')],
              [State('feedback_table', 'columns')])
def feedback_table_header_callback(activated_tab, n_clicks, existing_state):
    if activated_tab == 'tab-4':
        column_list = get_feedback_table_columns()
        return [{'name': item, 'id': item} for item in column_list]
    else:
        return existing_state

@app.callback(Output('feedback_table', 'data'),
              [Input('tabs', 'value'),
               Input('refresh_feedback_table_button', 'n_clicks')],
              [State('feedback_table', 'data')])
def feedback_table_rows_callback(activated_tab, n_clicks, existing_state):
    if activated_tab == 'tab-4':
        return get_feedback_table_data()
    else:
        return existing_state

@app.server.route("/feedback_table/")
def download_excel():
    # creating the dataframe
    df = pd.DataFrame(get_feedback_table_data())

    # convert to excel
    buf = io.BytesIO()
    excel_writer = pd.ExcelWriter(buf, engine = "xlsxwriter")
    df.to_excel(excel_writer, sheet_name = "sheet1", index = False)
    excel_writer.save()
    buf.seek(0)

    return send_file(
        buf,
        mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        attachment_filename = "kelowna_community_culture_feedback.xlsx",
        as_attachment = True,
        cache_timeout = 0
        )
