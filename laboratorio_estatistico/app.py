from pathlib import Path
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

import minhastats as ms

st.set_page_config(page_title="Laboratório Estatístico", layout="wide")
BASE = Path(__file__).parent
DATASET = BASE / "data" / "diamonds.csv"


@st.cache_data
def carregar_dados():
    return pd.read_csv(DATASET)


def valores_validos(serie):
    return serie.dropna().astype(float).tolist()


def interpretar_assimetria(vals):
    m = ms.media(vals)
    med = ms.mediana(vals)
    dp = ms.desvio_padrao(vals)
    if dp == 0:
        return "Distribuição praticamente constante."
    indice = (m - med) / dp
    if abs(indice) < 0.10:
        return "Distribuição aproximadamente simétrica pela proximidade entre média e mediana."
    if indice > 0:
        return "Indício de assimetria à direita: a média está acima da mediana."
    return "Indício de assimetria à esquerda: a média está abaixo da mediana."


def tabela_frequencia_continua(vals, classes=10):
    contagens, limites = np.histogram(vals, bins=classes)
    total = len(vals)
    return pd.DataFrame({
        "Classe": [f"[{limites[i]:.2f}, {limites[i+1]:.2f}{']' if i == len(contagens)-1 else ')'}" for i in range(len(contagens))],
        "Frequência": contagens,
        "Frequência relativa (%)": [c / total * 100 for c in contagens],
    })


def pagina_dados(df):
    st.header("Módulo 0 — Dados reais")
    st.write("Dataset: **Diamonds (ggplot2)**, com preços e características de diamantes.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Registros", f"{len(df):,}".replace(",", "."))
    c2.metric("Variáveis numéricas", len(df.select_dtypes(include="number").columns))
    c3.metric("Variáveis categóricas", len(df.select_dtypes(exclude="number").columns))
    st.dataframe(df.head(100), use_container_width=True)
    st.write("Tipos de dados:")
    st.dataframe(pd.DataFrame({"coluna": df.columns, "tipo": [str(t) for t in df.dtypes]}), use_container_width=True)


def pagina_nucleo(df):
    st.header("Módulo 1 — Núcleo estatístico próprio")
    nums = df.select_dtypes(include="number").columns.tolist()
    col = st.selectbox("Variável para demonstrar os cálculos", nums, key="m1")
    vals = valores_validos(df[col])
    q = ms.quartis(vals)
    dados = {
        "Média": ms.media(vals),
        "Mediana": ms.mediana(vals),
        "Amplitude": ms.amplitude(vals),
        "Variância amostral": ms.variancia(vals, True),
        "Desvio padrão amostral": ms.desvio_padrao(vals, True),
        "Q1": q["Q1"],
        "Q2": q["Q2"],
        "Q3": q["Q3"],
        "Coeficiente de variação (%)": ms.coeficiente_variacao(vals, True),
    }
    st.dataframe(pd.DataFrame(dados.items(), columns=["Medida", "Valor"]), use_container_width=True)
    modos = ms.moda(vals)
    st.write("**Moda:**", modos[:10] if modos else "Sem moda")
    st.info("Os valores acima vêm de `minhastats.py`. NumPy/SciPy aparecem apenas nos testes automatizados.")


def pagina_descritiva(df):
    st.header("Módulo 2 — Estatística descritiva interativa")
    nums = df.select_dtypes(include="number").columns.tolist()
    cats = df.select_dtypes(exclude="number").columns.tolist()
    tipo = st.radio("Tipo de variável", ["Numérica", "Categórica"], horizontal=True)
    if tipo == "Numérica":
        col = st.selectbox("Variável", nums, key="m2n")
        vals = valores_validos(df[col])
        classes = st.slider("Número de classes", 5, 30, 12)
        st.dataframe(tabela_frequencia_continua(vals, classes), use_container_width=True)
        q = ms.quartis(vals)
        iqr = q["Q3"] - q["Q1"]
        li, ls = q["Q1"] - 1.5 * iqr, q["Q3"] + 1.5 * iqr
        outliers = [v for v in vals if v < li or v > ls]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Média", f"{ms.media(vals):.3f}")
        c2.metric("Mediana", f"{ms.mediana(vals):.3f}")
        c3.metric("Desvio padrão", f"{ms.desvio_padrao(vals):.3f}")
        c4.metric("Outliers (IQR)", len(outliers))
        st.write(interpretar_assimetria(vals))
        fig, ax = plt.subplots()
        ax.hist(vals, bins=classes)
        ax.set_title(f"Histograma — {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequência")
        st.pyplot(fig)
        plt.close(fig)
        fig, ax = plt.subplots()
        ax.boxplot(vals, vert=False)
        ax.set_title(f"Boxplot — {col}")
        ax.set_xlabel(col)
        st.pyplot(fig)
        plt.close(fig)
    else:
        col = st.selectbox("Variável", cats, key="m2c")
        freq = df[col].value_counts(dropna=False)
        tab = pd.DataFrame({"Categoria": freq.index.astype(str), "Frequência": freq.values, "Relativa (%)": freq.values / len(df) * 100})
        st.dataframe(tab, use_container_width=True)
        fig, ax = plt.subplots()
        ax.bar(tab["Categoria"], tab["Frequência"])
        ax.set_title(f"Frequências — {col}")
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig)
        plt.close(fig)


