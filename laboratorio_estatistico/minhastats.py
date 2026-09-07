"""Núcleo estatístico implementado manualmente para a Sistematização.

Regra do projeto: as medidas exibidas na aplicação vêm destas funções.
NumPy/SciPy são usados apenas nos testes de validação.
"""
from math import sqrt, exp, pi


def _clean(values):
    vals = [float(v) for v in values]
    if not vals:
        raise ValueError("A sequência não pode estar vazia.")
    return vals


def media(values):
    vals = _clean(values)
    return sum(vals) / len(vals)


def mediana(values):
    vals = sorted(_clean(values))
    n = len(vals)
    meio = n // 2
    if n % 2:
        return vals[meio]
    return (vals[meio - 1] + vals[meio]) / 2


def moda(values):
    vals = _clean(values)
    freq = {}
    for v in vals:
        freq[v] = freq.get(v, 0) + 1
    maior = max(freq.values())
    # Se todos aparecem uma única vez, não há moda estatística útil.
    if maior == 1:
        return []
    return sorted([v for v, f in freq.items() if f == maior])


def amplitude(values):
    vals = _clean(values)
    return max(vals) - min(vals)


def variancia(values, amostral=True):
    vals = _clean(values)
    n = len(vals)
    if amostral and n < 2:
        raise ValueError("Variância amostral exige ao menos 2 valores.")
    m = media(vals)
    soma = sum((v - m) ** 2 for v in vals)
    divisor = n - 1 if amostral else n
    return soma / divisor


def desvio_padrao(values, amostral=True):
    return sqrt(variancia(values, amostral=amostral))


def percentil(values, p):
    """Percentil com interpolação linear, compatível com numpy.percentile(method='linear')."""
    if not 0 <= p <= 100:
        raise ValueError("p deve estar entre 0 e 100.")
    vals = sorted(_clean(values))
    if len(vals) == 1:
        return vals[0]
    pos = (len(vals) - 1) * (p / 100)
    inferior = int(pos)
    superior = min(inferior + 1, len(vals) - 1)
    fracao = pos - inferior
    return vals[inferior] + fracao * (vals[superior] - vals[inferior])


def quartis(values):
    return {
        "Q1": percentil(values, 25),
        "Q2": percentil(values, 50),
        "Q3": percentil(values, 75),
    }


def coeficiente_variacao(values, amostral=True):
    m = media(values)
    if m == 0:
        raise ZeroDivisionError("Coeficiente de variação é indefinido para média zero.")
    return desvio_padrao(values, amostral=amostral) / abs(m) * 100


def covariancia(x, y, amostral=True):
    xs = _clean(x)
    ys = _clean(y)
    if len(xs) != len(ys):
        raise ValueError("x e y devem ter o mesmo tamanho.")
    n = len(xs)
    if amostral and n < 2:
        raise ValueError("Covariância amostral exige ao menos 2 pares.")
    mx, my = media(xs), media(ys)
    soma = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    divisor = n - 1 if amostral else n
    return soma / divisor


def correlacao_pearson(x, y):
    xs = _clean(x)
    ys = _clean(y)
    if len(xs) != len(ys):
        raise ValueError("x e y devem ter o mesmo tamanho.")
    sx = desvio_padrao(xs, amostral=True)
    sy = desvio_padrao(ys, amostral=True)
    if sx == 0 or sy == 0:
        raise ZeroDivisionError("Correlação é indefinida quando uma variável é constante.")
    return covariancia(xs, ys, amostral=True) / (sx * sy)


def regressao_linear(x, y):
    """Retorna beta0, beta1 e R² da regressão y = beta0 + beta1*x."""
    xs = _clean(x)
    ys = _clean(y)
    if len(xs) != len(ys):
        raise ValueError("x e y devem ter o mesmo tamanho.")
    if len(xs) < 2:
        raise ValueError("Regressão exige ao menos 2 pares.")
    mx, my = media(xs), media(ys)
    denom = sum((v - mx) ** 2 for v in xs)
    if denom == 0:
        raise ZeroDivisionError("Não é possível regressão quando X é constante.")
    beta1 = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / denom
    beta0 = my - beta1 * mx
    previstos = [beta0 + beta1 * a for a in xs]
    sse = sum((b - p) ** 2 for b, p in zip(ys, previstos))
    sst = sum((b - my) ** 2 for b in ys)
    r2 = 1.0 if sst == 0 and sse == 0 else 1 - sse / sst
    return beta0, beta1, r2


def pdf_normal(x, mu, sigma):
    if sigma <= 0:
        raise ValueError("sigma deve ser positivo.")
    return (1 / (sigma * sqrt(2 * pi))) * exp(-0.5 * ((x - mu) / sigma) ** 2)


def pdf_exponencial(x, lambd):
    if lambd <= 0:
        raise ValueError("lambda deve ser positivo.")
    if x < 0:
        return 0.0
    return lambd * exp(-lambd * x)
