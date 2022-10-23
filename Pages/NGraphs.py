from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div("Select Graph Type : ",style={'padding':'5px'}),
                    dcc.Dropdown(['Scatter','Line','Horizontal Bar', 'Vertical Bar','Box Plot','Tree Map','Histogram','Vertical Stacked Bar','Horizontal Stacked Bar'  ], 'Box Plot' , id='graph_dropdown')
                ]),
                dbc.Col([
                    html.Div("Select X-axis ",style={'padding':'5px'}),
                    dcc.Dropdown(id='df_x')
                ]),
                dbc.Col([
                    html.Div("Select Y-axis ",style={'padding':'5px'}),
                    dcc.Dropdown(id='df_y')
                ]),
            ],style={'margin-right':'15px','margin-left':'15px'}),

            dbc.Row([
                dbc.Col(html.Div("Filter by : "),width=2),
            ],style={'margin-right':'15px','margin-left':'15px','padding':'10px'}),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id='df_fltr'),width=3),
                dbc.Col(dcc.Dropdown(id='df_fltr_colmn',multi=True),width=9)
            ],style={'margin-right':'15px','margin-left':'15px'}),
            dbc.Row([
                dbc.Col(dcc.Graph('update-graph', figure={},clickData=None, hoverData=None,))
            ])
        ],width=8),

        dbc.Col([
            dbc.Row(dbc.Col(html.Div("Pie Chart",style={'textAlign': 'center','padding':'5px'}))),
            dbc.Row([
                dbc.Col([
                    html.Div("Select Categories ",style={'padding':'5px'}),
                    dcc.Dropdown(id='pie_catg')
                ]),
                dbc.Col([
                    html.Div("Select Numeric",style={'padding':'5px'}),
                    dcc.Dropdown(id='pie_num')
                ]),
            ]),
            dbc.Col(dcc.Graph('update-piegraph',figure={}))
        ],width=4)
    ],style={'margin-right':'15px','margin-left':'15px','font-size':'small','padding-top':'8px'})
])