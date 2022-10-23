import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.tree import  DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor

def LinearReg(df,dv,iv,inp):
    X = df[dv].values.reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, df[iv])

    r_sq = model.score(X, df[iv])
    intercept=model.intercept_
    slope=model.coef_

    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    fig = px.scatter(df, x=dv, y=iv, opacity=0.65)
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit'))
    if inp is None :
        result=0
    else :
        result=model.predict([[inp]])
        fig.add_traces(go.Scatter(x=[inp], y=result, mode = 'markers',marker_size=15,marker_symbol='star',name='Prediction'))

    return fig , r_sq , intercept , slope ,result

def DecisionTreeReg(df,dv,iv,inp):
    X = df[dv].values.reshape(-1, 1)

    model = KNeighborsRegressor()
    model.fit(X, df[iv])

    r_sq = model.score(X, df[iv])

    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    fig = px.scatter(df, x=dv, y=iv, opacity=0.65)
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit'))
    if inp is None :
        result=0
    else :
        result=model.predict([[inp]])
        fig.add_traces(go.Scatter(x=[inp], y=result, mode = 'markers',marker_size=15,marker_symbol='star',name='Prediction'))

    return fig , r_sq ,result

def KNNReg(df,dv,iv,inp):
    X = df[dv].values.reshape(-1, 1)

    model = DecisionTreeRegressor()
    model.fit(X, df[iv])

    r_sq = model.score(X, df[iv])

    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    fig = px.scatter(df, x=dv, y=iv, opacity=0.65)
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit'))
    if inp is None :
        result=0
    else :
        result=model.predict([[inp]])
        fig.add_traces(go.Scatter(x=[inp], y=result, mode = 'markers',marker_size=15,marker_symbol='star',name='Prediction'))

    return fig , r_sq ,result