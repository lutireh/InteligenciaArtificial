from InteligenciaArtificial.utils.consts.DbConsts import DB_EUCLIDIAN_DISTANCE, DB_REAL_DISTANCE, DB_ESTIMATED_TIME, DB_NODES

class DbHandler:
    _instance = None

    def __init__(self):
        self._db = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = DbHandler()
        return cls._instance

    def initializeDb(self, db):
        self._db = db

    def getDb(self):
        if self._db is None:
            print("Missing db")
            return None
        return self._db

    def getRelationalStreetName(self, node):
        return self._db.get(node)[DB_NODES]

    def getColumn(self, node, columnName):
        return self._db.get(node)[columnName]

    def getDBColumns(self, initialNode, goalNode, columnName):
        goalNodeIndex = 0
        for i, node in enumerate(self.getRelationalStreetName(initialNode)):
            if node == goalNode:
                goalNodeIndex = i
                break
        if columnName == DB_EUCLIDIAN_DISTANCE:
            return self.getColumn(initialNode, DB_EUCLIDIAN_DISTANCE)[goalNodeIndex]
        elif columnName == DB_REAL_DISTANCE:
            return self.getColumn(initialNode, DB_REAL_DISTANCE)[goalNodeIndex]
        elif columnName == DB_ESTIMATED_TIME:
            return self.getColumn(initialNode, DB_ESTIMATED_TIME)[goalNodeIndex]
