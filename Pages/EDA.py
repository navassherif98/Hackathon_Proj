from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

corr=dbc.Card([
    dbc.CardHeader("Correlation Matrix",style={'padding-top':'7px','padding-bottom':'7px'}),
    dbc.CardBody([
            dcc.Graph(id='corr_graph')
        ],style={'padding':'0px'})
])

pre_process=dbc.Card([
    dbc.CardHeader("Data Pre-Processing",style={'padding-top':'7px','padding-bottom':'7px'}),
    dbc.CardBody([
        dbc.Row([
            dbc.Col(html.Div("Select columns to be removed:",style={'padding-top':"5px",}),width=5),
            dbc.Col(dcc.Dropdown(id="clmn_rm",multi=True,style={'width':'-webkit-fill-available'}),width=7,style={'padding':'0px'})
                 ],style={'font-size':'small'}),
        dbc.Row([
            dbc.Col(html.Div("Choose option to process Null Values:",style={'padding-top':"5px",}),width=5),
            dbc.Col(dcc.Dropdown(id="clmn_null_rm",multi=True,style={'padding-right':'1px','width':'-webkit-fill-available'}),width=3,style={'padding':'0px'}),
            dbc.Col(dcc.Dropdown(['None','Remove Null Values','Use Custom value'],'None',id='null_procs_mthd',style={'padding':'0px','width':'-webkit-fill-available'}),width=3),
            dbc.Col(dbc.Input(id='null_custm'),width=1,style={'padding':'0px'})
        ],style={'font-size':'small','padding-top':'10px'}),


    ])
],style={'width':'-webkit-fill-available'})

prop = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Meta", tab_id="Meta"),
                    dbc.Tab(label="Data_Types", tab_id="Data_Types"),
                    dbc.Tab(label="Mean", tab_id="Mean"),
                    dbc.Tab(label="Median", tab_id="Median"),
                    dbc.Tab(label="Max", tab_id="Max"),
                    dbc.Tab(label="Min", tab_id="Min"),
                    dbc.Tab(label="Null", tab_id="Null"),
                    dbc.Tab(label="Blank", tab_id="Blank"),
                ],
                id="card-tabs",
                active_tab="Meta",
            )
        ,style={"padding":'0px','border-bottom-width':'0px'}),
        dbc.CardBody(html.Div(id="card-content")),

])

summary=dbc.Card([
        dbc.CardHeader("Summary",style={'padding-top':'7px','padding-bottom':'7px'}),
        dbc.CardBody([
        prop
        ])
],style={'width':'-webkit-fill-available'})

layout=html.Div([
        dbc.Row([
            dbc.Col(corr,style={'padding':'10px'}),
            dbc.Col([
                dbc.Row(pre_process,style={'padding-bottom':'10px'}),
                dbc.Row(summary)
            ],style={'padding':'10px'})
        ],style={'padding-left':'15px'})
])