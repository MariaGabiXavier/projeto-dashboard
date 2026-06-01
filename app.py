import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

df = pd.read_csv('dados/enem_transformado.csv')

df = df[df['MEDIA_GERAL'] > 0]

# Opções hardcoded (para evitar .unique() em 2.6M de linhas)
opcoes_faixa = [
    {'label': 'Todas as idades', 'value': 'todas'},
    {'label': '17 anos', 'value': '17 anos'},
    {'label': '18 anos', 'value': '18 anos'},
    {'label': '19 anos', 'value': '19 anos'},
    {'label': '20 anos', 'value': '20 anos'},
    {'label': '21 anos', 'value': '21 anos'},
    {'label': '22 anos', 'value': '22 anos'},
    {'label': '23 anos', 'value': '23 anos'},
    {'label': '24 anos', 'value': '24 anos'},
    {'label': '25 anos', 'value': '25 anos'},
    {'label': '26-30 anos', 'value': '26-30 anos'},
    {'label': '31-35 anos', 'value': '31-35 anos'},
]

opcoes_escola = [
    {'label': 'Todas as escolas', 'value': 'todas'},
    {'label': 'Não Inf', 'value': 'Não Inf'},
    {'label': 'Pública', 'value': 'Pública'},
    {'label': 'Privada', 'value': 'Privada'}
]

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
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
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

    html.Div([

        html.H3(
            "Exploração Interativa de Dados ENEM 2023",
            style={
                "color": "#1e3a8a",
                "marginBottom": "5px",
                "fontWeight": "600"
            }
        ),

        html.P(
            "Analise padrões de desempenho por diferentes categorias e explore os dados em profundidade",
            style={
                "color": "#64748b",
                "fontSize": "14px",
                "marginBottom": "20px"
            }
        )

    ], style={"marginBottom": "30px"}),

    dbc.Row([

        dbc.Col([

            html.Div([

                html.Label("Selecione a Faixa Etária:", style={"fontWeight": "600", "color": "#1e3a8a"}),

                dcc.Dropdown(
                    id='filtro-faixa-etaria-dash2',
                    options=opcoes_faixa,
                    value='todas',
                    style={"width": "100%"}
                )

            ], style={
                "backgroundColor": "#f1f5f9",
                "padding": "15px",
                "borderRadius": "8px",
                "marginBottom": "15px"
            })

        ], width=6),

        dbc.Col([

            html.Div([

                html.Label("Selecione o Tipo de Escola:", style={"fontWeight": "600", "color": "#1e3a8a"}),

                dcc.Dropdown(
                    id='filtro-tipo-escola-dash2',
                    options=opcoes_escola,
                    value='todas',
                    style={"width": "100%"}
                )

            ], style={
                "backgroundColor": "#f1f5f9",
                "padding": "15px",
                "borderRadius": "8px",
                "marginBottom": "15px"
            })

        ], width=6)

    ]),

    html.Br(),

    dbc.Row([

        dbc.Col([

            dcc.Graph(id='grafico-notas-dash2')

        ], width=6),

        dbc.Col([

            dcc.Graph(id='grafico-sexo-dash2')

        ], width=6)

    ]),

    dbc.Row([

        dbc.Col([

            dcc.Graph(id='grafico-disciplinas-dash2')

        ], width=12)

    ]),

    dbc.Row([

        dbc.Col([

            dcc.Graph(id='grafico-raca-dash2')

        ], width=6),

        dbc.Col([

            dcc.Graph(id='grafico-desempenho-pie-dash2')

        ], width=6)

    ]),

    html.Br()

], fluid=True)


