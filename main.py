import json
import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.io as pio
import plotly.express as px

pio.templates.default = "simple_white"

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

data = pd.read_csv('pokedex.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])
server = app.server

#  Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
# ************************************************************************
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("POKEMON DASHBOARD"
                        "",
                        style={'color': 'red','text-align': 'center'}),
                width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H1(""
                        ""))
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
                value=1,
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
                        style={'color': 'blue', 'text-align': 'center','font-family':'Helvetica'}),
                dcc.Graph(id='the_graph3',
                          hoverData={'points': [{'customdata': ['Mewtwo']}]})
            ],
                width=5
            ),
            dbc.Col([
                html.H5(id='title-barpolar',
                        style={'color': 'blue', 'text-align': 'center','font-family': 'Helvetica'}),
                html.H6('Move the cursor over the data points in the left scatter plot to checkout stats of other pokemons',
                        style={'color': 'black', 'text-align': 'center','font-family': 'Helvetica'}),
                dcc.Graph(id='the_graph4'),
            ],
                width={'size': 5, 'offset': 1}
            ),
        ]),
    dbc.Row([
        dbc.Col([
            html.H5('# of pokemon by status',
                    style={'color': 'blue', 'text-align': 'center','font-family':'Helvetica'}),
            dcc.Graph(id='the_graph1')
        ],
            width=5
        ),
        dbc.Col([
            html.H5('# of pokemon by growth rate',
                    style={'color': 'blue', 'text-align': 'center','font-family':'Helvetica'}),
            dcc.Graph(id='the_graph2'),
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

def update_dataframe(dropdown):
    if not dropdown:
        return dash.no_update
    dff = data[data['generation'] == dropdown]
    return update_graph(dff)

def update_graph(dff):
    dff1 = dff.groupby(['status']).agg('count').reset_index()
    bar1 = px.bar(dff1, x='status', y='pokedex_number')
    bar1.update_layout(
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='# of Pokemon',
            titlefont_size=12,
            tickfont_size=12,
        ),
        xaxis=dict(
            title='Status',
            titlefont_size=12,
            tickfont_size=12,
        ))
    bar1.update_xaxes(categoryorder='total descending')
    dff1 = dff.groupby(['growth_rate']).agg('count').reset_index()
    bar2 = px.bar(dff1, y='pokedex_number', x='growth_rate')
    bar2.update_layout(
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
        )
    )
    bar2.update_xaxes(categoryorder='total descending')
    bar3 = px.scatter(dff, y='defense', x='attack', hover_data=['name'])
    bar3.update_layout(
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='defense',
            titlefont_size=12,
            tickfont_size=12,
        ),
        xaxis=dict(
            title='attack',
            titlefont_size=12,
            tickfont_size=12,
        )
    )
    dff1 = pd.melt(dff, id_vars='name', value_vars=['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed'])
    bar4 = px.bar_polar(dff1, theta='variable', r='value')
    bar4.update_layout(
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
        )
    )
    return (bar1, bar2, bar3)


def upgrade_line_polar(dff):
    dff1 = pd.melt(dff, id_vars='name', value_vars=['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed'])
    bar4 = px.line_polar(dff1, theta='variable', r='value', line_close=True)
    bar4.update_traces(fill='toself')
    bar4.update_layout(
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
    name = hoverData['points'][0]['customdata']
    dff = data[data['name'].isin(name)]
    return upgrade_line_polar(dff)

@app.callback(
    Output('title-barpolar', 'children'),
    [Input('the_graph3', 'hoverData')]
)

def update_barpolartitle(hoverData):
    if not hoverData:
        return dash.no_update
    name = hoverData['points'][0]['customdata']
    dff = data[data['name'].isin(name)]
    h5 = 'Stat of {}'.format(name[0])
    return (h5)


if __name__ == '__main__':
    app.run_server(debug=True)
