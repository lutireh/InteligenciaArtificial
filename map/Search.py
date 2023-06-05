from copy import deepcopy
import random
import networkx as nx

from InteligenciaArtificial.map.EuclidianDistance import EuclidianDistance
from InteligenciaArtificial.utils.Enums.HeuristicEnum import HeuristicEnum
from InteligenciaArtificial.utils.consts.SearchConsts import REAL_DISTANCE, TIME_TO_DESTINATION


class Search:
    # instance for Singleton
    _instance = None
    # this node is the initial and the last node
    _centralNode = 'Patron'
    distanceFile = './map/DistanciaReal.txt'

    # constructor
    def __init__(self, useHeuristic):
        # reading and creating a graph from the distanceFile
        self._graph = nx.read_edgelist(
            self.distanceFile,
            delimiter=",",
            data=[(REAL_DISTANCE, int), (TIME_TO_DESTINATION, int)],
            encoding='utf-8-sig'
        )
        # initialing variables
        self._openList = []
        self._openListFromNode = {}
        self._closedList = []
        self._closedListFromNode = {}
        self._goalsNodes = []
        self._solution = []
        self._solutionOpenList = []
        self._solutionCloseList = []
        # setting heuristic
        self._heuristic = HeuristicEnum.ADMISSIBLE if useHeuristic is None else useHeuristic
        # setting the time based on the heuristic
        self._heuristicTime = 1 if self._heuristic is HeuristicEnum.ADMISSIBLE else 20
        self._currentGoalNode = None

    # Singleton
    @classmethod
    def getInstance(cls, useHeuristic=None):
        if cls._instance is None:
            cls._instance = Search(useHeuristic)
        return cls._instance

    # add on the open list nodes that wasn't visited
    def addToOpenList(self, value):
        if type(value) is str:
            if value not in self._openList and value not in self._closedList:
                self._openList.append(value)
                return f"Node: {value} added to open list"

    def addToCloseList(self, node):
        self._closedList.append(node)

    # TODO verificar como é usado
    def removeFromOpenList(self, node):
        try:
            self._openList.remove(node)
            return 'nó removido com sucesso'
        except:
            'Não é possivel remover'

    def setGoalsNodes(self, goalsNodes):
        self._goalsNodes.extend(goalsNodes)

    # TODO verificar se é usado
    def getGoalsNodes(self):
        return self._goalsNodes

    def clearGoalsNodes(self):
        self._goalsNodes.clear()

    def getGraph(self):
        return self._graph

    def getCurrentGoalNode(self):
        return self._currentGoalNode

    def addToSolution(self, node):
        self._solution.append(node)

    def getSolution(self):
        return self._solution

    def getAdjacentNodes(self, node):
        adjacentList = list(self._graph.neighbors(node))

        return adjacentList

    # return the value between two nodes depending on the property (realDistance or timeToDestination)
    def getEdgeProperty(self, node1, node2, property):
        propertyValue = nx.path_weight(self._graph, [node1, node2], property)
        return propertyValue

    def heuristcFunction(self, node):
        distanceBetweenNodes = 0

        if self._heuristic is HeuristicEnum.ADMISSIBLE:
            distanceBetweenNodes = EuclidianDistance.getInstance().getDistanceBetweenStreets(
            node,
            self.getCurrentGoalNode()
            )
        else:
            distanceBetweenNodes = EuclidianDistance.getInstance().getRealDistanceBetweenStreets(
                node,
                self.getCurrentGoalNode()
            )

        return distanceBetweenNodes * self._heuristicTime

    def closestGoalNode(self, currentNode):
        closeNodeDistance = EuclidianDistance.getInstance().getDistanceBetweenStreets(
            currentNode,
            self._goalsNodes[0]
        )
        closeGoalNode = self._goalsNodes[0]
        for node in self._goalsNodes:
            tempNode = EuclidianDistance.getInstance().getDistanceBetweenStreets(currentNode, node)
            if tempNode < closeNodeDistance:
                closeNodeDistance = tempNode
                closeGoalNode = node
        return closeGoalNode

    def avaliationFunction(self, node, accumulatedCost):
        return node + accumulatedCost

    def cost(self, node1, node2):
        cost = self.getEdgeProperty(node1, node2, REAL_DISTANCE) * self.getEdgeProperty(node1, node2, TIME_TO_DESTINATION)
        return cost

    # TODO verificar se da pra refatorar o A*
    def aStar(self, initialNode):

        self._currentGoalNode = self.closestGoalNode(initialNode)

        accumulatedCost = {}
        accumulatedCost[initialNode] = 0
        print(f'Custo Inicial: {accumulatedCost}')

        # funciona como se fosse uma lista ligada, armazena qual nó é "pai" de qual
        previousNode = {}
        previousNode[initialNode] = initialNode  # o nó inicial não tem nó anterior
        print(f'Previous Inicial: {previousNode}')

        self.addToOpenList(initialNode)  # inicial começa como aberto para algoritmo iniciar por ele

        while len(self._openList) > 0:
            currentNode = None

            for openNode in self._openList:

                if currentNode is not None:
                    print(f"Avaliaçao aberto:{openNode}: {self.avaliationFunction(self.heuristcFunction(openNode), accumulatedCost[openNode])}")
                    print(f"Avaliaçao corrente:{currentNode}: {self.avaliationFunction(self.heuristcFunction(currentNode), accumulatedCost[currentNode])}")

                if (currentNode is None or self.avaliationFunction(self.heuristcFunction(openNode), accumulatedCost[openNode])
                        < self.avaliationFunction(self.heuristcFunction(currentNode), accumulatedCost[currentNode])):
                    currentNode = openNode
                    print(f"CORRENTE NODE: {currentNode}")

            if currentNode is None:
                break

            if currentNode == self._currentGoalNode:
                self.addToCloseList(currentNode)
                self.removeFromOpenList(currentNode)

                while previousNode[currentNode] is not currentNode:
                    self.addToSolution(currentNode)
                    currentNode = previousNode[currentNode]

                self.addToSolution(currentNode)
                self._solution.reverse()

                print(f"Custo Acumulado: {accumulatedCost}")
                print(f"SOLUTION: {self._solution}")
                return self._solution

            for adjacentNode in self.getAdjacentNodes(currentNode):
                if adjacentNode not in self._openList and adjacentNode not in self._closedList:
                    self.addToOpenList(adjacentNode)
                    previousNode[adjacentNode] = currentNode
                    accumulatedCost[adjacentNode] = accumulatedCost[currentNode] + self.cost(currentNode, adjacentNode)
                else:
                    if accumulatedCost[adjacentNode] > accumulatedCost[currentNode] + self.cost(currentNode,
                                                                                                adjacentNode):
                        accumulatedCost[adjacentNode] = accumulatedCost[currentNode] + self.cost(currentNode,
                                                                                                 adjacentNode)
                        previousNode[adjacentNode] = currentNode

                        if adjacentNode in self._closedList:
                            self._closedList.remove(adjacentNode)
                            self.addToOpenList(adjacentNode)

            self.addToCloseList(currentNode)
            self.removeFromOpenList(currentNode)

        return None

    def run(self):
        multipleSolution = {}
        multipleOpen = {}
        multipleClose = {}
        goalsList = deepcopy(self._goalsNodes)
        nextInitial = "Patron"
        solution = []

        for goal in range(len(goalsList)):
            solution = self.aStar(nextInitial)
            currentGoal = self._currentGoalNode
            currentIteration = f"{nextInitial}->{currentGoal}"
            multipleSolution[currentIteration] = 'Solução inexistente' if solution is None else solution
            multipleOpen[currentIteration] = deepcopy(self._openList)
            multipleClose[currentIteration] = deepcopy(self._closedList)
            nextInitial = currentGoal
            self._goalsNodes.remove(currentGoal)
            self.clearNodes()

        self.setGoalsNodes(["Patron"])
        solution = self.aStar(nextInitial)
        multipleSolution[f"{nextInitial}->Patron"] = 'Solução inexistente' if solution is None else solution
        multipleOpen[f"{nextInitial}->Patron"] = deepcopy(self._openList)
        multipleClose[f"{nextInitial}->Patron"] = deepcopy(self._closedList)

        print(f"Soluções: {multipleSolution}")
        print(f"Listas Abertas: {multipleOpen}")
        print(f"Listas Fechadas: {multipleClose}")


    def clearNodes(self):
        self._openList = []
        self._openListFromNode = {}
        self._closedList = []
        self._closedListFromNode = {}
        self._solution = []
        self._solutionOpenList = []
        self._solutionCloseList = []

