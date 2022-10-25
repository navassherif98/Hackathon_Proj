import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.tree import  DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor

def LinearReg(df,dv,iv,inp):
    X = df[iv].values.reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, df[dv])

    r_sq = model.score(X, df[dv])
    intercept=model.intercept_
    slope=model.coef_

    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    fig = px.scatter(df, x=iv, y=dv, opacity=0.65)
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit'))
    if inp is None :
        result=0
    else :
        result=model.predict([[inp]])
        fig.add_traces(go.Scatter(x=[inp], y=result, mode = 'markers',marker_size=15,marker_symbol='star',name='Prediction'))

    return fig , r_sq , intercept , slope ,result

def DecisionTreeReg(df,dv,iv,inp):
    X = df[iv].values.reshape(-1, 1)

    model = KNeighborsRegressor()
    model.fit(X, df[dv])

    r_sq = model.score(X, df[dv])

    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    fig = px.scatter(df, x=iv, y=dv, opacity=0.65)
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit'))
    if inp is None :
        result=0
    else :
        result=model.predict([[inp]])
        fig.add_traces(go.Scatter(x=[inp], y=result, mode = 'markers',marker_size=15,marker_symbol='star',name='Prediction'))

    return fig , r_sq ,result

def KNNReg(df,dv,iv,inp):
    X = df[iv].values.reshape(-1, 1)

    model = DecisionTreeRegressor()
    model.fit(X, df[dv])

    r_sq = model.score(X, df[dv])

    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    fig = px.scatter(df, x=iv, y=dv, opacity=0.65)
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit'))
    if inp is None :
        result=0
    else :
        result=model.predict([[inp]])
        fig.add_traces(go.Scatter(x=[inp], y=result, mode = 'markers',marker_size=15,marker_symbol='star',name='Prediction'))

    return fig , r_sq ,result

def SVM(df,dv,iv1,iv2,inp1,inp2) :
    mesh_size = 1
    margin = 0


    X = df[[iv1, iv2]]
    y = df[dv]

    # Condition the model on sepal width and length, predict the petal width
    model = SVR(C=1.)
    model.fit(X, y)

    # Create a mesh grid on which we will run our model
    x_min, x_max = X[iv1].min() - margin, X[iv1].max() + margin
    y_min, y_max = X[iv2].min() - margin, X[iv2].max() + margin
    xrange = np.arange(x_min, x_max, mesh_size)
    yrange = np.arange(y_min, y_max, mesh_size)
    xx, yy = np.meshgrid(xrange, yrange)

    # Run model
    pred = model.predict(np.c_[xx.ravel(), yy.ravel()])
    pred = pred.reshape(xx.shape)

    if (inp1 is None) or (inp2 is None) :
        result=0
    else :
        result=model.predict([[inp1,inp2]])

    # Generate the plot
    fig = px.scatter_3d(df, x=iv1, y=iv2, z=dv)
    fig.update_traces(marker=dict(size=5))
    fig.add_traces(go.Surface(x=xrange, y=yrange, z=pred, name='pred_surface'))
    return fig,result