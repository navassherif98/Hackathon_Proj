from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

def Navbar():
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
                          dcc.Store(id='pass_df1'),
                          dcc.Store(id='pass_df2'),
                          dcc.Store(id='pre_processed_df')
                          ],style={'margin-right':'-60px','margin-left':'15px'})

    layout = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=LOGO, height="30px")),
                            dbc.Col(dbc.NavbarBrand("Intelli Dash", className="ms-2"),style={'padding-left':'5px'}),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="https://www.iqvia.com/",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink("EDA", href='/')),
                        dbc.NavItem(dbc.NavLink("Dash_4u", href='/Dash4u')),
                        dbc.NavItem(dbc.NavLink("ML_Graphs", href='/MLGraphs')),
                    ],
                    color="dark",
                    dark=True,
                    style={'padding':'0px'}
                ),
                uploadfile
            ]
        ),
        color="dark",
        dark=True,style={'width': '-webkit-fill-available'}
    )

    return layout
