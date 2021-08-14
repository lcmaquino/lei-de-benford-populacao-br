import pandas as pd
from numpy import log10
from scipy import stats

class LeiDeBenford:
    """
        Determina o "quão próximo" está da lei de Benford uma distribuição de
        frequência relativa de um conjunto de dados.
    """
    _dado = None
    _coluna = ""
    _leiDeBenford = [100.0*(log10(d + 1) - log10(d)) for d in range(1, 10)]
    _frequenciaEsperada = []

    """
        Inicialização da classe.
    """
    def __init__(self, nomeDoArquivo, coluna, delimitador = ";", codificacao = "utf-8"):
        self._nomeDoArquivo = nomeDoArquivo
        self._coluna = coluna
        self._dado = pd.read_csv(nomeDoArquivo, delimiter = delimitador, encoding = codificacao)
        self._frequenciaEsperada = self._leiDeBenford[0:8]
        self._frequenciaEsperada += self._leiDeBenford[8]

    """
        Aplica o Teste de Aderência Qui-Quadrado em uma distribuição de frequência
        relativa.

        Argumentos:
            frequenciaRelativa (list): lista com a frequência relativa dos
            dígitos de 1 até 9 na amostra de dados.
            alfa (float): nível de confiança do teste.
            grauDeLiberdede: grau de liberdade do teste.

        Retorno:
            Imprime no terminal o resultado da aplicação do teste.
    """
    def testarAderencia(self, frequenciaRelativa, alfa = 0.05, grauDeLiberdade = 7):
        nivelDeConfianca = 1 - alfa
        qui2Critico = stats.chi2.ppf(nivelDeConfianca, grauDeLiberdade)
        print(f"(alfa = {alfa}, grauDeLiberdade = {grauDeLiberdade}, chi2Critico = {qui2Critico:5.2f})")
        frequenciaObservada = frequenciaRelativa[0:8]
        frequenciaObservada[7] += frequenciaRelativa[8]
        qui2, p = stats.chisquare(f_obs = frequenciaObservada, f_exp = self._frequenciaEsperada)
        print(f"qui2 = {qui2}, p = {p}")
        if(qui2 < qui2Critico):
            print(f"(qui2 < qui2Critico): Os dados seguem a distribuição da lei de Benford.")
        else:
            print(f"(qui2 >= qui2Critico): Os dados não seguem a distribuição da lei de Benford.")

    """
        Determina a frequência relativa dos dígitos de 1 até 9 na amostra de dados.

        Retorno:
            frequenciaRelativa (list): lista com a frequência relativa dos
            dígitos de 1 até 9 na amostra de dados.
    """
    def frequenciaRelativa(self):
        frequenciaRelativa = []
        totalDeMunicipios = len(self._dado)
        primeiroDigito = pd.DataFrame({
            self._coluna : self._dado[self._coluna].astype(str)
        })
        primeiroDigito[self._coluna] = primeiroDigito[self._coluna].apply(lambda valor: valor[0])
        for d in range(1, 10):
            frequenciaAbsoluta = len(primeiroDigito.loc[primeiroDigito[self._coluna] == str(d)])
            frequenciaRelativa.append(100.0*frequenciaAbsoluta/totalDeMunicipios)

        return frequenciaRelativa

    """
        Determina o mínimo e o máximo da amostra de dados, bem como a ordem de
        grandeza entre a diferença dos mesmos.

        Retorno:
            Imprime os valores de mínimo e máximo e da ordem de grandeza entre a
            diferença deles.
    """
    def ordemDeGradeza(self):
        minimo = self._dado[self._coluna].min()
        municipioMinimo = self._dado.loc[self._dado[self._coluna] == minimo]
        maximo = self._dado[self._coluna].max()
        municipioMaximo = self._dado.loc[self._dado[self._coluna] == maximo]
        print(f"MENOR POPULÇÃO\n{municipioMinimo}\n")
        print(f"MAIOR POPULÇÃO\n{municipioMaximo}\n")
        print(f"ordemDeGrandeza(maximo - minimo) = 10^{self.odg(maximo - minimo)}")

    """
        Determina a ordem de grandeza de um número real positivo.

        Argumento:
            valor (float): número real positivo.

        Retorno:
            ord (int): ordem de grandeza do valor desejado.
    """
    def odg(self, valor):
        ord = -1
        while(valor > 1.0):
            valor /= 10.0
            ord += 1

        return ord

    """
        Gera o arquivo com o gráfico da frequência relativa juntamente com a 
        curva da lei de Benford.

        Argumento:
            frequenciaRelativa (list): lista com a frequência relativa dos
            dígitos de 1 até 9 na amostra de dados.
            nomeDoArquivo (str): caminho do arquivo.
            titulo (str): título do gráfico.
            cores (list): lista com os códigos hexadecimais das cores usadas
            no gráfico.
        Retorno:
            Gera o arquivo com o gráfico desejado.
    """
    def grafico(self, frequenciaRelativa, nomeDoArquivo, titulo, cores = ["#009c3b", "#002776"]):
        frel = {
            "FREQUENCIA RELATIVA" : frequenciaRelativa
        }
        frel["PRIMEIRO DIGITO"] = range(1, 10)
        frel["LEI DE BENFORD"] = self._leiDeBenford
        frel = pd.DataFrame(frel)

        ax = frel.plot(
            x = "PRIMEIRO DIGITO",
            y = "LEI DE BENFORD",
            xlabel = "PRIMEIRO DÍGITO",
            ylabel = "FREQUÊNCIA RELATIVA (%)",
            title = titulo,
            rot = 0,
            marker = "o",
            color = cores[0],
            figsize = (10, 8),
            use_index = False
        )

        frel.plot(
            x = "PRIMEIRO DIGITO",
            y = "FREQUENCIA RELATIVA",
            label = "PRIMEIRO DÍGITO",
            rot = 0,
            color = cores[1],
            kind = "bar",
            ax = ax
        )

        ax.figure.savefig(nomeDoArquivo)