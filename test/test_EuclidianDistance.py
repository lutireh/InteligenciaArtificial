import unittest
import pandas as pd

from InteligenciaArtificial.map.DbHandler import DbHandler
from InteligenciaArtificial.utils.consts.DbConsts import DB_EUCLIDIAN_DISTANCE


class EuclidianDistanceTest(unittest.TestCase):
    def setUp(self):
        DbHandler.getInstance().initializeDb(pd.read_excel('../map/a_star.xlsx', sheet_name=None))

    def testGetEuclidianFromFT(self):
        result = DbHandler.getInstance().getColumn("FT", DB_EUCLIDIAN_DISTANCE)
        print(result)
        self.assertIsNotNone(result, "Is None")

    def testGetRelationatedNamesFromFT(self):
        result = DbHandler.getInstance().getRelationalStreetName("FT")
        print(result)
        self.assertIsNotNone(result, "Is None")

    def testGetDistanceBetweenPatronAndFT(self):
        result = DbHandler.getInstance().getDBColumns("FT", "Patron", DB_EUCLIDIAN_DISTANCE)
        print(result)
        self.assertEqual(1320,result)


if __name__ == '__main__':
    unittest.main()
