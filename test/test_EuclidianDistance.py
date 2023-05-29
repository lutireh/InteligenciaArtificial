import unittest
import pandas as pd

from InteligenciaArtificial.map.EuclidianDistance import EuclidianDistance


class EuclidianDistanceTest(unittest.TestCase):
    def setUp(self):
        EuclidianDistance.getInstance().initializeDb(pd.read_excel('../map/a_star.xlsx', sheet_name=None))

    def testGetEuclidianFromFT(self):
        result = EuclidianDistance.getInstance().getEuclidianDistance("FT")
        print(result)
        self.assertIsNotNone(result, "Is None")

    def testGetRelationatedNamesFromFT(self):
        result = EuclidianDistance.getInstance().getRelationalStreetName("FT")
        print(result)
        self.assertIsNotNone(result, "Is None")

    def testGetDistanceBetweenPatronAndFT(self):
        result = EuclidianDistance.getInstance().getDistanceBetweenStreets("FT", "Patron")
        print(result)
        self.assertEquals(result, 1320)


if __name__ == '__main__':
    unittest.main()
