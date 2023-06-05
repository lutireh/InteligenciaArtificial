class EuclidianDistance:

    _instance = None

    def __init__(self):
        self._db = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = EuclidianDistance()

        return cls._instance

    def initializeDb(self, db):
        self._db = db

    def getDb(self):
        if self._db is None:
            return "Não existe db"
        return self._db

    def getEuclidianDistance(self, node):
        return self._db.get(node)["Euclidiana"]

    def getRealDistance(self, node):
        return self._db.get(node)["Real"]

    def getRelationalStreetName(self, node):
        return self._db.get(node)["Nos"]

    def getDistanceBetweenStreets(self, initialStreet, goalStreet):
        goalStreetIndex = 0
        distancesInitialStreet = self.getRelationalStreetName(initialStreet)

        for i, street in enumerate(distancesInitialStreet):
            if street == goalStreet:
                goalStreetIndex = i
                break

        return self.getEuclidianDistance(initialStreet)[goalStreetIndex]

    def getRealDistanceBetweenStreets(self,  initialStreet, goalStreet):
        goalStreetIndex = 0
        distancesInitialStreet = self.getRelationalStreetName(initialStreet)

        for i, street in enumerate(distancesInitialStreet):
            if street == goalStreet:
                goalStreetIndex = i
                break

        return self.getRealDistance(initialStreet)[goalStreetIndex]