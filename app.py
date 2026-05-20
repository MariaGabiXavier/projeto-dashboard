import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv('dados/enem_transformado.csv')

df = df[df['MEDIA_GERAL'] > 0]

media_geral = round(df['MEDIA_GERAL'].mean(), 2)
maior_media = round(df['MEDIA_GERAL'].max(), 2)

participantes = len(df)

estado_top = (
    df.groupby('SG_UF_PROVA')['MEDIA_GERAL']
    .mean()
    .sort_values(ascending=False)
    .index[0]
)

graf_estado = (
    df.groupby('SG_UF_PROVA')['MEDIA_GERAL']
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig_estado = px.bar(
    graf_estado,
    x='SG_UF_PROVA',
    y='MEDIA_GERAL',
    text='MEDIA_GERAL',
    title='Média por Estado'
)

fig_estado.update_layout(
    xaxis_title='UF',
    yaxis_title='Média',
    yaxis=dict(range=[470, 570])
)

fig_estado.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside',
    marker_color='#578ee7',
    marker_line_width=0
)

def estilizar_grafico(fig):

    fig.update_layout(

        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        font=dict(
            family='Sora',
            color='#334155'
        ),

        title=dict(
            font=dict(
                size=22,
                color='#1e3a8a'
            ),
            x=0.03
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        xaxis=dict(
            showgrid=False,
            linecolor='#e2e8f0',
            tickfont=dict(color='#64748b')
        ),

        yaxis=dict(
            gridcolor='#eff6ff',
            zeroline=False,
            tickfont=dict(color='#64748b')
        )
    )

    return fig

fig_estado = estilizar_grafico(fig_estado)

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

def criar_card(titulo, valor, icone):

    return dbc.Card(

        dbc.CardBody([

            html.Div([

                html.Div([

                    html.H5(
                        titulo,
                        className='card-titulo'
                    ),

                    html.H2(
                        valor,
                        className='card-valor'
                    )

                ]),

                html.Div([

                    html.Img(
                        src=icone,
                        className='imagem-card'
                    )

                ], className='icone-card')

            ], className='card-topo')

        ]),

        className='card-dashboard'
    )

def criar_menu(pathname):

    return html.Div([

        dcc.Link(

            "Dashboard 1",

            href="/",

            style={

                "textDecoration": "none",

                "paddingBottom": "10px",

                "borderBottom":
                    "3px solid #1e3a8a"
                    if pathname == "/"
                    else "3px solid transparent",

                "color":
                    "#1e3a8a"
                    if pathname == "/"
                    else "#94a3b8",

                "fontWeight":
                    "600"
                    if pathname == "/"
                    else "500",

                "fontSize": "16px",

                "marginRight": "40px",

                "transition": "all 0.3s ease"

            }

        ),

        dcc.Link(

            "Dashboard 2",

            href="/dashboard2",

            style={

                "textDecoration": "none",

                "paddingBottom": "10px",

                "borderBottom":
                    "3px solid #1e3a8a"
                    if pathname == "/dashboard2"
                    else "3px solid transparent",

                "color":
                    "#1e3a8a"
                    if pathname == "/dashboard2"
                    else "#94a3b8",

                "fontWeight":
                    "600"
                    if pathname == "/dashboard2"
                    else "500",

                "fontSize": "16px",

                "transition": "all 0.3s ease"

            }

        )

    ],

    style={

        "display": "flex",

        "justifyContent": "center",

        "alignItems": "center",

        "borderBottom": "1px solid #e2e8f0",

        "marginTop": "25px",

        "paddingBottom": "10px"

    })

pagina_dashboard_1 = dbc.Container([

    html.Br(),

    dbc.Row([

        dbc.Col(
            criar_card(
                "Média Geral",
                media_geral,
                "../assets/icon_grafico.png"
            ),
            width=3
        ),

        dbc.Col(
            criar_card(
                "Participantes",
                participantes,
                "../assets/icon_participantes.png"
            ),
            width=3
        ),

        dbc.Col(
            criar_card(
                "Maior Média",
                maior_media,
                "../assets/icon_maiorMedia.png"
            ),
            width=3
        ),

        dbc.Col(
            criar_card(
                "Estado Destaque",
                estado_top,
                "../assets/icon_brasil.png"
            ),
            width=3
        )

    ]),

    html.Br(),

    dbc.Card([

        dbc.CardBody([

            html.H4(
                "Resumo Executivo",
                className='titulo-resumo'
            ),

            html.P(
                """
                Os dados indicam diferenças relevantes de desempenho entre estados.
                O gráfico abaixo apresenta a média geral dos participantes por UF.
                """,
                className='texto-resumo'
            )

        ])

    ],
    className='card-resumo'),

    html.Br(),

    dbc.Row([

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(
                        figure=fig_estado,
                        config={'displayModeBar': False}
                    )
                ]),
                className='grafico-card'
            ),
            width=12
        )

    ])

], fluid=True)

pagina_dashboard_2 = dbc.Container([

    html.Br(),

    html.Div(

        children=[

            html.H3(
                "Dashboard 2",
                style={
                    "color": "#94a3b8"
                }
            ),

            html.P(
                "desenvolver aqui.",
                style={
                    "color": "#94a3b8"
                }
            )

        ],

        style={
            "height": "500px",
            "backgroundColor": "white",
            "borderRadius": "12px",
            "padding": "30px"
        }
    )

], fluid=True)

app.layout = html.Div([

    dcc.Location(id='url', refresh=False),

    dbc.Container([

        html.Div([

            html.H1(
                "Dashboard ENEM 2023",
                className='titulo-principal'
            ),

            html.P(
                "Visão geral dos dados e principais indicadores",
                className='subtitulo'
            ),

            html.Div(id='menu-dinamico')

        ]),

        html.Div(id='conteudo-pagina')

    ], fluid=True)

])

@app.callback(

    Output('menu-dinamico', 'children'),
    Input('url', 'pathname')

)

def atualizar_menu(pathname):

    return criar_menu(pathname)

@app.callback(
    Output('conteudo-pagina', 'children'),
    Input('url', 'pathname')
)

def renderizar_pagina(pathname):

    if pathname == '/dashboard2':
        return pagina_dashboard_2

    return pagina_dashboard_1

if __name__ == '__main__':
    app.run(debug=True)