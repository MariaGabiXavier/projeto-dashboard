import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

df = pd.read_csv('dados/enem_transformado.csv')

df = df[df['MEDIA_GERAL'] > 0]

# ──────────────────────────────────────────────
# Opções de filtros
# ──────────────────────────────────────────────

opcoes_faixa = [
    {'label': 'Todas as idades', 'value': 'todas'},
    {'label': 'Menor de 17', 'value': 'Menor de 17'},
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
    {'label': '36-40 anos', 'value': '36-40 anos'},
    {'label': '41-45 anos', 'value': '41-45 anos'},
    {'label': '46-50 anos', 'value': '46-50 anos'},
    {'label': '51-55 anos', 'value': '51-55 anos'},
    {'label': '56-60 anos', 'value': '56-60 anos'},
    {'label': '61-65 anos', 'value': '61-65 anos'},
    {'label': '66-70 anos', 'value': '66-70 anos'},
    {'label': 'Maior de 70', 'value': 'Maior de 70'},
]

opcoes_escola = [
    {'label': 'Todas as escolas', 'value': 'todas'},
    {'label': 'Não Inf', 'value': 'Não Inf'},
    {'label': 'Pública', 'value': 'Pública'},
    {'label': 'Privada', 'value': 'Privada'}
]

opcoes_estado = [{'label': 'Todos os estados', 'value': 'todos'}] + [
    {'label': uf, 'value': uf}
    for uf in sorted(df['SG_UF_PROVA'].dropna().unique())
]

opcoes_sexo = [
    {'label': 'Todos', 'value': 'todos'},
    {'label': 'Feminino', 'value': 'F'},
    {'label': 'Masculino', 'value': 'M'},
]

opcoes_raca = [{'label': 'Todas', 'value': 'todas'}] + [
    {'label': r, 'value': r}
    for r in sorted(df['TP_COR_RACA'].dropna().unique())
]

opcoes_desempenho = [
    {'label': 'Todos', 'value': 'todos'},
    {'label': 'Alto', 'value': 'Alto'},
    {'label': 'Médio', 'value': 'Médio'},
    {'label': 'Baixo', 'value': 'Baixo'},
]

# ──────────────────────────────────────────────
# KPIs do Dashboard 1
# ──────────────────────────────────────────────

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

# ──────────────────────────────────────────────
# Função de estilo padrão
# ──────────────────────────────────────────────

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
        margin=dict(l=20, r=20, t=60, b=20),
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

# ──────────────────────────────────────────────
# App
# ──────────────────────────────────────────────

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# ──────────────────────────────────────────────
# Componentes reutilizáveis
# ──────────────────────────────────────────────

def criar_card(titulo, valor, icone):
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                html.Div([
                    html.H5(titulo, className='card-titulo'),
                    html.H2(valor, className='card-valor')
                ]),
                html.Div([
                    html.Img(src=icone, className='imagem-card')
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
                "borderBottom": "3px solid #1e3a8a" if pathname == "/" else "3px solid transparent",
                "color": "#1e3a8a" if pathname == "/" else "#94a3b8",
                "fontWeight": "600" if pathname == "/" else "500",
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
                "borderBottom": "3px solid #1e3a8a" if pathname == "/dashboard2" else "3px solid transparent",
                "color": "#1e3a8a" if pathname == "/dashboard2" else "#94a3b8",
                "fontWeight": "600" if pathname == "/dashboard2" else "500",
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


def estilo_filtro():
    return {
        "backgroundColor": "#f1f5f9",
        "padding": "15px",
        "borderRadius": "8px",
        "marginBottom": "15px"
    }


def label_filtro(texto):
    return html.Label(texto, style={"fontWeight": "600", "color": "#1e3a8a", "marginBottom": "6px"})

# ──────────────────────────────────────────────
# Dashboard 1
# ──────────────────────────────────────────────

pagina_dashboard_1 = dbc.Container([

    html.Br(),

    dbc.Row([
        dbc.Col(criar_card("Média Geral", media_geral, "../assets/icon_grafico.png"), width=3),
        dbc.Col(criar_card("Participantes", participantes, "../assets/icon_participantes.png"), width=3),
        dbc.Col(criar_card("Maior Média", maior_media, "../assets/icon_maiorMedia.png"), width=3),
        dbc.Col(criar_card("Estado Destaque", estado_top, "../assets/icon_brasil.png"), width=3),
    ]),

    html.Br(),

    dbc.Card([
        dbc.CardBody([
            html.H4("Resumo Executivo", className='titulo-resumo'),
            html.P(
                """
                Os dados indicam diferenças relevantes de desempenho entre estados.
                O gráfico abaixo apresenta a média geral dos participantes por UF.
                """,
                className='texto-resumo'
            )
        ])
    ], className='card-resumo'),

    html.Br(),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(figure=fig_estado, config={'displayModeBar': False})
                ]),
                className='grafico-card'
            ),
            width=12
        )
    ])

], fluid=True)

