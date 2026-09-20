# Resumo Executivo — Laboratório Estatístico Interativo

## Dataset

O projeto utiliza o dataset **Diamonds**, com 53.940 registros sobre preços e características físicas e qualitativas de diamantes. Ele contém sete variáveis numéricas e três categóricas.

## Solução

Foi construída uma aplicação interativa em Python/Streamlit dividida em sete módulos. O núcleo estatístico foi implementado manualmente em `minhastats.py`, incluindo média, mediana, moda, amplitude, variância, desvio padrão, quartis/percentis, coeficiente de variação, covariância, correlação de Pearson e regressão linear simples.

Os resultados das funções próprias são validados automaticamente contra NumPy/SciPy por meio de testes com `pytest`.

A aplicação inclui estatística descritiva, detecção de outliers pelo IQR, simulações de Monte Carlo da Lei dos Grandes Números e do Teorema Central do Limite, comparação visual com distribuições teóricas, correlação, regressão linear, R² e predição interativa.

## Três principais descobertas

1. A maior correlação linear em módulo foi entre `carat` e `x`, com r = 0,9751, indicando uma relação linear positiva muito forte entre o peso do diamante e sua dimensão x.

2. A variável `price` apresentou o maior coeficiente de variação, com CV = 101,44%, mostrando grande dispersão relativa dos preços.

3. Na variável categórica `cut`, a categoria mais frequente foi `Ideal`, representando 39,95% dos registros.

## Links finais

- Dataset original: https://github.com/tidyverse/ggplot2/blob/main/data-raw/diamonds.csv
- Repositório da solução: https://github.com/gabriel10100/laboratorio-estatistico
- Vídeo de demonstração: (https://youtu.be/UZOnp_o4bXU)
