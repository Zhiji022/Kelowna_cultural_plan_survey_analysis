import plotly.graph_objs as go
from dash.dependencies import Input, Output
from server import app
from dataloaders.GoalImportance import goal_importance
import pandas as pd

color = {'Very Important':'#9C1141','Important':'#111F9C','Less Important':'#D7A71E','Not Important':'#4A4946'}

@app.callback(
    Output('stacked_bar', 'figure'),
    [Input('age_option', 'values'),
    Input('gender_option','values'),
    Input('localities_options','value'),
    Input('stacked_bar','clickData')
    ])

# Plotting function for stacked bar plot
def stacked_barplot(age, gender, locality, click_data):
        if((len(age)==0) & (len(gender)==0)):
            df2 = goal_importance
        elif((len(age)==0) & (len(gender)>0)):
            df2 = goal_importance[goal_importance['Gender'].isin(gender)]
        elif((len(age)>0) & (len(gender)==0)):
            df2 = goal_importance[goal_importance['Age'].isin(age)]
        else:
            df2 = goal_importance[(goal_importance['Age'].isin(age)) & (goal_importance['Gender'].isin(gender))]

        if(locality!='All'):
            df2 = df2[df2['Postal Code']==locality]

        df_bar = df2.iloc[:,3:].apply(pd.Series.value_counts)
        df_bar.fillna(0, inplace=True)
        df_bar = df_bar.apply(lambda x: round(x / x.sum()*100,2))
        try:
            not_important = df_bar.iloc[1,:]
            somewhat_important = df_bar.iloc[2,:]
            important = df_bar.iloc[0,:]
            very_important = df_bar.iloc[3,:]
            df_bar.drop('Important',axis=0, inplace=True)
            df_bar.drop('Not Important',axis=0, inplace=True)
            df_bar.drop('Less Important',axis=0, inplace=True)
            df_bar.drop('Very Important',axis=0, inplace=True)

            df_bar.loc['Not Important'] = not_important
            df_bar.loc['Less Important'] = somewhat_important
            df_bar.loc['Important'] = important
            df_bar.loc['Very Important'] = very_important
        except:
            important = df_bar.iloc[0,:]
            somewhat_important = df_bar.iloc[1,:]
            very_important = df_bar.iloc[2,:]
            df_bar.drop('Important',axis=0, inplace=True)
            df_bar.drop('Less Important',axis=0, inplace=True)
            df_bar.drop('Very Important',axis=0, inplace=True)
            df_bar.loc['Less Important'] = somewhat_important
            df_bar.loc['Important'] = important
            df_bar.loc['Very Important'] = very_important
        data = []
        for i in range(len(df_bar)):
            for k, v in color.items():
                if k == list(df_bar.index)[i]:
                    marker_color = v
            if click_data == None:
                trace = go.Bar(
                    x=list(df_bar.columns),
                    y=df_bar.iloc[i,:],
                    name=list(df_bar.index)[i],
                    marker=dict(color=marker_color)
                )
                data.append(trace)
            else:
                trace = go.Bar(
                    x=list(df_bar.columns),
                    y=df_bar.iloc[i,:],
                    name=list(df_bar.index)[i] + ' - ' + '<b>' + str(i) + '</b>',
                    marker=dict(color=marker_color)
                )
                data.append(trace)
        layout = go.Layout(
        barmode = 'stack',
        yaxis=dict(
            title='Percentage (%)'
            ),
        margin=go.layout.Margin(
            r=0,
            t=0,
            b = 30,
            l = 45
        ),
        modebar = dict(orientation = 'v')
        )

        return{
            'data': data,
            'layout': layout
        }