# ──────────────────────────────────────────────
# Dashboard 2
# ──────────────────────────────────────────────

pagina_dashboard_2 = dbc.Container([

    html.Br(),

    html.Div([
        html.H3(
            "Exploração Interativa de Dados ENEM 2023",
            style={"color": "#1e3a8a", "marginBottom": "5px", "fontWeight": "600"}
        ),
        html.P(
            "Analise padrões de desempenho por diferentes categorias e explore os dados em profundidade",
            style={"color": "#64748b", "fontSize": "14px", "marginBottom": "20px"}
        )
    ], style={"marginBottom": "20px"}),

    # ── Filtros ──
    dbc.Row([
        dbc.Col([
            html.Div([
                label_filtro("Faixa Etária:"),
                dcc.Dropdown(
                    id='filtro-faixa-etaria-dash2',
                    options=opcoes_faixa,
                    value='todas',
                    style={"width": "100%"}
                )
            ], style=estilo_filtro())
        ], width=4),

        dbc.Col([
            html.Div([
                label_filtro("Tipo de Escola:"),
                dcc.Dropdown(
                    id='filtro-tipo-escola-dash2',
                    options=opcoes_escola,
                    value='todas',
                    style={"width": "100%"}
                )
            ], style=estilo_filtro())
        ], width=4),

        dbc.Col([
            html.Div([
                label_filtro("Estado (UF):"),
                dcc.Dropdown(
                    id='filtro-estado-dash2',
                    options=opcoes_estado,
                    value='todos',
                    style={"width": "100%"}
                )
            ], style=estilo_filtro())
        ], width=4),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                label_filtro("Sexo:"),
                dcc.Dropdown(
                    id='filtro-sexo-dash2',
                    options=opcoes_sexo,
                    value='todos',
                    style={"width": "100%"}
                )
            ], style=estilo_filtro())
        ], width=4),

        dbc.Col([
            html.Div([
                label_filtro("Cor/Raça:"),
                dcc.Dropdown(
                    id='filtro-raca-dash2',
                    options=opcoes_raca,
                    value='todas',
                    style={"width": "100%"}
                )
            ], style=estilo_filtro())
        ], width=4),

        dbc.Col([
            html.Div([
                label_filtro("Nível de Desempenho:"),
                dcc.Dropdown(
                    id='filtro-desempenho-dash2',
                    options=opcoes_desempenho,
                    value='todos',
                    style={"width": "100%"}
                )
            ], style=estilo_filtro())
        ], width=4),
    ]),

    html.Br(),

    # ── Linha 1: Escola + Redação ──
    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id='grafico-escola-dash2', config={'displayModeBar': False})
            ]), className='grafico-card')
        ], width=6),

        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id='grafico-redacao-dash2', config={'displayModeBar': False})
            ]), className='grafico-card')
        ], width=6),
    ]),

    html.Br(),

    # ── Linha 2: Renda (boxplot) ──
    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id='grafico-renda-dash2', config={'displayModeBar': False})
            ]), className='grafico-card')
        ], width=12),
    ]),

    html.Br(),

    # ── Linha 3: Correlação + Faixa Etária ──
    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id='grafico-correlacao-dash2', config={'displayModeBar': False})
            ]), className='grafico-card')
        ], width=6),

        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id='grafico-idade-dash2', config={'displayModeBar': False})
            ]), className='grafico-card')
        ], width=6),
    ]),

    html.Br(),

    # ── Linha 4: Distribuição de notas + Pizza ──
    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id='grafico-notas-dash2', config={'displayModeBar': False})
            ]), className='grafico-card')
        ], width=6),

        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id='grafico-desempenho-pie-dash2', config={'displayModeBar': False})
            ]), className='grafico-card')
        ], width=6),
    ]),

    html.Br(),

    # ── Linha 5: Sexo + Raça ──
    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id='grafico-sexo-dash2', config={'displayModeBar': False})
            ]), className='grafico-card')
        ], width=6),

        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id='grafico-raca-dash2', config={'displayModeBar': False})
            ]), className='grafico-card')
        ], width=6),
    ]),

    html.Br(),

    # ── Linha 6: Disciplinas ──
    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                dcc.Graph(id='grafico-disciplinas-dash2', config={'displayModeBar': False})
            ]), className='grafico-card')
        ], width=12),
    ]),

    html.Br()

], fluid=True)

