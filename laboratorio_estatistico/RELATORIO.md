# Relatório — Laboratório Estatístico Interativo

## 1. Identificação

- Grupo: **Gabriel**
- Integrantes e matrículas: **72650463**

## 2. Dataset escolhido e justificativa

Foi utilizado o dataset **Diamonds**, mantido no ecossistema ggplot2/tidyverse. Ele contém 53.940 registros e 10 variáveis, incluindo sete numéricas (`carat`, `depth`, `table`, `price`, `x`, `y`, `z`) e três categóricas (`cut`, `color`, `clarity`). O conjunto atende aos requisitos de volume e variedade de atributos e permite análises descritivas, simulações e relações lineares interessantes, especialmente entre características físicas e preço.

Fonte: https://ggplot2.tidyverse.org/reference/diamonds.html

Dados crus: https://github.com/tidyverse/ggplot2/blob/main/data-raw/diamonds.csv

## 3. Núcleo estatístico próprio

As medidas exibidas pela aplicação foram implementadas no arquivo `minhastats.py`.

### 3.1 Média

\[
\bar{x} = \frac{1}{n}\sum_{i=1}^{n}x_i
\]

### 3.2 Mediana

Os dados são ordenados. Para `n` ímpar, seleciona-se a posição central; para `n` par, calcula-se a média dos dois valores centrais.

### 3.3 Amplitude

\[
A = x_{max} - x_{min}
\]

### 3.4 Variância populacional

\[
\sigma^2 = \frac{\sum_{i=1}^{n}(x_i-\mu)^2}{n}
\]

### 3.5 Variância amostral

\[
s^2 = \frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}
\]

### 3.6 Desvio padrão

\[
s = \sqrt{s^2}
\]

### 3.7 Coeficiente de variação

\[
CV = \frac{s}{|\bar{x}|}\times100\%
\]

### 3.8 Covariância amostral

\[
cov(X,Y)=\frac{\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})}{n-1}
\]

### 3.9 Correlação de Pearson

\[
r=\frac{cov(X,Y)}{s_Xs_Y}
\]

### 3.10 Regressão linear simples

\[
\hat{Y}=\beta_0+\beta_1X
\]

\[
\beta_1=\frac{\sum (x_i-\bar{x})(y_i-\bar{y})}{\sum (x_i-\bar{x})^2}
\]

\[
\beta_0=\bar{y}-\beta_1\bar{x}
\]

O coeficiente de determinação é:

\[
R^2=1-\frac{\sum(y_i-\hat{y}_i)^2}{\sum(y_i-\bar{y})^2}
\]

## 4. Validação contra bibliotecas

O arquivo `tests/test_minhastats.py` compara os resultados das funções próprias com referências de NumPy e SciPy, usando tolerância numérica de `1e-9`.

**Resultado dos testes:** 12 testes executados com sucesso.

**Print dos testes:** ver captura de tela abaixo.

## 5. Módulo 2 — Estatística descritiva

A aplicação permite selecionar variáveis numéricas e categóricas. Para variáveis numéricas, apresenta tabela de frequências por classes, medidas de tendência central e dispersão, histograma, boxplot e outliers pela regra do IQR:

\[
IQR=Q_3-Q_1
\]

Limites para detecção de outliers:

\[
LI=Q_1-1,5\cdot IQR
\]

\[
LS=Q_3+1,5\cdot IQR
\]

**Print e interpretação:**  A variável `price` apresenta distribuição assimétrica à direita. 
A média dos preços é aproximadamente 3932,80, enquanto a mediana é 2401,00, 
indicando que valores elevados aumentam a média. O desvio padrão é aproximadamente 
3989,44, demonstrando alta dispersão dos preços. Pela regra do IQR, foram identificados 
3540 valores considerados outliers.

![Estatística descritiva - gráficos](images/images_testes_pytest.png)

![Estatística descritiva - gráficos](images/estatistica_descritiva_graficos.png)

![Estatística descritiva - medidas](images/estatistica_descritiva_medidas.png)

