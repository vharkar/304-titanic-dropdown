######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Titanic!'
color1='#007FFF'
color2='#EFBBCC'
color3='#FFFF99'
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/vharkar/304-titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv("assets/titanic_data.csv")
variables_list=['Survived', 'AccompanyingParentsOrChildren', 'Fare', 'Age']
values_list=['survived','parch','fare','age']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a continuous variable for summary statistics:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': variables_list[i], 'value': values_list[i]} for i in range(0, len(variables_list))],
        value=values_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_mean=df.groupby(['who', 'embark_town'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['first'].index,
        y=results.loc['first'][continuous_var],
        name='man',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['second'].index,
        y=results.loc['second'][continuous_var],
        name='woman',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results.loc['third'].index,
        y=results.loc['third'][continuous_var],
        name='child',
        marker=dict(color=color3)
    )

    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Port of Embarkation'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
