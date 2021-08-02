#import packages
import json
import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
from pandas.io.formats.format import CategoricalFormatter
import plotly.graph_objs as go
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

#importing the stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Starting the Application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
server = app.server

# importing the data
data = pd.read_csv('pokedex.csv')
print(data.dtypes)

#Dropdown Values
options= [('Generation ' + x.astype(str)) for x in sorted(data['generation'].unique())]

#Default option as Generation 1 Pokemon
dff = data[data['generation'] == 1]

#Creating Plotly Graphs
# Number of pokemons by status chart
trace_1 = go.Bar(x = dff.groupby(['status']).agg('count').reset_index()['status'], 
                y = dff.groupby(['status']).agg('count').reset_index()['pokedex_number'],
                text=dff.groupby(['status']).agg('count').reset_index()['pokedex_number'],
                name = '# of pokemon')
layout = go.Layout(title={'text': "# of pokemon by status",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                   hovermode = 'closest',
                   barmode='stack',
                   xaxis={'categoryorder':'total descending'},
                   xaxis_title="Status",
                   yaxis_title="# of Pokemon",
                   title_font_color="red",
                   font=dict(family="Georama",
                   size=18,
                   color="RebeccaPurple")
                )
fig1 = go.Figure(data = [trace_1], layout = layout)
fig1.update_traces( textposition='outside')

# Number of pokemons by growth rate chart
trace_2 = go.Bar(x = dff.groupby(['growth_rate']).agg('count').reset_index()['growth_rate'], 
                y = dff.groupby(['growth_rate']).agg('count').reset_index()['pokedex_number'],
                text=dff.groupby(['growth_rate']).agg('count').reset_index()['pokedex_number'],
                name = '# of pokemon')
layout = go.Layout(title={'text': "# of pokemon by growth rate",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                   hovermode = 'closest',
                   barmode='stack',
                   xaxis={'categoryorder':'total descending'},
                   xaxis_title="Growth Rate",
                   yaxis_title="# of Pokemon",
                   title_font_color="red",
                   font=dict(family="Georama",
                   size=18,
                   color="RebeccaPurple")
                )
fig2 = go.Figure(data = [trace_2], layout = layout)
fig2.update_traces( textposition='outside')


# Number of pokemons by growth rate chart
trace_3 = go.Scatter(x = dff['attack'], 
                y = dff['defense'],
                customdata=dff['name'],
                name = '',
                hovertemplate='%{customdata}',
                mode='markers')
layout = go.Layout(title={'text': "Relation between attack and defense power",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                   hovermode = 'closest',
                   xaxis={'categoryorder':'total descending'},
                   xaxis_title="Attack",
                   yaxis_title="Defence",
                   title_font_color="red",
                   font=dict(family="Georama",
                   size=18,
                   color="RebeccaPurple")
                )
fig3 = go.Figure(data = [trace_3], layout = layout)


#Creating Dash Layout
# ************************************************************************
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("POKEMON DASHBOARD"
                        "",
                        style={'color': 'red','text-align': 'center'}),
                width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H1(""))
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='dropdown',
                className='dropdown',
                options=[
                    {'label': 'Generation ' + x.astype(str), 'value': x}
                    for x in sorted(data['generation'].unique())
                ],
                value='1',
                searchable=True,
            ),
            width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H1(""
                        ""))
    ]),
    dbc.Row([
            dbc.Col([
                html.H5('Relation between attack and defense power',
                        style={'color': 'blue', 'text-align': 'center'}),
                dcc.Graph(id='the_graph3',figure = fig3,
                          )
            ],
                width=5
            ),
            dbc.Col([
                html.H5('Stats of ',
                        style={'color': 'blue', 'text-align': 'center'}),
                dcc.Graph(id='the_graph4',
                hoverData={'points': [{'customdata': ['Mewtwo']}]}),
            ],
                width={'size': 5, 'offset': 1}
            ),
        ]),
    dbc.Row([
        dbc.Col([
            html.H5('# of pokemon by status',
                    style={'color': 'blue', 'text-align': 'center'}),
            dcc.Graph(id='the_graph1',figure = fig1)
        ],
            width=5
        ),
        dbc.Col([
            html.H5('# of pokemon by growth rate',
                    style={'color': 'blue', 'text-align': 'center'}),
            dcc.Graph(id='the_graph2',figure = fig2),
        ],
            width={'size': 5, 'offset': 1}
        )
    ])
])


