import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff

df = pd.read_csv('dados/enem_transformado.csv')

df = df[df['MEDIA_GERAL'] > 0]

media_geral = round(df['MEDIA_GERAL'].mean(), 2)
maior_media = round(df['MEDIA_GERAL'].max(), 2)
menor_media = round(df['MEDIA_GERAL'].min(), 2)

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

df_escola = df[df['TP_ESCOLA'].isin(['Pública', 'Privada'])]

graf_escola = (
    df_escola.groupby('TP_ESCOLA')['MEDIA_GERAL']
    .mean()
    .reset_index()
)

fig_escola = px.bar(
    graf_escola,
    x='TP_ESCOLA',
    y='MEDIA_GERAL',
    color='TP_ESCOLA',
    color_discrete_map={
        'Pública': '#578ee7',
        'Privada': "#191b80"
    },
    title='Média por Tipo de Escola'
)

fig_escola.update_traces(
    marker_line_width=0
)

fig_escola.update_layout(
    xaxis_title='Tipo de Escola',
    yaxis_title='Média',
)

corr = df[
    [
        'NU_NOTA_CN',
        'NU_NOTA_CH',
        'NU_NOTA_LC',
        'NU_NOTA_MT',
        'NU_NOTA_REDACAO',
    ]
].rename(columns={
    'NU_NOTA_CN': 'Ciências da Natureza',
    'NU_NOTA_CH': 'Ciências Humanas',
    'NU_NOTA_LC': 'Linguagens',
    'NU_NOTA_MT': 'Matemática',
    'NU_NOTA_REDACAO': 'Redação',
}).corr()

fig_correlacao = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale='Blues',
    title='Correlação entre Notas'
)

fig_correlacao.update_layout(
    paper_bgcolor='#1e1e2f',
    plot_bgcolor='#1e1e2f',
    font_color='white',
    title_x=0.5
)

fig_redacao = ff.create_distplot(
    [df['NU_NOTA_REDACAO'].dropna()],
    ['Redação'],
    bin_size=50,
    show_hist=True,
    show_curve=True,
    show_rug=False
)

fig_redacao.update_traces(
    marker_color='skyblue'
)

fig_redacao.update_layout(
    title='Distribuição das Notas da Redação',
    xaxis_title='Nota da Redação',
    yaxis_title='Quantidade de Participantes',
    xaxis=dict(range=[0, 1000]),

    paper_bgcolor='#1e1e2f',
    plot_bgcolor='#1e1e2f',
    font_color='white',

    showlegend=False
)

fig_redacao.data[1].line.color = '#578ee7'

graf_renda = df.copy()

ordem_renda = [
    'Nenhuma Renda',
    'Até R$ 1.320',
    'R$ 1.320 - 1.980',
    'R$ 3.960 - 5.280',
    'R$ 7.920 - 9.240',
    'R$ 11.880 - 13.200',
    'R$ 19.800 - 26.400',
    'Acima de R$ 26.400'
]

renda_filtrada = graf_renda[
    graf_renda['Q006'].isin(ordem_renda)
]

fig_renda = px.box(
    renda_filtrada,
    x='Q006',
    y='MEDIA_GERAL',
    category_orders={'Q006': ordem_renda},
    points=False,
    title='Média por Renda Familiar'
)

fig_renda.update_traces(
    marker_color='steelblue'
)

fig_renda.update_layout(
    xaxis_title='Faixa de Renda',
    yaxis_title='Média',
    xaxis={'categoryorder':'array',
           'categoryarray': ordem_renda}
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
fig_escola = estilizar_grafico(fig_escola)
fig_correlacao = estilizar_grafico(fig_correlacao)
fig_redacao = estilizar_grafico(fig_redacao)
fig_renda = estilizar_grafico(fig_renda)

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

app.layout = dbc.Container([

    html.Div([

        html.H1(
            "Dashboard ENEM 2023",
            className='titulo-principal'
        ),

        html.P(
            "Visão geral dos dados e principais indicadores",
            className='subtitulo'
        ),

        html.Hr(className='linha-divisoria')

    ]),

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
                Os dados indicam diferenças relevantes de desempenho entre estados,
                tipo de escola e faixa etária. Observa-se maior média entre escolas privadas
                e variações significativas nas notas de redação.
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
                        figure=fig_renda,
                        config={'displayModeBar': False}
                    )
                ]),
                className='grafico-card'
            ),
            width=6
        ),

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(
                        figure=fig_escola,
                        config={'displayModeBar': False}
                    )
                ]),
                className='grafico-card'
            ),
            width=6
        )

    ]),

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

    ]),

    html.Br(),

    dbc.Row([

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(
                        figure=fig_correlacao,
                        config={'displayModeBar': False}
                    )
                ]),
                className='grafico-card'
            ),
            width=6
        ),

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(
                        figure=fig_redacao,
                        config={'displayModeBar': False}
                    )
                ]),
                className='grafico-card'
            ),
            width=6
        )

    ])

], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)