def pagina_simulacao(df):
    st.header("Módulo 3 — Probabilidade e simulação")
    aba1, aba2 = st.tabs(["Lei dos Grandes Números", "Teorema Central do Limite"])
    with aba1:
        n = st.slider("Lançamentos da moeda", 100, 20000, 5000, step=100)
        seed = st.number_input("Seed", value=42, step=1, key="seed_lgn")
        rng = random.Random(int(seed))
        acumulado, proporcoes = 0, []
        for i in range(1, n + 1):
            acumulado += rng.randint(0, 1)
            proporcoes.append(acumulado / i)
        fig, ax = plt.subplots()
        ax.plot(range(1, n + 1), proporcoes)
        ax.axhline(0.5, linestyle="--")
        ax.set_xlabel("Número de lançamentos")
        ax.set_ylabel("Frequência relativa de cara")
        ax.set_title("Lei dos Grandes Números")
        st.pyplot(fig)
        plt.close(fig)
        st.write(f"Frequência final observada: **{proporcoes[-1]:.4f}**; valor teórico: **0,5**.")
    with aba2:
        nums = df.select_dtypes(include="number").columns.tolist()
        col = st.selectbox("Variável do dataset", nums, key="tcl_col")
        tamanho = st.slider("Tamanho da amostra", 2, 300, 30)
        repeticoes = st.slider("Número de repetições", 100, 5000, 1000, step=100)
        seed = st.number_input("Seed", value=42, step=1, key="seed_tcl")
        rng = np.random.default_rng(int(seed))
        base = df[col].dropna().to_numpy()
        medias = []
        for _ in range(repeticoes):
            amostra = rng.choice(base, size=tamanho, replace=True)
            medias.append(ms.media(amostra.tolist()))
        fig, ax = plt.subplots()
        ax.hist(medias, bins=30)
        ax.set_title(f"Distribuição de médias amostrais — {col}")
        ax.set_xlabel("Média amostral")
        ax.set_ylabel("Frequência")
        st.pyplot(fig)
        plt.close(fig)
        st.write("Ao aumentar o tamanho da amostra, a distribuição das médias tende a se aproximar de uma forma Normal, conforme o TCL.")


def pagina_distribuicoes(df):
    st.header("Módulo 4 — Distribuições teóricas")
    nums = df.select_dtypes(include="number").columns.tolist()
    col = st.selectbox("Variável", nums, key="m4")
    vals = valores_validos(df[col])
    mu = ms.media(vals)
    sigma = ms.desvio_padrao(vals, amostral=False)
    minimo, maximo = min(vals), max(vals)
    eixo = np.linspace(minimo, maximo, 300)
    normal = [ms.pdf_normal(x, mu, sigma) for x in eixo]
    fig, ax = plt.subplots()
    ax.hist(vals, bins=40, density=True, alpha=0.5, label="Dados")
    ax.plot(eixo, normal, label="Normal estimada")
    if minimo >= 0 and mu > 0:
        lambd = 1 / mu
        expo = [ms.pdf_exponencial(x, lambd) for x in eixo]
        ax.plot(eixo, expo, label="Exponencial estimada")
    ax.set_title(f"Histograma e distribuições teóricas — {col}")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)
    st.write(f"Parâmetros estimados dos dados: média = **{mu:.4f}**, desvio padrão populacional = **{sigma:.4f}**.")
    st.caption("O ajuste aqui é uma comparação visual, como pedido na atividade; não é uma prova de aderência estatística.")