# App Callback
# ************************************************************************
@app.callback(
    dash.dependencies.Output('the_graph1', 'figure'),
    dash.dependencies.Output('the_graph2', 'figure'),
    dash.dependencies.Output('the_graph3', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
    
# Update_graph function Initialisation
# ************************************************************************

def update_graph(dropdown):
    dff = data[data['generation'] == 1]
    dff = data[data['generation'] == dropdown]
    dff1 = dff.groupby(['status']).agg('count').reset_index()
    trace_1 = go.Bar(x = dff1['status'], 
                y = dff1['pokedex_number'],
                text=dff1['pokedex_number'],
                name = '# of pokemon')
    layout = go.Layout(title={'text': "# of pokemon by status",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                   hovermode = 'closest',
                   barmode='stack',
                   xaxis={'categoryorder':'total descending'},
                   xaxis_title="Status",
                   yaxis_title="# of Pokemon",
                   title_font_color="red",
                   font=dict(family="Georama",
                   size=18,
                   color="RebeccaPurple")
                )
    fig1 = go.Figure(data = [trace_1], layout = layout)
    fig1.update_traces( textposition='outside')

    dff2 = dff.groupby(['growth_rate']).agg('count').reset_index()
    trace_2 = go.Bar(x = dff2['growth_rate'], 
                y = dff2['pokedex_number'],
                text=dff2['pokedex_number'],
                name = '# of pokemon')
    layout = go.Layout(title={'text': "# of pokemon by growth rate",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                   hovermode = 'closest',
                   barmode='stack',
                   xaxis={'categoryorder':'total descending'},
                   xaxis_title="Growth Rate",
                   yaxis_title="# of Pokemon",
                   title_font_color="red",
                   font=dict(family="Georama",
                   size=18,
                   color="RebeccaPurple")
                )
    fig2 = go.Figure(data = [trace_2], layout = layout)
    fig2.update_traces( textposition='outside')

    trace_3 = go.Scatter(x = dff['attack'], 
                y = dff['defense'],
                customdata=dff['name'],
                name = '',
                hovertemplate='%{customdata}',
                mode='markers')
    layout = go.Layout(title={'text': "Relation between attack and defense power",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                   hovermode = 'closest',
                   xaxis={'categoryorder':'total descending'},
                   xaxis_title="Attack",
                   yaxis_title="Defence",
                   title_font_color="red",
                   font=dict(family="Georama",
                   size=18,
                   color="RebeccaPurple")
                )
    fig3 = go.Figure(data = [trace_3], layout = layout)
    return (fig1, fig2, fig3)

def upgrade_line_polar(dff, title):
    dff3 = pd.melt(dff, id_vars='name', value_vars=['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed'])
    bar4 = px.line_polar(dff3, theta='variable', r='value', line_close=True)
    bar4.update_traces(fill='toself')
    bar4.update_layout(
        title=title,
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='# of Pokemon',
            titlefont_size=12,
            tickfont_size=12,
        ),
        xaxis=dict(
            title='Growth Rate',
            titlefont_size=12,
            tickfont_size=12,
        ),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 260]
            ))
    )
    return (bar4)


@app.callback(
    Output('the_graph4', 'figure'),
    [Input('the_graph3', 'hoverData')]
)

def update_dataframe(hoverData):
    if not hoverData:
        return dash.no_update
    name = [hoverData['points'][0]['customdata']]
    dff = data[data['name'].isin(name)]
    title = 'Stat of {}'.format(name[0])
    return upgrade_line_polar(dff, title)

if __name__ == '__main__':
    app.run_server(debug=True)
