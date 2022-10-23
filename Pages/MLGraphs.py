from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Col(dbc.Row(dcc.Graph('ml-graph')))],width=9),

        dbc.Col([
            dbc.Row(html.Div("Dash Tools"),style={'font-size':'large','padding':'10px','justify-content':'center'}),
            dbc.Row(html.Div("Select ML Model :",style={'padding':'5px'})),
            dbc.Row(dcc.Dropdown(['Linear Regression','Decision Tree Regression','K-NN Regression'],'Linear Regression',id='df_model',style={'width':'-webkit-fill-available'})),
            dbc.Row(html.Div("Select Dependent Var :",style={'padding':'5px'})),
            dbc.Row(dcc.Dropdown(id='df_dv',style={'width':'-webkit-fill-available'})),
            dbc.Row(html.Div("Select Independent Var :",style={'padding':'5px'})),
            dbc.Row(dcc.Dropdown(id='df_iv',style={'width':'-webkit-fill-available'})),
            dbc.Row(html.Div("Input for Prediction : ",style={'padding':'5px'})),
            dbc.Row(dbc.Input(id='df_inp',type="number",style={'width':'-webkit-fill-available'})),
            dbc.Row([
                dbc.Card(dbc.CardBody([
                    dbc.Row(html.Div(id='rsq')),
                    dbc.Row(html.Div(id='intercept')),
                    dbc.Row(html.Div(id='slope')),
                    dbc.Row(html.Div(id="result",style={'color':'green'}))
                ]),style={'width':'-webkit-fill-available'})
            ],style={'padding-top':'20px'})
        ],style={'font-size':'small'},width=3)
    ],style={'margin-right':'15px','margin-left':'15px','padding-top':'10px'})
])