from dash import Dash, html, dcc ,dash_table
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc

import base64
import io

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

LOGO ="https://images.plot.ly/logo/new-branding/plotly-logomark.png"

uploadfile = dbc.Row([dbc.Col(dcc.Upload(id='upload-data',children=html.Div(['Drag and Drop or ',html.A('Select Files')]),
                                         style={
                                             'width':'400px',
                                             'height': '40px',
                                             'lineHeight': '40px',
                                             'borderWidth': '1px',
                                             'borderStyle': 'dashed',
                                             'borderRadius': '5px',
                                             'textAlign': 'center',
                                             'background-color':'white'
                                         },
                                         # Allow multiple files to be uploaded
                                         multiple=True),align="center",),
                      dcc.Store(id='output-data-upload'),
                      dcc.Store(id='pass_df'),
                      ],style={'margin-right':'-60px','margin-left':'15px'})

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Dash 4U", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://www.iqvia.com/",
                style={"textDecoration": "none"},
            ),
            uploadfile
        ]
    ),
    color="dark",
    dark=True,style={'width': '-webkit-fill-available'}
)

app.layout = html.Div([
    dbc.Row(navbar,style={'padding-bottom':'20px'}),
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
    ],style={'margin-right':'15px','margin-left':'15px'})
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    global df
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
    return df

@app.callback(Output('output-data-upload', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              )
def upload_file(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n ) for c, n in
            zip(list_of_contents, list_of_names )]
        return df.to_json(orient="split")

@app.callback([Output('df_x', 'options'),Output('df_y', 'options'),Output('pie_catg', 'options'),Output('pie_num', 'options')
                  ,Output('df_fltr','options'),Output('pass_df','data')],
              Input('output-data-upload', 'data')
              )
def update_filter(pds):
    try :
        df = pd.read_json(pds,orient="split")
        catg = df.select_dtypes(exclude=np.number)
        num = df.select_dtypes(include=np.number)
        collist=df.columns.unique()
        return collist,collist,catg.columns.unique(),num.columns.unique(),collist, pds
    except Exception as e:
        print(e)
        return [],[],[],[],[],[]

@app.callback(Output('update-graph', 'figure'),Output('df_fltr_colmn','options'),
              Input('pass_df', 'data'),
              Input('graph_dropdown','value'),
              Input('df_x','value'),
              Input('df_y','value'),
              Input('df_fltr','value'),
              Input('df_fltr_colmn','value')
              )
def update_graph(pds,graph_typ,df_x,df_y,df_fltr,df_fltr_val):
    try :
        df = pd.read_json(pds,orient="split")

        if df_fltr is not None :
            fltrcolval=df[df_fltr].unique()
        else :
            fltrcolval=[]

        if (df_fltr_val is not None) and (df_fltr_val != []):
            df=df.loc[df[df_fltr].isin(df_fltr_val)]

        if (graph_typ=="Scatter") :
            fig = px.scatter(df, x=df_x, y=df_y)
        elif (graph_typ=="Horizontal Bar") :
            if df_fltr is not None :
                fig = px.bar(df, x=df_x, y=df_y,orientation='h',color=df_fltr)
            else :
                fig = px.bar(df, x=df_x, y=df_y,orientation='h')
        elif (graph_typ=="Horizontal Stacked Bar") :
            if df_fltr is not None :
                fig = px.bar(df, x=df_x, y=df_y,orientation='h',color=df_fltr)
            else :
                fig = px.bar(df, x=df_x, y=df_y,orientation='h')
        elif (graph_typ=="Vertical Bar") :
            if df_fltr is not None :
                fig = px.bar(df, x=df_x, y=df_y,color=df_fltr)
            else :
                fig = px.bar(df, x=df_x, y=df_y)
        elif (graph_typ=="Vertical Stacked Bar") :
            if df_fltr is not None :
                fig = px.bar(df, x=df_x, y=df_y,color=df_fltr)
            else :
                fig = px.bar(df, x=df_x, y=df_y)
        elif (graph_typ=="Box Plot"):
            df = px.data.tips()
            fig = px.box(df,  x="time", y="total_bill", points="all")
        elif (graph_typ=="Tree Map"):
            fig = px.treemap(data_frame= df,path = [df_x] ,values = df_y)
        elif (graph_typ=="Histogram"):
            fig = px.histogram(df, x=df_x,nbins=20)
        else :
            if df_fltr is not None :
                fig = px.line(data_frame=df, x=df[df_x], y=df[df_y],color=df_fltr)
            else :
                fig = px.line(data_frame=df, x=df[df_x], y=df[df_y])
            fig.update_traces(mode='lines+markers')
        return fig , fltrcolval
    except Exception as e:
        print(e)
        return {} , []

@app.callback(Output('update-piegraph','figure'),
              Input('pass_df', 'data'),
              Input('df_x','value'),
              Input('df_y','value'),
              Input('update-graph', 'clickData'),
              Input('df_fltr','value'),
              Input('df_fltr_colmn','value'),
              Input('pie_catg','value'),
              Input('pie_num','value'),
)
def update_piegraph(pds,df_x,df_y,hov_data,df_fltr,df_fltr_val,pie_catg,pie_num):
    try :
        df = pd.read_json(pds,orient="split")
        if (df_fltr_val is not None) and (df_fltr_val != []):
            df=df.loc[df[df_fltr].isin(df_fltr_val)]

        if hov_data is None:
            if pie_catg is not None:
                fig2 = px.pie(df, values=pie_num, names=pie_catg, hole=.3)
            else :
                fig2 = px.pie(df, values=df_x, names=df_y, hole=.3)
            return fig2
        else:
            hov_val = hov_data['points'][0]['x']
            df1 = df.loc[df[df_x].isin([hov_val])]
            if pie_catg is not None:
                fig2 = px.pie(df, values=pie_num, names=pie_catg, hole=.3)
            else:
                fig2 = px.pie(df1, values=df_x, names=df_y, hole=.3)
            return fig2
    except Exception as e:
        print(e)
        return {}


if __name__ == '__main__':
    app.run_server(debug=False)
