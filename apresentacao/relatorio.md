# Roteiro de apresentação

## 1. Abertura

Este projeto realiza um diagnóstico aprofundado sobre os resultados do ENEM 2023, investigando como fatores socioeconômicos, geográficos e a infraestrutura escolar moldam as notas finais dos participantes. O objetivo central é responder: de que forma a desigualdade de renda e o tipo de administração escolar impactam o desempenho real dos estudantes nas quatro áreas do conhecimento e na redação?

## 2. Fonte dos dados

O projeto conecta duas fontes oficiais de dados públicos disponibilizadas pelo INEP:

- `enem_tratado.csv`: Amostra estruturada contendo dados de inscrição, localização do candidato, perfil sociodemográfico (sexo, idade, raça), tipo de escola, questionário socioeconômico (renda familiar) e as notas detalhadas das provas objetivas e de redação.
- `ITENS_PROVA_2023.csv`: Matriz técnica com as especificações das questões, gabaritos e os parâmetros analíticos da Teoria de Resposta ao Item (TRI), com destaque para o **Parâmetro B (Dificuldade do Item)**.

O volume de dados processado atende com folga aos critérios de grande escala, permitindo análises estatísticas robustas sobre o comportamento de centenas de milhares de candidatos presentes no exame.

Como diferencial técnico de enriquecimento de dados, o pipeline não olha apenas para as notas brutas: ele calcula a dificuldade média real enfrentada por cada candidato nas provas objetivas através do cruzamento com a matriz de itens do INEP.

## 3. Pipeline de dados

O pipeline foi construído utilizando a biblioteca Pandas em Python e seguiu etapas rigorosas de engenharia e tratamento de dados:

1. **Leitura Otimizada:** Carregamento do arquivo `enem_tratado.csv` utilizando delimitador de vírgula (`,`), com a codificação explicitamente configurada como `encoding='latin-1'`.
2. **Cálculo da Dificuldade das Provas:** A partir do arquivo de itens da prova (lido com separador `;`), extraiu-se a média do Parâmetro B (`NU_PARAM_B`) agrupada por área do conhecimento (`SG_AREA`). Esses valores foram convertidos em um dicionário técnico e injetados de forma cruzada de voltar no DataFrame principal, criando 4 novas colunas métricas: `DIF_MT`, `DIF_CN`, `DIF_CH` e `DIF_LC`.
3. **Limpeza de Registros Nulos:** Aplicação de filtros para remover registros inválidos onde as notas das quatro disciplinas objetivas estivessem ausentes de forma simultânea, garantindo que a análise refletisse o desempenho de candidatos que efetivamente realizaram as avaliações.
4. **Tratamento de Anomalias de Texto (Encoding):** Identificação de que a coluna de municípios apresentava problemas na exibição de caracteres especiais decorrentes da origem dos dados. Isso foi corrigido de forma cirúrgica na linha de código que converte e redecodifica o texto: `df_final['NO_MUNICIPIO_PROVA'].str.encode('latin-1').str.decode('utf-8', errors='ignore')`.
5. **Mapeamento e Categorização Descritiva:** Substituição de códigos numéricos e caracteres brutos por categorias textuais limpas e legíveis por meio de estruturas de dicionários pré-definidos:
   - `dic_idade`: Faixas etárias mapeadas de anos exatos para descrições textuais.
   - `dic_raca`: Tradução dos códigos de cor/raça (Branca, Preta, Parda, Amarela, Indígena).
   - `dic_escola` e `dic_adm`: Classificação do tipo de estabelecimento (Pública, Privada) e sua dependência administrativa.
   - `dic_presenca`: Conversão dos status de presença nos dias de aplicação.
   - `dic_renda`: Conversão das letras do questionário socioeconômico (Q006) para faixas reais de valores em Reais (R$).
6. **Engenharia de Recursos:** Criação da coluna calculada `Média Geral`, obtida através da média aritmética simples das notas de Matemática, Ciências da Natureza, Ciências Humanas, Linguagens e Redação.

## 4. Dashboard 1 - Visão geral

O primeiro dashboard, estruturado no arquivo de visualização (`app.py`), serve como o painel executivo e estratégico do projeto. Ele consolida os indicadores macro para apresentar o cenário educacional do país de forma direta:

- Exibe os grandes KPIs do exame, incluindo o volume de candidatos analisados e a média geral calculada nacional.
- Apresenta gráficos de barras horizontais e mapas coropléticos ordenando e distribuindo a performance média geral de cada Unidade da Federação (UF), destacando as discrepâncias de desempenho entre diferentes estados e regiões.
- Traz gráficos consolidados que avaliam o comportamento das médias de desempenho conforme as faixas de idade e recortes gerais de dependência escolar.

## 5. Dashboard 2 - Exploração interativa

O segundo ambiente do dashboard é voltado para a análise granular e cruzamento dinâmico de variáveis pelos usuários. Ele implementa controles interativos que atualizam os gráficos dinamicamente:

- **Filtros Personalizados:** Usuários conseguem segmentar toda a base de dados por Idioma escolhido na prova de Linguagens (Inglês ou Espanhol), Sexo, Cor/Raça e Categoria Administrativa da Escola.
- **Análise de Correlação:** Uma matriz de correlação interativa que demonstra a força do relacionamento estatístico entre as disciplinas (por exemplo, revelando como candidatos que performam bem em exatas se comportam nas disciplinas de humanas).
- **Gráficos de Distribuição e Dispersão:** Histogramas de densidade das notas combinados com diagramas de *Boxplot* interativos, ideais para visualizar a dispersão, a mediana e os limites de variação das notas de acordo com os degraus de renda familiar (variável socioeconômica).

