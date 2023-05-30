import unittest
import pandas as pd

from InteligenciaArtificial.map.EuclidianDistance import EuclidianDistance
from InteligenciaArtificial.map.Search import Search
from InteligenciaArtificial.utils.Enums.HeuristicEnum import HeuristicEnum
from InteligenciaArtificial.utils.consts.SearchConsts import REAL_DISTANCE, TIME_TO_DESTINATION


class EuclidianDistanceTest(unittest.TestCase):
    def setUp(self):
        EuclidianDistance.getInstance().initializeDb(pd.read_excel('../map/a_star.xlsx', sheet_name=None))
        Search.distanceFile = '../map/DistanciaReal.txt'
        Search.getInstance(HeuristicEnum.ADMISSIBLE)
        Search.getInstance().clearGoalsNodes()


    def testClosestGoalNodeByPatron(self):
        Search.getInstance().setGoalsNodes(["Rodoviaria", "LimeiraShopping", "FT"])
        result = Search.getInstance().closestGoalNode("Patron")
        self.assertEqual(result, "FT")

    def testClosestGoalNodeByFT(self):
        Search.getInstance().setGoalsNodes(["AvenidaSantaBarbara", "Estadio", "RuaPresidenteRoosevelt" , "RuaAugustoJorge" , "RuaPaschoalMarmo"])
        result = Search.getInstance().closestGoalNode("FT")
        self.assertEqual(result, "RuaPaschoalMarmo")

    def testGetAdjacentNodes(self):
        expectedNeighbors = ['RuaPaschoalMarmo', 'RodoviaLimeira-Piracicaba', 'RuaAntonioCruanesFilho', 'RuadaBoaMorte', 'RuaFranciscoDAndrea', 'RuaPresidenteRoosevelt', 'RuaBaraodeCampinas']
        adjacentNode = 'Patron'
        result = Search.getInstance().getAdjacentNodes(adjacentNode)
        self.assertEquals(result, expectedNeighbors)

    def testGetEdgeProperty(self):
        node1 = 'Patron'
        node2 = 'RuaPaschoalMarmo'
        expectedDistance = 850
        expectedTime = 3

        distanceResult = Search.getInstance().getEdgeProperty(node1, node2, REAL_DISTANCE)
        timeResult = Search.getInstance().getEdgeProperty(node1, node2, TIME_TO_DESTINATION)

        self.assertEqual(distanceResult, expectedDistance)
        self.assertEqual(timeResult, expectedTime)

    def testRunSingleObjective(self):
        Search.getInstance().setGoalsNodes(["Rodoviaria"])
        Search.getInstance().aStar("Patron")

    def testRunMultipleObjective(self):
        Search.getInstance().setGoalsNodes(["FT", "Rodoviaria"])
        Search.getInstance().run()

if __name__ == '__main__':
    unittest.main()