import unittest
import pandas as pd

from InteligenciaArtificial.map.DbHandler import DbHandler
from InteligenciaArtificial.map.Search import Search
from InteligenciaArtificial.utils.Enums.HeuristicEnum import HeuristicEnum
from InteligenciaArtificial.utils.consts.SearchConsts import REAL_DISTANCE, TIME_TO_DESTINATION


class EuclidianDistanceTest(unittest.TestCase):
    def setUp(self):
        DbHandler.getInstance().initializeDb(pd.read_excel('../map/a_star.xlsx', sheet_name=[
            "Patron", "FT", "Rodoviaria", "Estadio", "EspaçoColibri", "ShoppingNacoesLimeira", "LimeiraShopping",
            "SupermercadoServBem", "RuadaBoaMorte", "AvenidaSantaBarbara", "RuaBahia", "RuaAntonioCruanesFilho",
            "RuaBaraodeCampinas", "AvenidaProfJoaquimdeMichieli", "RodoviaLimeira-Piracicaba", "RuaPaschoalMarmo",
            "AvenidaConegoManuelAlves", "RuaFranciscoDAndrea", "RuaPresidenteRoosevelt", "RuaAugustoJorge",
            "RodoviaAnhanguera"]))
        Search.distanceFile = '../map/RealDistance.txt'
        Search.getInstance(HeuristicEnum.INADMISSIBLE)
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
        Search.getInstance().run()

    def testRunMultipleObjective(self):
        admissibleReturn = {'Patron->FT': ['Patron', 'RuaPaschoalMarmo', 'FT'],
                            'FT->ShoppingNacoesLimeira': ['FT', 'RuaPaschoalMarmo', 'Patron',
                                                          'RodoviaLimeira-Piracicaba', 'ShoppingNacoesLimeira'],
                            'ShoppingNacoesLimeira->Estadio': ['ShoppingNacoesLimeira', 'RodoviaLimeira-Piracicaba',
                                                               'Patron', 'RuadaBoaMorte', 'Rodoviaria',
                                                               'RuaAugustoJorge', 'Estadio'],
                            'Estadio->LimeiraShopping': ['Estadio', 'RuaFranciscoDAndrea', 'LimeiraShopping'],
                            'LimeiraShopping->Patron': ['LimeiraShopping', 'RuaFranciscoDAndrea', 'Patron']}

        Search.getInstance().setGoalsNodes(['FT', 'Estadio', 'ShoppingNacoesLimeira', 'LimeiraShopping'])
        solution = Search.getInstance().run()
        self.assertEqual(len(solution), 5)
        self.assertNotEqual(solution, admissibleReturn)

if __name__ == '__main__':
    unittest.main()