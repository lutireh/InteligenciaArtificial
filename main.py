import pandas as pd
from pyvis.network import Network
import networkx as nx

from InteligenciaArtificial.map.EuclidianDistance import EuclidianDistance
from InteligenciaArtificial.map.Search import Search
from InteligenciaArtificial.utils.Enums.HeuristicEnum import HeuristicEnum

goalNodes = []
possibleNodes = []

print('Olá, insira a lista de nós objetivos abaixo, um de cada vez\nQuando não quiser mais inserir nós, basta dar enter com a linha em branco!')

with open('./map/possibleNodes.txt', 'r', encoding='utf-8') as file:

    lines = file.readlines()
    for line in lines:
        line = line.strip()
        possibleNodes.append(line)
    print(f'Os nós possíveis são: {possibleNodes}')

while True:
    node = input('Insira um nó objetivo: ')

    if not node:
        break

    if node not in possibleNodes:
        print('Nó objetivo inválido')
        continue

    if node not in goalNodes:
        goalNodes.append(node.strip())
    else:
        print('Nó objetivo já inserido')

print(f'Nós para buscar: {goalNodes}')

#   Primeira inicialização passamos a heurística que vamos utilizar


search = Search.getInstance(HeuristicEnum.ADMISSIBLE)
EuclidianDistance.getInstance().initializeDb(pd.read_excel('map/a_star.xlsx', sheet_name=None))
search.setGoalsNodes(goalNodes)
nt = Network('500px', '500px')
nt.from_nx(search.getGraph())
nt.show('nx.html')
search.run()
