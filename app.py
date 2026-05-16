import pandas as pd
from dash import Dash, html
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
                Este dashboard apresenta uma visão geral do desempenho dos participantes do ENEM 2023.
                Os indicadores permitem identificar padrões gerais de desempenho,
                comportamento das notas e diferenças entre grupos analisados.
                """,
                className='texto-resumo'
            )

        ])

    ],
    className='card-resumo')

], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)