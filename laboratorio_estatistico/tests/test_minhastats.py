import numpy as np
from scipy import stats
import minhastats as ms

TOL = 1e-9
DADOS = [2.0, 3.0, 3.0, 5.0, 8.0, 13.0]
X = [1, 2, 3, 4, 5, 6]
Y = [2, 4, 5, 4, 5, 7]


def test_media():
    assert abs(ms.media(DADOS) - np.mean(DADOS)) < TOL


def test_mediana():
    assert abs(ms.mediana(DADOS) - np.median(DADOS)) < TOL


def test_moda():
    esperado = float(stats.mode(DADOS, keepdims=False).mode)
    assert ms.moda(DADOS) == [esperado]


def test_amplitude():
    assert abs(ms.amplitude(DADOS) - (np.max(DADOS) - np.min(DADOS))) < TOL


def test_variancia_populacional():
    assert abs(ms.variancia(DADOS, amostral=False) - np.var(DADOS, ddof=0)) < TOL


def test_variancia_amostral():
    assert abs(ms.variancia(DADOS, amostral=True) - np.var(DADOS, ddof=1)) < TOL


def test_desvio_padrao():
    assert abs(ms.desvio_padrao(DADOS, amostral=True) - np.std(DADOS, ddof=1)) < TOL


def test_percentis_e_quartis():
    for p in [10, 25, 50, 75, 90]:
        assert abs(ms.percentil(DADOS, p) - np.percentile(DADOS, p, method="linear")) < TOL


def test_coeficiente_variacao():
    esperado = np.std(DADOS, ddof=1) / abs(np.mean(DADOS)) * 100
    assert abs(ms.coeficiente_variacao(DADOS) - esperado) < TOL


def test_covariancia():
    esperado = np.cov(X, Y, ddof=1)[0, 1]
    assert abs(ms.covariancia(X, Y) - esperado) < TOL


def test_correlacao():
    esperado = np.corrcoef(X, Y)[0, 1]
    assert abs(ms.correlacao_pearson(X, Y) - esperado) < TOL


def test_regressao_linear():
    beta1, beta0 = np.polyfit(X, Y, 1)
    b0, b1, r2 = ms.regressao_linear(X, Y)
    assert abs(b0 - beta0) < TOL
    assert abs(b1 - beta1) < TOL
    yhat = beta0 + beta1 * np.array(X)
    esperado_r2 = 1 - np.sum((np.array(Y) - yhat) ** 2) / np.sum((np.array(Y) - np.mean(Y)) ** 2)
    assert abs(r2 - esperado_r2) < TOL
