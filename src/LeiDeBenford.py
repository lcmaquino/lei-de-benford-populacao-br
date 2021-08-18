import pandas as pd
from numpy import log10
from scipy import stats

class LeiDeBenford:
    """
        Determina o "quão próximo" está da lei de Benford uma distribuição de
        frequência absoluta de um conjunto de dados.
    """
    _dado = None
    _coluna = ""
    _leiDeBenford = [(log10(d + 1) - log10(d)) for d in range(1, 10)]

    """
        Inicialização da classe.
    """
    def __init__(self, nomeDoArquivo, coluna, delimitador = ";", codificacao = "utf-8"):
        self._nomeDoArquivo = nomeDoArquivo
        self._coluna = coluna
        self._dado = pd.read_csv(nomeDoArquivo, delimiter = delimitador, encoding = codificacao)

    """
        Determina a frequência absoluta dos algarismos de 1 até 9 no primeiro
        dígito dos valores na amostra de dados.

        Retorno:
            frequenciaAbsoluta (list): lista com a frequência absoluta.
    """
    def frequenciaAbsoluta(self):
        frequenciaAbsoluta = []
        primeiroDigito = pd.DataFrame({
            self._coluna : self._dado[self._coluna].astype(str)
        })
        primeiroDigito[self._coluna] = primeiroDigito[self._coluna].apply(lambda valor: valor[0])
        for d in range(1, 10):
            frequenciaAbsoluta.append(len(primeiroDigito.loc[primeiroDigito[self._coluna] == str(d)]))

        return frequenciaAbsoluta

    """
        Determina o mínimo e o máximo da amostra de dados, bem como a ordem de
        grandeza entre a diferença dos mesmos.

        Retorno:
            minimo (int): menor valor dos dados.
            maximo (int): maior valor dos dados.
            odg (int): ordem de grandeza da diferença entre o máximo e o mínimo.
    """
    def ordemDeGradeza(self):
        minimo = self._dado[self._coluna].min()
        maximo = self._dado[self._coluna].max()
        diferenca = maximo - minimo
        odg = 0
        while(diferenca >= 10.0):
            diferenca /= 10.0
            odg += 1

        return (minimo, maximo, odg)

    """
        Gera o arquivo com o gráfico da frequência absoluta juntamente com a 
        curva da lei de Benford.

        Argumento:
            frequenciaAbsoluta (list): lista com a frequência absoluta dos
            dígitos de 1 até 9 na amostra de dados.
            nomeDoArquivo (str): caminho do arquivo.
            titulo (str): título do gráfico.
            cores (list): lista com os códigos hexadecimais das cores usadas
            no gráfico.
        Retorno:
            Nenhum retorno de variável. Gera o arquivo com o gráfico desejado.
    """
    def grafico(self, frequenciaAbsoluta, nomeDoArquivo, titulo, cores = ["#009c3b", "#002776"]):
        fqAbs = {
            "FREQUENCIA ABSOLUTA" : frequenciaAbsoluta
        }
        fqAbs["PRIMEIRO DIGITO"] = range(1, 10)
        totalDeMunicipios = sum(frequenciaAbsoluta)
        frequenciaEsperada = [totalDeMunicipios*self._leiDeBenford[i] for i in range(len(frequenciaAbsoluta))]
        fqAbs["LEI DE BENFORD"] = frequenciaEsperada
        fqAbs = pd.DataFrame(fqAbs)

        ax = fqAbs.plot(
            x = "PRIMEIRO DIGITO",
            y = "LEI DE BENFORD",
            xlabel = "PRIMEIRO DÍGITO",
            ylabel = "FREQUÊNCIA ABSOLUTA",
            title = titulo,
            rot = 0,
            marker = "o",
            color = cores[0],
            figsize = (10, 8),
            use_index = False
        )

        fqAbs.plot(
            x = "PRIMEIRO DIGITO",
            y = "FREQUENCIA ABSOLUTA",
            label = "PRIMEIRO DÍGITO",
            rot = 0,
            color = cores[1],
            kind = "bar",
            ax = ax
        )

        ax.figure.savefig(nomeDoArquivo)