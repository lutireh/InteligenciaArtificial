from copy import deepcopy
import networkx as nx

from InteligenciaArtificial.map.DbHandler import DbHandler
from InteligenciaArtificial.utils.Enums.HeuristicEnum import HeuristicEnum
from InteligenciaArtificial.utils.consts.SearchConsts import REAL_DISTANCE, TIME_TO_DESTINATION
from InteligenciaArtificial.utils.consts.DbConsts import *


class Search:
    # instance for Singleton
    _instance = None
    # this node is the initial and the last node
    _centralNode = 'Patron'
    distanceFile = './map/RealDistance.txt'
    debug = False

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
        self._closedList = []
        self._goalsNodes = []
        self._solution = []
        self._solutionOpenList = []
        self._solutionCloseList = []
        self._searchAccumulatedCost = {}
        self._currentGoalNode = None
        # setting heuristic
        self._heuristic = HeuristicEnum.ADMISSIBLE if useHeuristic is None else useHeuristic
        # setting the time based on the heuristic
        self._heuristicTime = 1 if self._heuristic is HeuristicEnum.ADMISSIBLE else 20

    # Singleton
    @classmethod
    def getInstance(cls, useHeuristic = None):
        if cls._instance is None:
            cls._instance = Search(useHeuristic)
        return cls._instance

    # add on the open list nodes that wasn't visited
    def addToOpenList(self, value):
        if value not in self._openList and value not in self._closedList:
            self._openList.append(value)

    # add on the close list and remove from the open list nodes that were visited
    def addToCloseList(self, node):
        try:
            self._openList.remove(node)
            self._closedList.append(node)
        except:
            print(f'ERROR: is not possible add to the close list the node: {node}')

    # remove from the close list if the node needs to be revisited
    def removeToCloseList(self, node):
        try:
            self._closedList.remove(node)
        except:
            print(f'ERROR: is not possible remove the node: {node}')

    # list of goals nodes
    def setGoalsNodes(self, goalsNodes):
        self._goalsNodes.extend(goalsNodes)

    # clear goals nodes for unitary tests
    def clearGoalsNodes(self):
        self._goalsNodes = []

    # get the next goal node
    def getCurrentGoalNode(self):
        return self._currentGoalNode

    # add the visited node to the solution
    def addToSolution(self, node):
        self._solution.append(node)

    # get the adjacent nodes of the node that is passed for the function (using neighbors from the lib networkx)
    def getAdjacentNodes(self, node):
        return list(self._graph.neighbors(node))

    # return the real distance or the time to destination between two nodes
    def getEdgeProperty(self, node1, node2, property):
        return nx.path_weight(self._graph, [node1, node2], property)

    # get the heuristic function for the admissible or the inadmissible heuristic
    # the heuristic is based in what as passed in the main class
    def heuristcFunction(self, node):
        if self._heuristic is HeuristicEnum.ADMISSIBLE:
            distanceBetweenNodes = DbHandler.getInstance().getDBColumns(node, self.getCurrentGoalNode(),
                                                                        DB_EUCLIDIAN_DISTANCE)
        else:
            distanceBetweenNodes = DbHandler.getInstance().getDBColumns(node, self.getCurrentGoalNode(),
                                                                        DB_REAL_DISTANCE)
        return distanceBetweenNodes * self._heuristicTime

    # search for the next goal node getting the closest for the current node
    def closestGoalNode(self, currentNode):
        closeNodeDistance = DbHandler.getInstance().getDBColumns(currentNode, self._goalsNodes[0],
                                                                 DB_EUCLIDIAN_DISTANCE)
        # get the first index of the array for an organized search and to get the name of the nodes
        closeGoalNode = self._goalsNodes[0]
        for node in self._goalsNodes:
            # for each node, get the euclidian distance for searching the closest
            auxNode = DbHandler.getInstance().getDBColumns(currentNode, node, DB_EUCLIDIAN_DISTANCE)
            if auxNode < closeNodeDistance:
                closeNodeDistance = auxNode
                closeGoalNode = node
        return closeGoalNode

    def avaliationFunction(self, heuristic, accumulatedCost):
        return heuristic + accumulatedCost

    def cost(self, node1, node2):
        realDistance = self.getEdgeProperty(node1, node2, REAL_DISTANCE)
        timeToDestination = self.getEdgeProperty(node1, node2, TIME_TO_DESTINATION)
        cost = realDistance * timeToDestination
        print(f"{node1}->{node2} | CUSTO: {cost}")
        return cost

    # runes the aStar for each goal
    def aStar(self, initialNode):
        # initialize the current goal node with the closest goal node from Patron - the initial node
        self._currentGoalNode = self.closestGoalNode(initialNode)
        print(f"======={initialNode}->{self._currentGoalNode}===========")
        # creating the dictionaries
        accumulatedCost = {}
        previousNode = {}
        # initializing the dictionary with Patron - the initial node and the cost of 0
        accumulatedCost[initialNode] = 0
        # initializing the dictionary with Patron
        # it doesn't have a previousNode so that is being initialized with Patron itself
        # has the behavior of a linked list
        previousNode[initialNode] = initialNode
        # initializing the open list with Patron
        self.addToOpenList(initialNode)

        while len(self._openList) > 0:
            currentNode = None

            for openNode in self._openList:
                # the first interaction is None so the current node receive the open node
                if (currentNode is None or
                        self.avaliationFunction(self.heuristcFunction(openNode), accumulatedCost[openNode])
                        < self.avaliationFunction(self.heuristcFunction(currentNode), accumulatedCost[currentNode])):
                    currentNode = openNode

            # after the first interaction, if the current node is None, the function break
            if currentNode is None:
                break

            if currentNode == self._currentGoalNode:
                self.addToCloseList(currentNode)
                # give the solution list
                while previousNode[currentNode] is not currentNode:
                    self.addToSolution(currentNode)
                    currentNode = previousNode[currentNode]
                self.addToSolution(currentNode)
                self._solution.reverse()

                print(f"Custo Acumulado: {accumulatedCost}")
                print(f"Solução: {self._solution}")
                self._searchAccumulatedCost = deepcopy(accumulatedCost)
                return self._solution

            for adjacentNode in self.getAdjacentNodes(currentNode):

                adjdacentNodeCost = accumulatedCost[currentNode] + self.cost(currentNode, adjacentNode)

                if (adjacentNode not in self._openList) and (adjacentNode not in self._closedList):
                    self.addToOpenList(adjacentNode)
                    previousNode[adjacentNode] = currentNode
                    accumulatedCost[adjacentNode] = adjdacentNodeCost
                else:
                    if adjdacentNodeCost < accumulatedCost[adjacentNode]:
                        accumulatedCost[adjacentNode] = adjdacentNodeCost
                        previousNode[adjacentNode] = currentNode
                        if adjacentNode in self._closedList:
                            self.removeToCloseList(adjacentNode)
                            self.addToOpenList(adjacentNode)

            self.addToCloseList(currentNode)

        return None

    def run(self):
        multipleSolution = {}
        multipleOpen = {}
        multipleClose = {}
        goalsList = deepcopy(self._goalsNodes)
        nextInitial = "Patron"
        nodeCosts = {}
        solution = []

        # runs aStar for each goal
        for goal in range(len(goalsList)):
            solution = self.aStar(nextInitial)
            currentGoal = self._currentGoalNode
            currentIteration = f"{nextInitial}->{currentGoal}"
            multipleSolution[currentIteration] = 'Solução inexistente' if solution is None else solution
            multipleOpen[currentIteration] = deepcopy(self._openList)
            multipleClose[currentIteration] = deepcopy(self._closedList)
            nodeCosts[currentIteration] = deepcopy(self._searchAccumulatedCost)
            nextInitial = currentGoal
            self._goalsNodes.remove(currentGoal)
            self.clearNodes()
        # runs again for getting back to Patron
        self.setGoalsNodes(["Patron"])
        solution = self.aStar(nextInitial)
        multipleSolution[f"{nextInitial}->Patron"] = 'Solução inexistente' if solution is None else solution
        multipleOpen[f"{nextInitial}->Patron"] = deepcopy(self._openList)
        multipleClose[f"{nextInitial}->Patron"] = deepcopy(self._closedList)
        nodeCosts[f"{nextInitial}->Patron"] = deepcopy(self._searchAccumulatedCost)
        # print the solutions
        print("\n\nMULTIPLOS OBJETIVOS SOLUÇÕES FINAIS:")
        print(f"Solução final: {multipleSolution}")
        print(f"Lista Aberta final: {multipleOpen}")
        print(f"Lista fechada final: {multipleClose}")
        print(f"Custo Acumulado final: {nodeCosts}")

        return multipleSolution

    def clearNodes(self):
        self._openList = []
        self._closedList = []
        self._solution = []
        self._solutionOpenList = []
        self._solutionCloseList = []
        self._searchAccumulatedCost = {}
