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
                          dcc.Store(id='pass_df1')
                          ],style={'margin-right':'-60px','margin-left':'15px'})

    layout = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=LOGO, height="30px")),
                            dbc.Col(dbc.NavbarBrand("Dash 4U", className="ms-2"),style={'padding-left':'5px'}),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="https://www.iqvia.com/",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink("NGraphs", href='/')),
                        dbc.NavItem(dbc.NavLink("MLGraphs", href='/MLGraphs')),
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
