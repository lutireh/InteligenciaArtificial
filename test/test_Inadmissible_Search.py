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
        Search.getInstance().clearNodes()


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

    # TODO Revisar possivel inconsistência
    def testRunSingleObjective(self):
        expectedSolution = {'Patron->Rodoviaria': ['Patron', 'RuaBaraodeCampinas', 'Rodoviaria'],
                          'Rodoviaria->Patron': ['Rodoviaria', 'RuadaBoaMorte', 'Patron']}
        expectedCost = 22300
        admissibleCost = 18400

        Search.getInstance().setGoalsNodes(["Rodoviaria"])

        solution = Search.getInstance().run()
        cost = Search.getInstance().finalCost

        self.assertEqual(expectedSolution, solution)
        self.assertEqual(expectedCost, cost)
        self.assertGreater(cost, admissibleCost)

    def testRunMultipleObjective(self):
        expectedReturn ={'Patron->Estadio': ['Patron', 'RuaPresidenteRoosevelt', 'Estadio'], 'Estadio->ShoppingNacoesLimeira': ['Estadio', 'RuaPresidenteRoosevelt', 'Patron', 'RodoviaLimeira-Piracicaba', 'ShoppingNacoesLimeira'], 'ShoppingNacoesLimeira->Patron': ['ShoppingNacoesLimeira', 'RodoviaLimeira-Piracicaba', 'Patron']}
        expectedLength = 3
        expectedCost = 154400
        admissibleCost = 146000

        Search.getInstance().setGoalsNodes(['Estadio', 'ShoppingNacoesLimeira'])

        solution = Search.getInstance().run()
        cost = Search.getInstance().finalCost

        self.assertEqual(expectedLength, len(solution))
        self.assertDictEqual(expectedReturn, solution)
        self.assertEqual(expectedCost, cost)
        self.assertGreater(cost, admissibleCost)

    def testRunAllObjective(self):
        expectedSolution = {'Patron->EspaçoColibri': ['Patron', 'RuadaBoaMorte', 'AvenidaSantaBarbara', 'EspaçoColibri'], 'EspaçoColibri->Rodoviaria': ['EspaçoColibri', 'AvenidaSantaBarbara', 'RuadaBoaMorte', 'Rodoviaria'], 'Rodoviaria->SupermercadoServBem': ['Rodoviaria', 'RuadaBoaMorte', 'SupermercadoServBem'], 'SupermercadoServBem->Estadio': ['SupermercadoServBem', 'RuadaBoaMorte', 'Rodoviaria', 'RuaAugustoJorge', 'Estadio'], 'Estadio->LimeiraShopping': ['Estadio', 'RuaFranciscoDAndrea', 'LimeiraShopping'], 'LimeiraShopping->FT': ['LimeiraShopping', 'RuaFranciscoDAndrea', 'AvenidaConegoManuelAlves', 'FT'], 'FT->ShoppingNacoesLimeira': ['FT', 'RuaPaschoalMarmo', 'Patron', 'RodoviaLimeira-Piracicaba', 'ShoppingNacoesLimeira'], 'ShoppingNacoesLimeira->Patron': ['ShoppingNacoesLimeira', 'RodoviaLimeira-Piracicaba', 'Patron']}

        expectedLength = 8
        admissibleCost = 336240
        expectedCost = 338320

        Search.getInstance().setGoalsNodes(['FT', 'Rodoviaria', 'Estadio', 'EspaçoColibri', 'ShoppingNacoesLimeira', 'LimeiraShopping', 'SupermercadoServBem'])

        solution = Search.getInstance().run()
        cost = Search.getInstance().finalCost

        self.assertEqual(expectedLength, len(solution))
        self.assertDictEqual(expectedSolution, solution)
        self.assertEqual(expectedCost, cost)
        self.assertGreater(cost, admissibleCost)


if __name__ == '__main__':
    unittest.main()