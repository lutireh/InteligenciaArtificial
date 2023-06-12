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
        Search.getInstance(HeuristicEnum.ADMISSIBLE)
        Search.getInstance().clearGoalsNodes()
        Search.getInstance().clearNodes()
        Search.debug = True


    def testClosestGoalNodeByPatron(self):
        expectedReturn = "FT"
        Search.getInstance().setGoalsNodes(["Rodoviaria", "LimeiraShopping", "FT"])
        result = Search.getInstance().closestGoalNode("Patron")
        self.assertEqual(expectedReturn, result)

    def testClosestGoalNodeByFT(self):
        expectedReturn = "RuaPaschoalMarmo"
        Search.getInstance().setGoalsNodes(["AvenidaSantaBarbara", "Estadio", "RuaPresidenteRoosevelt" , "RuaAugustoJorge" , "RuaPaschoalMarmo"])
        result = Search.getInstance().closestGoalNode("FT")
        self.assertEqual(expectedReturn, result)

    def testGetAdjacentNodes(self):
        expectedNeighbors = ['RuaPaschoalMarmo', 'RodoviaLimeira-Piracicaba', 'RuaAntonioCruanesFilho', 'RuadaBoaMorte', 'RuaFranciscoDAndrea', 'RuaPresidenteRoosevelt', 'RuaBaraodeCampinas']
        adjacentNode = 'Patron'
        result = Search.getInstance().getAdjacentNodes(adjacentNode)
        self.assertEqual(expectedNeighbors, result)

    def testGetEdgeProperty(self):
        node1 = 'Patron'
        node2 = 'RuaPaschoalMarmo'
        expectedDistance = 850
        expectedTime = 2

        distanceResult = Search.getInstance().getEdgeProperty(node1, node2, REAL_DISTANCE)
        timeResult = Search.getInstance().getEdgeProperty(node1, node2, TIME_TO_DESTINATION)

        self.assertEqual(expectedDistance, distanceResult)
        self.assertEqual(expectedTime, timeResult)

    def testRunSingleObjective(self):
        expectedSolution = {'Patron->Rodoviaria': ['Patron', 'RuadaBoaMorte', 'Rodoviaria'], 'Rodoviaria->Patron': ['Rodoviaria', 'RuadaBoaMorte', 'Patron']}
        expectedCost = 18400

        Search.getInstance().setGoalsNodes(["Rodoviaria"])

        solution = Search.getInstance().run()
        cost = Search.getInstance().finalCost

        self.assertDictEqual(expectedSolution, solution)
        self.assertEqual(expectedCost, cost)


    def testRunMultipleObjective(self):
        expectedSolution = {'Patron->Estadio': ['Patron', 'RuadaBoaMorte', 'Rodoviaria', 'RuaAugustoJorge', 'Estadio'], 'Estadio->ShoppingNacoesLimeira': ['Estadio', 'RuaAugustoJorge', 'Rodoviaria', 'RuadaBoaMorte', 'Patron', 'RodoviaLimeira-Piracicaba', 'ShoppingNacoesLimeira'], 'ShoppingNacoesLimeira->Patron': ['ShoppingNacoesLimeira', 'RodoviaLimeira-Piracicaba', 'Patron']}

        expectedLength = 3
        expectedCost = 146000

        Search.getInstance().setGoalsNodes(['Estadio', 'ShoppingNacoesLimeira'])
        solution = Search.getInstance().run()
        cost = Search.getInstance().finalCost

        self.assertEqual(expectedLength, len(solution))
        self.assertDictEqual(expectedSolution, solution)
        self.assertEqual(expectedCost, cost)

    def testRunAllObjective(self):
        expectedSolution = {'Patron->EspaçoColibri': ['Patron', 'RuadaBoaMorte', 'AvenidaSantaBarbara', 'EspaçoColibri'], 'EspaçoColibri->Rodoviaria': ['EspaçoColibri', 'AvenidaSantaBarbara', 'RuadaBoaMorte', 'Rodoviaria'], 'Rodoviaria->SupermercadoServBem': ['Rodoviaria', 'RuadaBoaMorte', 'SupermercadoServBem'], 'SupermercadoServBem->Estadio': ['SupermercadoServBem', 'RuadaBoaMorte', 'Rodoviaria', 'RuaAugustoJorge', 'Estadio'], 'Estadio->LimeiraShopping': ['Estadio', 'RuaFranciscoDAndrea', 'LimeiraShopping'], 'LimeiraShopping->FT': ['LimeiraShopping', 'RuaFranciscoDAndrea', 'Patron', 'RuaPaschoalMarmo', 'FT'], 'FT->ShoppingNacoesLimeira': ['FT', 'RuaPaschoalMarmo', 'Patron', 'RodoviaLimeira-Piracicaba', 'ShoppingNacoesLimeira'], 'ShoppingNacoesLimeira->Patron': ['ShoppingNacoesLimeira', 'RodoviaLimeira-Piracicaba', 'Patron']}

        expectedLength = 8
        expectedCost = 336240

        Search.getInstance().setGoalsNodes(['FT', 'Rodoviaria', 'Estadio', 'EspaçoColibri', 'ShoppingNacoesLimeira', 'LimeiraShopping', 'SupermercadoServBem'])

        solution = Search.getInstance().run()
        cost = Search.getInstance().finalCost

        self.assertEqual(expectedLength, len(solution))
        self.assertDictEqual(expectedSolution, solution)
        self.assertEqual(expectedCost, cost)

if __name__ == '__main__':
    unittest.main()