def pagina_regressao(df):
    st.header("Módulo 5 — Correlação e regressão linear")
    nums = df.select_dtypes(include="number").columns.tolist()
    xcol = st.selectbox("Variável X", nums, index=0, key="rx")
    opcoes_y = [c for c in nums if c != xcol]
    ycol = st.selectbox("Variável Y", opcoes_y, index=opcoes_y.index("price") if "price" in opcoes_y else 0, key="ry")
    pares = df[[xcol, ycol]].dropna()
    xs, ys = pares[xcol].astype(float).tolist(), pares[ycol].astype(float).tolist()
    corr = ms.correlacao_pearson(xs, ys)
    b0, b1, r2 = ms.regressao_linear(xs, ys)
    c1, c2, c3 = st.columns(3)
    c1.metric("Correlação de Pearson", f"{corr:.4f}")
    c2.metric("R²", f"{r2:.4f}")
    c3.metric("Inclinação β₁", f"{b1:.4f}")
    st.latex(rf"\hat{{Y}} = {b0:.4f} + ({b1:.4f})X")
    # Amostra visual para não desenhar 54 mil pontos quando desnecessário.
    visual = pares.sample(min(6000, len(pares)), random_state=42)
    eixo_x = np.linspace(pares[xcol].min(), pares[xcol].max(), 200)
    eixo_y = b0 + b1 * eixo_x
    fig, ax = plt.subplots()
    ax.scatter(visual[xcol], visual[ycol], s=8, alpha=0.35)
    ax.plot(eixo_x, eixo_y)
    ax.set_xlabel(xcol)
    ax.set_ylabel(ycol)
    ax.set_title(f"{ycol} em função de {xcol}")
    st.pyplot(fig)
    plt.close(fig)
    valor_x = st.number_input(f"Digite um valor de {xcol} para prever {ycol}", value=float(ms.mediana(xs)))
    previsao = b0 + b1 * valor_x
    st.success(f"Predição: **{previsao:.4f}**")
    st.write(f"Interpretação: mantendo o modelo linear, um aumento de 1 unidade em **{xcol}** está associado a uma variação média estimada de **{b1:.4f}** unidades em **{ycol}**.")
    st.warning("Correlação não implica causalidade.")


def pagina_descobertas(df):
    st.header("Módulo 6 — Relatório de descobertas")
    nums = df.select_dtypes(include="number").columns.tolist()
    pares = []
    for i, a in enumerate(nums):
        for b in nums[i+1:]:
            tmp = df[[a, b]].dropna()
            r = ms.correlacao_pearson(tmp[a].tolist(), tmp[b].tolist())
            pares.append((abs(r), r, a, b))
    pares.sort(reverse=True)
    _, r, a, b = pares[0]
    cvs = []
    for c in nums:
        vals = valores_validos(df[c])
        if ms.media(vals) != 0:
            cvs.append((ms.coeficiente_variacao(vals), c))
    cvs.sort(reverse=True)
    cv, cvcol = cvs[0]
    cats = df.select_dtypes(exclude="number").columns.tolist()
    cat = cats[0]
    mais_comum = df[cat].value_counts().idxmax()
    perc = df[cat].value_counts(normalize=True).max() * 100
    st.markdown(f"1. **Maior correlação linear em módulo:** `{a}` × `{b}`, com r = **{r:.4f}**.")
    st.markdown(f"2. **Maior variabilidade relativa:** `{cvcol}`, com coeficiente de variação de **{cv:.2f}%**.")
    st.markdown(f"3. **Categoria mais frequente em `{cat}`:** **{mais_comum}**, representando **{perc:.2f}%** dos registros.")
    st.caption("Estas descobertas são geradas automaticamente a partir do dataset; no relatório final, expliquem por que são relevantes.")


df = carregar_dados()
st.title("Laboratório Estatístico Interativo")
st.caption("Matemática e Estatística para Computação — núcleo matemático implementado manualmente")

pagina = st.sidebar.radio(
    "Navegação",
    [
        "0 — Dados reais",
        "1 — Núcleo estatístico",
        "2 — Estatística descritiva",
        "3 — Probabilidade e simulação",
        "4 — Distribuições teóricas",
        "5 — Correlação e regressão",
        "6 — Descobertas",
    ],
)

if pagina.startswith("0"):
    pagina_dados(df)
elif pagina.startswith("1"):
    pagina_nucleo(df)
elif pagina.startswith("2"):
    pagina_descritiva(df)
elif pagina.startswith("3"):
    pagina_simulacao(df)
elif pagina.startswith("4"):
    pagina_distribuicoes(df)
elif pagina.startswith("5"):
    pagina_regressao(df)
else:
    pagina_descobertas(df)