**Interpretação:** Foi observada forte correlação linear positiva entre `carat` e `price`, com coeficiente de Pearson de aproximadamente 0,9216. O valor de R² foi de aproximadamente 0,8493, indicando que cerca de 84,93% da variação observada no preço é explicada pelo modelo linear em função do peso em quilates. A inclinação positiva da reta mostra que, em média, o preço aumenta à medida que o valor de `carat` aumenta.

![Correlação e regressão](images/regressao.png)

## 6. Módulo 3 — Probabilidade e simulação

### Lei dos Grandes Números

Foram simulados lançamentos de uma moeda justa. À medida que o número de repetições cresce, a frequência relativa de caras tende ao valor teórico de 0,5.

### Teorema Central do Limite

A aplicação sorteia repetidamente amostras de uma variável numérica do dataset, calcula suas médias com a função própria e exibe a distribuição dessas médias. O usuário controla tamanho da amostra e número de repetições.

**Discussão:** A simulação mostra que, ao realizar várias amostragens e calcular suas médias, a distribuição das médias amostrais tende a assumir um formato aproximadamente normal conforme o tamanho da amostra aumenta, ilustrando o Teorema Central do Limite.

![Teorema Central do Limite](images/tcl.png)

## 7. Módulo 4 — Distribuições teóricas

A aplicação sobrepõe ao histograma a densidade Normal estimada usando a média e o desvio padrão calculados a partir dos dados. Para variáveis não negativas, também apresenta uma Exponencial como segunda candidata.

A comparação é visual e não deve ser interpretada como prova formal de aderência.

**Discussão do ajuste:** A sobreposição das curvas teóricas ao histograma permite comparar visualmente o comportamento dos dados com distribuições conhecidas. A análise apresentada é exploratória e visual, servindo para observar o grau de aproximação entre a distribuição empírica e os modelos teóricos, sem caracterizar um teste formal de aderência.

![Distribuições teóricas](images/distribuicoes.png)

## 8. Módulo 5 — Correlação e regressão linear

O usuário escolhe duas variáveis numéricas. A aplicação calcula a correlação de Pearson, a reta de regressão, o R² e permite realizar uma predição interativa.

**Exemplo recomendado:** usar `carat` como X e `price` como Y.

**Print, equação e interpretação:** 
**Equação da regressão:**

\[
\hat{Y} = -2256,3606 + 7756,4256X
\]

**Interpretação:** Foi observada forte correlação linear positiva entre `carat` e `price`, com coeficiente de Pearson de aproximadamente 0,9216. O valor de R² foi de aproximadamente 0,8493, indicando que cerca de 84,93% da variação observada no preço é explicada pelo modelo linear em função do peso em quilates. A inclinação positiva da reta mostra que, em média, o preço aumenta à medida que o valor de `carat` aumenta.

![Correlação e regressão](images/regressao.png)

> Correlação não implica causalidade.

## 9. Três descobertas estatísticas

A aplicação possui uma página que calcula automaticamente três destaques. Antes da entrega, executem o programa e tragam para este relatório os valores exibidos, explicando o significado deles.

1. Maior correlação linear em módulo:  `carat × x`, com r = 0,9751.
2. Variável com maior coeficiente de variação:  `price`, com CV = 101,44%.
3. Categoria mais frequente: em `cut`, a categoria `Ideal`, representando 39,95% dos registros.

Esses resultados indicam que o peso em quilates (`carat`) possui forte relação linear com a dimensão `x` do diamante. A variável `price` apresenta elevada dispersão relativa, mostrando grande heterogeneidade nos preços. Além disso, a categoria `Ideal` é a classificação de corte mais comum no conjunto de dados.

![Relatório de descobertas](images/descobertas.png)

## 10. Conclusão

O projeto permitiu transformar conceitos de estatística descritiva, probabilidade e regressão em código executável. A implementação manual tornou explícitas as fórmulas usadas nos cálculos, enquanto os testes contra bibliotecas consolidadas serviram para verificar a corretude numérica do núcleo estatístico.
