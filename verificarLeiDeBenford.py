#!/usr/bin/python3
import numpy as np
import pandas as pd
from src.LeiDeBenford import *

"""
    Ler arquivo com os dados da população no Brasil.

    Vide: https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html?edicao=28674&t=resultados
"""
arquivoDeDados = "data/estimativa-de-populacao-brasil-2020.csv"
coluna = "POPULACAO_ESTIMADA"
lb = LeiDeBenford(arquivoDeDados, coluna)

"""
    Determinar a frequência absoluta dos algarimos no primeiro dígito dos dados
    da população.
"""
print(f"[DÍGITO  |  FREQUÊNCIA ABSOLUTA  |  LEI DE BENFORD  |  ERRO (%)]")
frequenciaAbsoluta = lb.frequenciaAbsoluta()
totalDeMunicipios = sum(frequenciaAbsoluta)
leiDeBenford = [totalDeMunicipios*(np.log10(d + 1) - np.log10(d)) for d in range(1, 10)]
erroPercentual = [frequenciaAbsoluta[i]/leiDeBenford[i] - 1.0 for i in range(len(frequenciaAbsoluta))]
for i in range(9):
    print(f"{i + 1}     {frequenciaAbsoluta[i]}     {leiDeBenford[i]:5.2f}     {erroPercentual[i]:5.2f}")

print("")

"""
    Determinar a ordem de grandeza entre a diferença da população dos municípios
    com menor e maior habitantes.
"""
print(f"ORDEM DE GRANDEZA NOS DADOS")
minimo, maximo, ordemDeGrandeza = lb.ordemDeGradeza()
print(f"MENOR POPULÇÃO: \n{minimo}\n")
print(f"MAIOR POPULÇÃO: \n{maximo}\n")
print(f"ordemDeGrandeza(maximo - minimo) = 10^{ordemDeGrandeza}")
print("")

"""
    Salvar o arquivo do gráfico da frequência relativa junto com a curva
    da lei de Benford.
"""
arquivoGrafico = "data/teste-de-aderencia-populacao-br.png"
titulo = "FREQUÊNCIA ABSOLUTA DO PRIMEIRO DÍGITO"
print(f"SALVANDO O GRÁFICO: {arquivoGrafico}")
lb.grafico(frequenciaAbsoluta, arquivoGrafico, titulo)