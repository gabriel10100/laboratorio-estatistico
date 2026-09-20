# Laboratório Estatístico Interativo

Projeto da disciplina **Matemática e Estatística para Computação**.

## Integrantes

> Preencher antes da entrega.

| Nome completo | Gabriel Melo França da Costa |
| Matrícula | 72650463 |

## Dataset

**Diamonds — ggplot2/tidyverse**

- 53.940 registros
- 10 variáveis
- Numéricas: `carat`, `depth`, `table`, `price`, `x`, `y`, `z`
- Categóricas: `cut`, `color`, `clarity`
- Documentação: https://ggplot2.tidyverse.org/reference/diamonds.html
- Dados crus: https://github.com/tidyverse/ggplot2/blob/main/data-raw/diamonds.csv

O arquivo usado pela aplicação está em `data/diamonds.csv`.

## O que foi implementado

- Módulo 0: apresentação e inspeção do dataset real.
- Módulo 1: núcleo estatístico próprio (`minhastats.py`).
- Módulo 2: estatística descritiva, frequências, histogramas, boxplots, IQR e interpretação de assimetria.
- Módulo 3: Monte Carlo para Lei dos Grandes Números e Teorema Central do Limite.
- Módulo 4: sobreposição de distribuições Normal e Exponencial estimadas a partir dos dados.
- Módulo 5: correlação de Pearson, regressão linear por mínimos quadrados, R² e predição.
- Módulo 6: três descobertas estatísticas geradas a partir do dataset.

## Regra do núcleo estatístico

As principais medidas estatísticas mostradas ao usuário são calculadas por funções próprias, sem NumPy/SciPy:

- média
- mediana
- moda
- amplitude
- variância amostral e populacional
- desvio padrão amostral e populacional
- quartis e percentis
- coeficiente de variação
- covariância
- correlação de Pearson
- regressão linear simples e R²

NumPy e SciPy são usados nos **testes** para validar os resultados.

## Como executar

### 1. Criar ambiente virtual (opcional, recomendado)

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Rodar os testes

```bash
pytest -q
```

### 4. Executar a aplicação

```bash
streamlit run app.py
```

## Tolerância numérica dos testes

A tolerância padrão usada nas comparações é `1e-9`. Os testes comparam as funções próprias com NumPy/SciPy.

## Estrutura

```text
laboratorio_estatistico/
├── app.py
├── minhastats.py
├── requirements.txt
├── README.md
├── RELATORIO.md
├── RESUMO_EXECUTIVO.md
├── ROTEIRO_VIDEO.md
├── data/
│   └── diamonds.csv
└── tests/
    └── test_minhastats.py
```

## Versionamento

O histórico de commits deve refletir o desenvolvimento real. Não deixem tudo para um único commit final. Em grupo, cada integrante deve fazer contribuições próprias.

Sugestão de divisão de commits:

1. estrutura e dataset;
2. média/mediana/moda/amplitude;
3. variância/desvio/quartis;
4. covariância/correlação/regressão;
5. testes;
6. interface descritiva;
7. simulações;
8. distribuições;
9. regressão/predição;
10. documentação e ajustes finais.

## Capturas de tela

### Estatística descritiva
![Estatística descritiva](images/estatistica_descritiva_graficos.png)

### Probabilidade e simulação
![Lei dos Grandes Números](images/lgn.png)

![Teorema Central do Limite - parte 1](images/tcl_parte1.png)

![Teorema Central do Limite - parte 2](images/tcl_parte2.png)

### Distribuições teóricas
![Distribuições teóricas](images/distribuicoes.png)

### Correlação e regressão
![Regressão linear](images/regressao.png)

### Descobertas
![Descobertas](images/descobertas.png)