# ──────────────────────────────────────────────
# Callback Dashboard 2
# ──────────────────────────────────────────────

@app.callback(
    [
        Output('grafico-escola-dash2', 'figure'),
        Output('grafico-redacao-dash2', 'figure'),
        Output('grafico-renda-dash2', 'figure'),
        Output('grafico-correlacao-dash2', 'figure'),
        Output('grafico-idade-dash2', 'figure'),
        Output('grafico-notas-dash2', 'figure'),
        Output('grafico-desempenho-pie-dash2', 'figure'),
        Output('grafico-sexo-dash2', 'figure'),
        Output('grafico-raca-dash2', 'figure'),
        Output('grafico-disciplinas-dash2', 'figure'),
    ],
    [
        Input('filtro-faixa-etaria-dash2', 'value'),
        Input('filtro-tipo-escola-dash2', 'value'),
        Input('filtro-estado-dash2', 'value'),
        Input('filtro-sexo-dash2', 'value'),
        Input('filtro-raca-dash2', 'value'),
        Input('filtro-desempenho-dash2', 'value'),
    ]
)
def atualizar_graficos_dash2(faixa_etaria, tipo_escola, estado, sexo, raca, desempenho):

    df_filtrado = df.copy()

    if faixa_etaria != 'todas':
        df_filtrado = df_filtrado[df_filtrado['TP_FAIXA_ETARIA'] == faixa_etaria]
    if tipo_escola != 'todas':
        df_filtrado = df_filtrado[df_filtrado['TP_ESCOLA'] == tipo_escola]
    if estado != 'todos':
        df_filtrado = df_filtrado[df_filtrado['SG_UF_PROVA'] == estado]
    if sexo != 'todos':
        df_filtrado = df_filtrado[df_filtrado['TP_SEXO'] == sexo]
    if raca != 'todas':
        df_filtrado = df_filtrado[df_filtrado['TP_COR_RACA'] == raca]
    if desempenho != 'todos':
        df_filtrado = df_filtrado[df_filtrado['DESEMPENHO'] == desempenho]

    if len(df_filtrado) == 0:
        fig_vazio = go.Figure().add_annotation(
            text="Nenhum dado disponível para este filtro",
            xref="paper", yref="paper", x=0.5, y=0.5,
            showarrow=False, font=dict(size=16, color="#64748b")
        )
        fig_vazio = estilizar_grafico(fig_vazio)
        return [fig_vazio] * 10

    # ── Gráfico 1: Média por tipo de escola (barras — mesmo do notebook) ──
    media_escola = df_filtrado.groupby('TP_ESCOLA')['MEDIA_GERAL'].mean().reset_index()
    fig1 = px.bar(
        media_escola,
        x='TP_ESCOLA',
        y='MEDIA_GERAL',
        text='MEDIA_GERAL',
        title='Média Geral por Tipo de Escola',
        labels={'TP_ESCOLA': 'Tipo de Escola', 'MEDIA_GERAL': 'Média Geral'},
        color='TP_ESCOLA',
        color_discrete_sequence=['#93c5fd', '#578ee7', '#1e3a8a']
    )
    fig1.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig1.update_layout(showlegend=False)
    fig1 = estilizar_grafico(fig1)

    # ── Gráfico 2: Distribuição notas da redação (histograma — mesmo do notebook) ──
    fig2 = px.histogram(
        df_filtrado,
        x='NU_NOTA_REDACAO',
        nbins=20,
        title='Distribuição das Notas da Redação',
        labels={'NU_NOTA_REDACAO': 'Nota da Redação', 'count': 'Quantidade de Participantes'},
        color_discrete_sequence=['#578ee7']
    )
    fig2.update_traces(marker_line_color='white', marker_line_width=0.5, opacity=0.85)
    fig2.update_layout(xaxis_range=[0, 1000], bargap=0.05)
    fig2 = estilizar_grafico(fig2)

    # ── Gráfico 3: Renda x Média (boxplot — mesmo do notebook) ──
    ordem_renda = [
        'Nenhuma Renda', 'Até R$ 1.320', 'R$ 1.320 - 1.980', 'R$ 1.980 - 2.640',
        'R$ 2.640 - 3.300', 'R$ 3.300 - 3.960', 'R$ 3.960 - 5.280', 'R$ 5.280 - 6.600',
        'R$ 6.600 - 7.920', 'R$ 7.920 - 9.240', 'R$ 9.240 - 10.560', 'R$ 10.560 - 11.880',
        'R$ 11.880 - 13.200', 'R$ 13.200 - 15.840', 'R$ 15.840 - 19.800',
        'R$ 19.800 - 26.400', 'Acima de R$ 26.400'
    ]
    rendas_presentes = [r for r in ordem_renda if r in df_filtrado['Q006'].values]

    fig3 = px.box(
        df_filtrado[df_filtrado['Q006'].isin(rendas_presentes)],
        x='Q006',
        y='MEDIA_GERAL',
        category_orders={'Q006': rendas_presentes},
        title='Renda Familiar × Média Geral',
        labels={'Q006': 'Faixa de Renda', 'MEDIA_GERAL': 'Média Geral'},
        color_discrete_sequence=['#578ee7']
    )
    fig3.update_traces(showlegend=False)
    fig3.update_layout(xaxis_tickangle=-45)
    fig3 = estilizar_grafico(fig3)

    # ── Gráfico 4: Correlação entre notas (heatmap — mesmo do notebook) ──
    corr_df = df_filtrado[[
        'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO'
    ]].rename(columns={
        'NU_NOTA_CN': 'Ciências da Natureza',
        'NU_NOTA_CH': 'Ciências Humanas',
        'NU_NOTA_LC': 'Linguagens',
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_REDACAO': 'Redação'
    }).corr()

    fig4 = px.imshow(
        corr_df,
        text_auto='.2f',
        color_continuous_scale='Blues',
        title='Correlação entre as Notas',
        zmin=0, zmax=1
    )
    fig4.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
    fig4 = estilizar_grafico(fig4)

    # ── Gráfico 5: Média por faixa etária (barras — mesmo do notebook) ──
    ordem_idades = [
        'Menor de 17', '17 anos', '18 anos', '19 anos', '20 anos', '21 anos',
        '22 anos', '23 anos', '24 anos', '25 anos', '26-30 anos', '31-35 anos',
        '36-40 anos', '41-45 anos', '46-50 anos', '51-55 anos', '56-60 anos',
        '61-65 anos', '66-70 anos', 'Maior de 70'
    ]
    media_idade = df_filtrado.groupby('TP_FAIXA_ETARIA')['MEDIA_GERAL'].mean().reset_index()
    idades_presentes = [i for i in ordem_idades if i in media_idade['TP_FAIXA_ETARIA'].values]

    fig5 = px.bar(
        media_idade,
        x='TP_FAIXA_ETARIA',
        y='MEDIA_GERAL',
        title='Média Geral por Faixa Etária',
        labels={'TP_FAIXA_ETARIA': 'Faixa Etária', 'MEDIA_GERAL': 'Média Geral'},
        category_orders={'TP_FAIXA_ETARIA': idades_presentes},
        color_discrete_sequence=['#578ee7']
    )
    fig5.update_layout(xaxis_tickangle=-45)
    fig5 = estilizar_grafico(fig5)

    # ── Gráfico 6: Box plot distribuição de notas por disciplina ──
    df_notas_melted = df_filtrado[
        ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT']
    ].rename(columns={
        'NU_NOTA_CN': 'Ciências da Natureza',
        'NU_NOTA_CH': 'Ciências Humanas',
        'NU_NOTA_LC': 'Linguagens',
        'NU_NOTA_MT': 'Matemática'
    }).melt(var_name='Disciplina', value_name='Nota').dropna()

    fig6 = px.box(
        df_notas_melted,
        x='Disciplina',
        y='Nota',
        title='Distribuição de Notas por Disciplina',
        color='Disciplina',
        color_discrete_sequence=['#1e3a8a', '#2563eb', '#578ee7', '#93c5fd']
    )
    fig6 = estilizar_grafico(fig6)
    fig6.update_layout(showlegend=False, xaxis_title='Disciplina', yaxis_title='Nota')

    # ── Gráfico 7: Pizza de desempenho ──
    dist_desempenho = df_filtrado['DESEMPENHO'].value_counts().reset_index()
    dist_desempenho.columns = ['DESEMPENHO', 'count']
    dist_desempenho['pct'] = (dist_desempenho['count'] / dist_desempenho['count'].sum() * 100).round(1)

    fig7 = px.pie(
        dist_desempenho,
        values='count',
        names='DESEMPENHO',
        title='Distribuição de Desempenho',
        color='DESEMPENHO',
        color_discrete_map={'Alto': '#1e3a8a', 'Médio': '#578ee7', 'Baixo': '#93c5fd'}
    )
    fig7.update_traces(
        texttemplate='<b>%{label}</b><br>%{customdata:.1f}%',
        textposition='inside',
        customdata=dist_desempenho['pct']
    )
    fig7 = estilizar_grafico(fig7)

    # ── Gráfico 8: Média por sexo ──
    desempenho_sexo = df_filtrado.groupby('TP_SEXO')['MEDIA_GERAL'].agg(['mean', 'count']).reset_index()
    desempenho_sexo = desempenho_sexo[desempenho_sexo['count'] > 0].sort_values('mean', ascending=False)

    fig8 = px.bar(
        desempenho_sexo,
        x='TP_SEXO',
        y='mean',
        text='mean',
        title='Desempenho Médio por Sexo',
        labels={'TP_SEXO': 'Sexo', 'mean': 'Média Geral'},
        color_discrete_sequence=['#578ee7']
    )
    fig8.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig8 = estilizar_grafico(fig8)

    # ── Gráfico 9: Média por cor/raça ──
    desempenho_raca = df_filtrado.groupby('TP_COR_RACA')['MEDIA_GERAL'].agg(['mean', 'count']).reset_index()
    desempenho_raca = desempenho_raca[desempenho_raca['count'] > 0].sort_values('mean', ascending=False)

    fig9 = px.bar(
        desempenho_raca,
        x='TP_COR_RACA',
        y='mean',
        text='mean',
        title='Desempenho Médio por Cor/Raça',
        labels={'TP_COR_RACA': 'Cor/Raça', 'mean': 'Média Geral'},
        color_discrete_sequence=['#578ee7']
    )
    fig9.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig9.update_xaxes(tickangle=-45)
    fig9 = estilizar_grafico(fig9)

    # ── Gráfico 10: Comparação de médias por disciplina (linha) ──
    medias_disc = pd.DataFrame({
        'Disciplina': ['Ciências da Natureza', 'Ciências Humanas', 'Linguagens', 'Matemática'],
        'Média': [
            df_filtrado['NU_NOTA_CN'].mean(),
            df_filtrado['NU_NOTA_CH'].mean(),
            df_filtrado['NU_NOTA_LC'].mean(),
            df_filtrado['NU_NOTA_MT'].mean()
        ]
    })

    fig10 = px.line(
        medias_disc,
        x='Disciplina',
        y='Média',
        markers=True,
        title='Comparação de Médias Entre Disciplinas',
        color_discrete_sequence=['#06b6d4']
    )
    fig10.update_traces(marker=dict(size=10), text=medias_disc['Média'].round(1),
                        textposition='top center', mode='lines+markers+text',
                        texttemplate='%{text:.1f}')
    fig10 = estilizar_grafico(fig10)

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10



app.layout = html.Div([

    dcc.Location(id='url', refresh=False),

    dbc.Container([

        html.Div([
            html.H1("Dashboard ENEM 2023", className='titulo-principal'),
            html.P("Visão geral dos dados e principais indicadores", className='subtitulo'),
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