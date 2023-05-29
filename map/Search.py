from copy import deepcopy
import random
import networkx as nx

from InteligenciaArtificial.map.EuclidianDistance import EuclidianDistance
from InteligenciaArtificial.utils.Enums.HeuristicEnum import HeuristicEnum
from InteligenciaArtificial.utils.consts.SearchConsts import REAL_DISTANCE, TIME_TO_DESTINATION


class Search:
    _instance = None
    # this node is the initial and the last node
    _centralNode = 'Patron'
    distanceFile = './map/DistanciaReal.txt'

    def __init__(self, useHeuristic):

        self._graph = nx.read_edgelist(
            self.distanceFile,
            delimiter=",",
            data=[(REAL_DISTANCE, int), (TIME_TO_DESTINATION, int)],
            encoding='utf-8-sig'
        )
        self._openList = []
        self._openListFromNode = {}
        self._closedList = []
        self._closedListFromNode = {}
        self._goalsNodes = []
        self._solution = []
        self._heuristic = HeuristicEnum.ADMISSIBLE if useHeuristic is None else useHeuristic
        self._heuristicTime = 1 if self._heuristic is HeuristicEnum.ADMISSIBLE else 15
        self._currentGoalNode = None

    @classmethod
    def getInstance(cls, useHeuristic = None):
        if cls._instance is None:
            cls._instance = Search(useHeuristic)
        return cls._instance

    def addToOpenList(self, value):
        if type(value) is str:
            if value not in self._openList and value not in self._closedList:
                self._openList.append(value)
                return f"Node: {value} added to open list"

        if type(value) is list:
            print('lista')
            for node in value:
                if node not in self._openList and node not in self._closedList:
                    self._openList.append(node)
                    return "Nodes added to open list"

    def addToCloseList(self, node):
        self._closedList.append(node)

    def removeFromOpenList(self, node):
        try:
            self._openList.remove(node)
            return 'nó removido com sucesso'
        except:
            'Não é possivel remover'

    def setGoalsNodes(self, goalsNodes):
        self._goalsNodes.extend(goalsNodes)

    def clearGoalsNodes(self):
        self._goalsNodes.clear()

    def getGoalsNodes(self):
        return self._goalsNodes

    def getCurrentGoalNode(self):
        return self._currentGoalNode

    def addToSolution(self, node):
        self._solution.append(node)

    def getSolution(self):
        return self._solution

    def getAdjacentNodes(self, node):
        adjacentList = list(self._graph.neighbors(node))
        return adjacentList

    def getEdgeProperty(self, node1, node2, property):
        propertyValue = nx.path_weight(self._graph, [node1, node2], property)
        return propertyValue


    def heuristcFunction(self, node):
        distanceBetweenNodes = EuclidianDistance.getInstance().getDistanceBetweenStreets(node, self.getCurrentGoalNode())

        return distanceBetweenNodes * self._heuristicTime

    def closestGoalNode(self, currentNode):
        closeNodeDistance = EuclidianDistance.getInstance().getDistanceBetweenStreets(currentNode, self._goalsNodes[0])
        closeNode = self._goalsNodes[0]
        for node in self._goalsNodes:
            tempNode = EuclidianDistance.getInstance().getDistanceBetweenStreets(currentNode, node)
            if  tempNode < closeNodeDistance:
                closeNodeDistance = tempNode
                closeNode = node
        return closeNode



    def avaliationFunction(self, g, h):
        return g + h

    def cost(self, node1, node2):
        return self.getEdgeProperty(node1, node2, REAL_DISTANCE) * self.getEdgeProperty(node1, node2, TIME_TO_DESTINATION)


    def functionOfX(self, node, accumulatedCost):
        return self.avaliationFunction(accumulatedCost, self.heuristcFunction(node))

    def run(self):

        self._currentGoalNode = self.closestGoalNode(self._centralNode)

        accumulatedCost = {}
        accumulatedCost[self._centralNode] = 0
        print(f'Custo Inicial: {accumulatedCost}')

        # funciona como se fosse uma lista ligada, armazena qual nó é "pai" de qual
        previousNode = {}
        previousNode[self._centralNode] = self._centralNode  # o nó inicial não tem nó anterior
        print(f'Previous Inicial: {previousNode}')



        self.addToOpenList(self._centralNode)  # inicial começa como aberto para algoritmo iniciar por ele

        while len(self._openList) > 0:
            currentNode = None

            for openNode in self._openList:
                if (currentNode is None or self.functionOfX(openNode, accumulatedCost[openNode])
                                        < self.functionOfX(currentNode, accumulatedCost[currentNode])):
                    currentNode = openNode

            if currentNode is None:
                break

            if currentNode == self._currentGoalNode:
                self.addToCloseList(currentNode)
                self.removeFromOpenList(currentNode)

                while previousNode[currentNode] != currentNode:
                    # lista solução
                    self.addToSolution(currentNode)
                    currentNode = previousNode[currentNode]

                print(self._solution)
                self.addToSolution(currentNode)
                self._solution.reverse()  # inverte a ordem, inicia pelo nó objetivo e vai até o inicial

                print("\n<-------------------------------------------------------------------------->\n")

                print(("lista final de fechados: "+str(self._closedList)))
                print("\nlista final de abertos: "+str(self._openList))

                print("\n<-------------------------------------------------------------------------->\n")

                print(f"SOLUTION: {self._solution}")
                return self._solution

            for adjacentNode in self.getAdjacentNodes(currentNode):
                if adjacentNode not in self._openList and adjacentNode not in self._closedList:
                    self.addToOpenList(adjacentNode)
                    previousNode[adjacentNode] = currentNode
                    accumulatedCost[adjacentNode] = accumulatedCost[currentNode] + self.cost(currentNode, adjacentNode)
                    # print(f'Previous de {adjacentNode} :{previousNode}')
                    # print(f'Acumulado de {adjacentNode} :{accumulatedCost}')
                else:
                    if accumulatedCost[adjacentNode] > accumulatedCost[currentNode] + self.cost(currentNode, adjacentNode):
                        accumulatedCost[adjacentNode] = accumulatedCost[currentNode] + self.cost(currentNode, adjacentNode)
                        previousNode[adjacentNode] = currentNode

                        if adjacentNode in self._closedList:
                            self._closedList.remove(adjacentNode)
                            self.addToOpenList(adjacentNode)

            self.addToCloseList(currentNode)
            self.removeFromOpenList(currentNode)

            print(("lista fechados: "+str(self._closedList)))
            print("lista abertos: "+str(self._openList))
        print('Solucao inexistente')
        return None


    def multiStageRun(self):
        pass


