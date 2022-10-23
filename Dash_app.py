from dash import Dash, html, dcc ,dash_table
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc

import base64
import io

#connect to main app.py file
from app import app

from ML_algorithms import LinearReg,DecisionTreeReg,KNNReg

#connect to our pages
from pages import NGraphs,MLGraphs , navbar

nav = navbar.Navbar()

app.layout = html.Div([
    dcc.Location(id='url',refresh=False),
    dbc.Row(nav),
    html.Div(id='page-content',children=[])
])

@app.callback(Output('page-content','children'),
              Input('url','pathname'))
def display_page(pathname):
    if pathname == '/MLGraphs':
        return MLGraphs.layout
    elif pathname == '/':
        return  NGraphs.layout
    else:
        return "404 Page Error ! please choose a page"
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

@app.callback([Output('pass_df1','data'),Output('df_dv', 'options'),Output('df_iv', 'options')],
              Input('output-data-upload', 'data')
              )
def update_mlfilter(pds):
    try :
        df = pd.read_json(pds,orient="split")
        catg = df.select_dtypes(exclude=np.number)
        num = df.select_dtypes(include=np.number)
        collist=df.columns.unique()
        return pds, collist,collist
    except Exception as e:
        print(e)
        return [],[],[]


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

@app.callback(Output('ml-graph','figure'),Output('rsq','children'),
              Output('intercept','children'),Output('slope','children'),
              Output('result','children'),
              Input('pass_df1', 'data'),
              Input('df_iv','value'),
              Input('df_dv','value'),
              Input('df_inp','value'),
              Input('df_model','value'))
def mlgraph(pds,df_iv,df_dv,df_inp,df_model):
    try :
        df1 = pd.read_json(pds,orient="split")

        if df_model=="Linear Regression" :
            fig,r_sqr,intercept,slope,result=LinearReg(df1,df_dv,df_iv,df_inp)
            return fig , f'R Squre : {r_sqr}' , f'Intercept : {intercept}' , f'Slope : {slope}', f'Predicted Output : {result}'
        elif(df_model =='Decision Tree Regression'):
            fig,r_sqr,result=DecisionTreeReg(df1,df_dv,df_iv,df_inp)
            return fig , f'R Squre : {r_sqr}' , [] , [], f'Predicted Output : {result}'
        else:
            fig,r_sqr,result=KNNReg(df1,df_dv,df_iv,df_inp)
            return fig , f'R Squre : {r_sqr}' , [] , [], f'Predicted Output : {result}'


    except Exception as e:
        print(e)
        return {},[],[],[],[]


if __name__ == '__main__':
    app.run_server(debug=False)