@app.callback(
    [
        Output('grafico-notas-dash2', 'figure'),
        Output('grafico-sexo-dash2', 'figure'),
        Output('grafico-disciplinas-dash2', 'figure'),
        Output('grafico-raca-dash2', 'figure'),
        Output('grafico-desempenho-pie-dash2', 'figure')
    ],
    [
        Input('filtro-faixa-etaria-dash2', 'value'),
        Input('filtro-tipo-escola-dash2', 'value')
    ]
)
def atualizar_graficos_dash2(faixa_etaria, tipo_escola):

    df_filtrado = df[df['MEDIA_GERAL'] > 0].copy()

    if faixa_etaria != 'todas':
        df_filtrado = df_filtrado[df_filtrado['TP_FAIXA_ETARIA'] == faixa_etaria]

    if tipo_escola != 'todas':
        df_filtrado = df_filtrado[df_filtrado['TP_ESCOLA'] == tipo_escola]
    
    # Validação: garantir que temos dados
    if len(df_filtrado) == 0:
        # Retornar gráficos vazios se não há dados
        fig_vazio = go.Figure().add_annotation(text="Nenhum dado disponível para este filtro")
        return fig_vazio, fig_vazio, fig_vazio, fig_vazio, fig_vazio

    # Gráfico 1: Box plot de distribuição de notas
    df_notas = pd.DataFrame({
        'CN': df_filtrado['NU_NOTA_CN'].dropna(),
        'CH': df_filtrado['NU_NOTA_CH'].dropna(),
        'LC': df_filtrado['NU_NOTA_LC'].dropna(),
        'MT': df_filtrado['NU_NOTA_MT'].dropna()
    })

    df_notas_melted = df_notas.melt(var_name='Disciplina', value_name='Nota').dropna()

    fig1 = px.box(
        df_notas_melted,
        x='Disciplina',
        y='Nota',
        title='Distribuição de Notas por Disciplina',
        color='Disciplina',
        color_discrete_sequence=['#578ee7', '#8b5cf6', '#06b6d4', '#f59e0b']
    )
    fig1 = estilizar_grafico(fig1)
    fig1.update_layout(showlegend=False, xaxis_title='Disciplina', yaxis_title='Notas')

    # Gráfico 2: Desempenho por sexo
    desempenho_sexo = df_filtrado.groupby('TP_SEXO')['MEDIA_GERAL'].agg(['mean', 'count']).reset_index()
    desempenho_sexo = desempenho_sexo[desempenho_sexo['count'] > 0].sort_values('mean', ascending=False)
    
    fig2 = px.bar(
        desempenho_sexo,
        x='TP_SEXO',
        y='mean',
        title='Desempenho Médio por Sexo',
        labels={'TP_SEXO': 'Sexo', 'mean': 'Média Geral'},
        color_discrete_sequence=['#8b5cf6']
    )
    fig2.update_traces(texttemplate='%{y:.1f}', textposition='outside')
    fig2 = estilizar_grafico(fig2)

    # Gráfico 3: Comparação de disciplinas (linha)
    medias = pd.DataFrame({
        'Disciplina': ['CN', 'CH', 'LC', 'MT'],
        'Média': [
            df_filtrado['NU_NOTA_CN'].mean(),
            df_filtrado['NU_NOTA_CH'].mean(),
            df_filtrado['NU_NOTA_LC'].mean(),
            df_filtrado['NU_NOTA_MT'].mean()
        ]
    })
    
    fig3 = px.line(medias, x='Disciplina', y='Média', markers=True, 
                   title='Comparação de Médias Entre Disciplinas',
                   color_discrete_sequence=['#06b6d4'])
    fig3.update_traces(marker=dict(size=10))
    fig3 = estilizar_grafico(fig3)

    # Gráfico 4: Desempenho por raça
    desempenho_raca = df_filtrado.groupby('TP_COR_RACA')['MEDIA_GERAL'].agg(['mean', 'count']).reset_index()
    desempenho_raca = desempenho_raca[desempenho_raca['count'] > 0].sort_values('mean', ascending=False)
    
    fig4 = px.bar(
        desempenho_raca,
        x='TP_COR_RACA',
        y='mean',
        title='Desempenho Médio por Cor/Raça',
        labels={'TP_COR_RACA': 'Cor/Raça', 'mean': 'Média Geral'},
        color_discrete_sequence=['#f59e0b']
    )
    fig4.update_traces(texttemplate='%{y:.1f}', textposition='outside')
    fig4.update_xaxes(tickangle=-45)
    fig4 = estilizar_grafico(fig4)

    # Gráfico 5: Pizza de desempenho
    dist_desempenho = df_filtrado['DESEMPENHO'].value_counts().reset_index()
    dist_desempenho.columns = ['DESEMPENHO', 'count']
    dist_desempenho['pct'] = (dist_desempenho['count'] / dist_desempenho['count'].sum() * 100).round(1)
    
    cores = {'Alto': '#10b981', 'Médio': '#f59e0b', 'Baixo': '#ef4444'}
    
    fig5 = px.pie(
        dist_desempenho,
        values='count',
        names='DESEMPENHO',
        title='Distribuição de Desempenho',
        color='DESEMPENHO',
        color_discrete_map=cores
    )
    fig5.update_traces(
        texttemplate='<b>%{label}</b><br>%{customdata:.1f}%',
        textposition='inside',
        customdata=dist_desempenho['pct']
    )
    fig5 = estilizar_grafico(fig5)

    return fig1, fig2, fig3, fig4, fig5

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