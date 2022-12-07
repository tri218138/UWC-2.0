from models.database.database import Database

class DBMS:
    def __init__(self):
        pass
    def selectVehicle(self):
        return Database["vehicle"]
    def selectEmployee(self):
        return Database["employee"]
    def selectMCP(self):
        return Database["mcp"]
    def selectRoute(self):
        return Database["route"]
    def selectUserProfile(self, id):
        for c in Database["employee"]:
            if c["id"] == id:
                return c
        return None
    def saveEmployeeInformation(self, id, data):
        for c in Database["employee"]:
            if c["id"] == id:
                for key in c:
                    if key in data:
                        c[key] = data[key]
dbms = DBMS()