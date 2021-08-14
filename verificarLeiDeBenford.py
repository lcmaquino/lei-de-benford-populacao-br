#!/usr/bin/python3
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
    Determinar a ordem de grandeza entre a diferença da população dos municípios
    com menor e maior habitantes.
"""
print(f"ORDEM DE GRANDEZA NOS DADOS")
lb.ordemDeGradeza()
print("")

"""
    Determinar a frequência relativa dos algarimos no primeiro dígito dos dados
    da população.
"""
print(f"[DÍGITO  |  FREQUÊNCIA RELATIVA]")
frequenciaRelativa = lb.frequenciaRelativa()
for i in range(9):
    print(f"{i + 1}  {frequenciaRelativa[i]:5.2f}")

print("")

"""
    Aplicar o Teste de Aderência Qui-quadrado.
"""
print(f"TESTE DE ADERÊNCIA QUI-QUADRADO")
lb.testarAderencia(frequenciaRelativa)
print("")

"""
    Salvar o arquivo do gráfico da frequência relativa junto com a curva
    da lei de Benford.
"""
arquivoGrafico = "data/teste-de-aderencia-populacao-br.png"
titulo = "FREQUÊNCIA RELATIVA DO PRIMEIRO DÍGITO"
print(f"SALVANDO O GRÁFICO: {arquivoGrafico}")
lb.grafico(frequenciaRelativa, arquivoGrafico, titulo)