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

from ML_algorithms import LinearReg,DecisionTreeReg,KNNReg,SVM

#connect to our pages
from pages import NGraphs,MLGraphs , navbar , EDA

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
    elif pathname == '/Dash4u':
        return  NGraphs.layout
    elif pathname == '/':
        return EDA.layout
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
              Input('pre_processed_df', 'data')
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

@app.callback([Output('pass_df1','data'),Output('df_dv', 'options'),Output('df_iv', 'options'),Output('df_iv2', 'options')],
              Input('pre_processed_df', 'data')
              )
def update_mlfilter(pds):
    try :
        df = pd.read_json(pds,orient="split")
        numcolist = df.select_dtypes(include=np.number).columns.unique()
        return pds, numcolist,numcolist,numcolist
    except Exception as e:
        print(e)
        return [],[],[],[]


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
              Output('graph_nm','children'),
              Input('pass_df1', 'data'),
              Input('df_iv','value'),
              Input('df_iv2','value'),
              Input('df_dv','value'),
              Input('df_inp','value'),
              Input('df_inp2','value'),
              Input('df_model','value'))
def mlgraph(pds,df_iv,df_iv2,df_dv,df_inp,df_inp2,df_model):
    try :
        df1 = pd.read_json(pds,orient="split")

        if df_model=="Linear Regression" :
            fig,r_sqr,intercept,slope,result=LinearReg(df1,df_dv,df_iv,df_inp)
            return fig , f'R Squre : {r_sqr}' , f'Intercept : {intercept}' , f'Slope : {slope}', f'Predicted Output : {result}' , df_model
        elif(df_model =='Decision Tree Regression'):
            fig,r_sqr,result=DecisionTreeReg(df1,df_dv,df_iv,df_inp)
            return fig , f'R Squre : {r_sqr}' , [] , [], f'Predicted Output : {result}',df_model
        elif(df_model =='SVM'):
            fig,result=SVM(df1,df_dv,df_iv,df_iv2,df_inp,df_inp2)
            return fig ,[],[],[],f'Predicted Output : {result}',df_model
        else:
            fig,r_sqr,result=KNNReg(df1,df_dv,df_iv,df_inp)
            return fig , f'R Squre : {r_sqr}' , [] , [], f'Predicted Output : {result}',df_model


    except Exception as e:
        print(e)
        return {},[],[],[],[],[]
@app.callback(Output('pass_df2','data'),Output('clmn_rm','options'),Output('clmn_null_rm','options'),
              Input('output-data-upload', 'data')
              )
def update_edafilter(pds):
    try :
        df = pd.read_json(pds,orient="split")
        colist=df.columns.unique()
        lst=[]
        for i in df.columns:
            if df[i].isnull().sum() > 0:
                lst.append(i)

        #numcolist = df.select_dtypes(include=np.number).columns.unique()
        return pds ,colist ,lst
    except Exception as e:
        print(e)
        return [],[],[]

def prop_cal(df2,typ):
    lst=[]
    if typ=="Meta":
        lst.append(["Shape","Rows :"+str(df2.shape[0])+" Columns :"+str(df2.shape[1])])
        lst.append(["Total Count",len(df2)])
        lst.append(["Unique Rows",len(df2.drop_duplicates())])
        lst.append(["Duplicate Rows",df2.duplicated(keep='first').sum()])
        propdf=pd.DataFrame(lst,columns=["Properties","Value"])
    else :
        if typ=="Blank":
            for i in df2.columns:
                if df[i].eq("").sum() > 0 :
                    lst.append([i,df[i].eq("").sum()])
        elif typ=="Data_Types":
            for i in df2.columns:
                lst.append(([i,str(df2.dtypes[i])]))
        elif typ=="Null":
            for i in df2.columns:
                if df2[i].isnull().sum() > 0:
                    lst.append([i,df2[i].isnull().sum()])
        else:
            for i in df2.select_dtypes(include=np.number).columns :
                if typ=="Mean":
                    lst.append([i,round(df2[i].mean(),3)])
                elif typ=="Median":
                    lst.append([i,round(df2[i].median(),3)])
                elif typ=="Max":
                    lst.append([i,round(df2[i].max(),3)])
                elif typ=="Min":
                    lst.append([i,round(df2[i].min(),3)])
        propdf=pd.DataFrame(lst,columns=["Column Name",typ])
    return propdf

@app.callback(Output('pre_processed_df','data'),Output('corr_graph','figure'),
              (Output('card-content','children')),
              Input('pass_df2', 'data'),
              Input("card-tabs", "active_tab"),
              Input('clmn_rm','value'),
              Input('clmn_null_rm','value'),
              Input('null_procs_mthd','value'),
              Input('null_custm','value'))
def update_eda(pds,prop_tab,clmm_rm,clmn_null_rm,null_procs_mthd,null_custm):
    try :
        df2 = pd.read_json(pds,orient="split")
        if clmm_rm is not None:
            df2.drop(clmm_rm, inplace=True, axis=1)
        if null_procs_mthd=="Remove Null Values":
            if clmn_null_rm is not None:
                for i in clmn_null_rm:
                    df2.dropna(inplace=True,subset=[i])
        elif null_procs_mthd=="Use Custom value":
            if clmn_null_rm is not None:
                if (null_custm is not None) or null_custm == "" :
                    for i in clmn_null_rm:
                        df2[i].fillna(float(null_custm), inplace = True)
        if df2 is None:
            fig={}
        else :
            corr_matrix = df2.corr()
            fig = px.imshow(corr_matrix)
        if prop_tab is not None:
            propdf=prop_cal(df2,prop_tab)
            table = dbc.Table.from_dataframe(propdf,striped=False, bordered=True, hover=True,size='sm',style={'padding':'0px','font-size':'small'})
        else:
            table=""
        return df2.to_json(orient="split"),fig ,table
    except Exception as e:
        print(e)
        return [],{} , ""


if __name__ == '__main__':
    app.run_server(debug=False)
