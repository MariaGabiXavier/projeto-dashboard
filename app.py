import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc

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
    .head(10)
    .reset_index()
)

fig_estado = px.bar(
    graf_estado,
    x='SG_UF_PROVA',
    y='MEDIA_GERAL',
    title='Top 10 Média por Estado'
)

graf_escola = (
    df.groupby('TP_ESCOLA')['MEDIA_GERAL']
    .mean()
    .reset_index()
)

fig_escola = px.bar(
    graf_escola,
    x='TP_ESCOLA',
    y='MEDIA_GERAL',
    title='Média por Tipo de Escola'
)

fig_redacao = px.histogram(
    df,
    x='NU_NOTA_REDACAO',
    nbins=20,
    title='Distribuição das Notas da Redação'
)

graf_idade = (
    df.groupby('TP_FAIXA_ETARIA')['MEDIA_GERAL']
    .mean()
    .reset_index()
)

fig_idade = px.bar(
    graf_idade,
    x='TP_FAIXA_ETARIA',
    y='MEDIA_GERAL',
    title='Média por Faixa Etária'
)

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

def criar_card(titulo, valor):

    return dbc.Card(

        dbc.CardBody([

            html.H5(
                titulo,
                className='card-titulo'
            ),

            html.H2(
                valor,
                className='card-valor'
            )

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
        )

    ]),

    html.Br(),

    dbc.Row([

        dbc.Col(
            criar_card(
                "Média Geral",
                media_geral
            ),
            width=3
        ),

        dbc.Col(
            criar_card(
                "Participantes",
                participantes
            ),
            width=3
        ),

        dbc.Col(
            criar_card(
                "Maior Média",
                maior_media
            ),
            width=3
        ),

        dbc.Col(
            criar_card(
                "Estado Destaque",
                estado_top
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
            dcc.Graph(figure=fig_estado),
            width=6
        ),

        dbc.Col(
            dcc.Graph(figure=fig_escola),
            width=6
        )

    ]),

    html.Br(),

    dbc.Row([

        dbc.Col(
            dcc.Graph(figure=fig_redacao),
            width=6
        ),

        dbc.Col(
            dcc.Graph(figure=fig_idade),
            width=6
        )

    ])

], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)