## 6. Insights para destacar

- **O Abismo da Natureza Escolar:** Estudantes pertencentes à rede privada de ensino registraram uma média geral consolidada de **616,1 pontos**, ao passo que os alunos da rede pública mantiveram uma média de **515,8 pontos**. Esse intervalo numérico representa uma vantagem de aproximadamente 19,4% para a rede privada, escancarando a disparidade estrutural do sistema de ensino.
- **Predominância dos Estados do Sul e Sudeste:** A distribuição regional revela uma forte concentração de médias altas no topo do ranking federativo. O estado de **Minas Gerais (MG)** liderou nacionalmente com uma média geral de **565,14 pontos**, seguido de forma extremamente competitiva pelo estado de **São Paulo (SP)** com **564,92 pontos**.
- **Desigualdade de Renda Linear Perfeita:** A análise estatística de distribuição por Boxplot comprovou que a nota média geral avança de forma rigorosamente linear a cada incremento nas faixas de renda familiar do questionário socioeconômico (Q006). A faixa correspondente à classe alta (rendas acima de R$ 26.400) apresenta caixas de pontuação totalmente deslocadas para o topo e com incidência quase nula de notas abaixo da linha de corte básica.
- **O Fator Redação:** A nota da redação apresentou-se como a variável de maior volatilidade e desvio padrão dentro do conjunto total de notas. Ela atua diretamente como o grande divisor de águas que projeta os candidatos das faixas medianas de pontuação para o patamar de excelência (notas acima de 700 pontos).
- **Sinergia nas Ciências Exatas:** A matriz de correlação indicou que a maior associação positiva entre disciplinas ocorre entre Matemática e Ciências da Natureza. Candidatos que apresentam raciocínio lógico bem estruturado na prova de exatas tendem a replicar o alto aproveitamento nas questões biológicas e físicas.

## 7. Fechamento

A aplicação construída em `app.py` ultrapassa a mera exibição estática de dados: ela consolida uma narrativa visual e analítica que liga as condições sociais de partida do estudante ao seu resultado final no exame. Entender e mapear esses cruzamentos por meio de filtros interativos fornece a gestores públicos, pedagogos e analistas uma ferramenta baseada em evidências para apontar com precisão onde os investimentos e políticas corretivas de ensino devem ser priorizados.

# Relatório de insights - Dashboard ENEM 2023

## Fonte dos dados

- Amostra extraída dos Microdados Oficiais do ENEM 2023 (Base de dados do INEP).
- Matriz técnica complementar de Itens da Prova 2023 fornecida pelo órgão oficial.
- Processo de inteligência de dados focado no cálculo individualizado da dificuldade média (Parâmetro B da TRI) das disciplinas para enriquecimento analítico.

## Pipeline executado

1. **Leitura dos Microdados:** Carga da tabela `enem_tratado.csv` via Pandas usando separador `,` e parâmetro de `encoding='latin-1'`.
2. **Carga e Agregação de Itens:** Processamento da planilha de itens (`ITENS_PROVA_2023.csv`) para extrair a dificuldade média ponderada por código de área da prova.
3. **Integração Cruzada (Merge):** Associação dos valores médios calculados de dificuldade diretamente ao cadastro de candidatos através do mapeamento de dicionários de disciplinas.
4. **Tratamento de Nulos:** Filtragem e eliminação de registros com valores ausentes em lote nas notas das provas objetivas para preservar a integridade das estatísticas de presença real.
5. **Correção de Codificação de Texto:** Tratamento do erro na leitura de caracteres especiais e acentuações no campo geográfico através do método `.str.encode('latin-1').str.decode('utf-8', errors='ignore')` na coluna `NO_MUNICIPIO_PROVA`.
6. **Mapeamento de Categoriais:** Conversão em lote de variáveis codificadas de controle (Renda, Idade, Cor/Raça, Presença e Administração Escolar) em sequências de strings descritivas completas para alimentação direta das legendas dos gráficos.
7. **Geração da Média Geral:** Engenharia de atributo para calcular a nota média unificada dos participantes e salvamento do arquivo otimizado final para leitura direta pelo servidor do dashboard.

## Insights principais para a apresentação

- **Liderança Estatística por UF:** O ranking nacional de notas médias gerais é encabeçado por **Minas Gerais (MG) com 565,14** e **São Paulo (SP) com 564,92**.
- **Impacto da Infraestrutura Administrativa:** Estudantes de escolas **Privadas** atingiram performance média de **616,1 pontos**, contrastando fortemente com a média de **515,8 pontos** obtida por alunos de escolas **Públicas**.
- **Distribuição Sócio-Educação:** A concentração volumétrica aponta que a maior parcela de alunos provenientes de escolas públicas se situa em faixas intermediárias de nota (entre 450 e 650), enquanto o público de escolas particulares apresenta forte densidade na extremidade de alto rendimento (pontuações superiores a 650).
- **Fator de Opção de Idioma:** Candidatos que selecionaram a opção de língua estrangeira **Inglês** demonstraram pontuação média na prova de Linguagens substancialmente superior à média obtida pelos candidatos que optaram por **Espanhol**.
- **Gráfico de Tendência de Renda:** O mapeamento socioeconômico demonstrou de forma inequívoca que o desempenho acadêmico final dos candidatos é diretamente proporcional ao poder aquisitivo familiar, sem inflexões negativas ao longo de toda a curva ascendente das faixas de renda analisadas.