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
    def selectUserProfile(self):
        for c in Database["employee"]:
            if c["username"] == "":
                return c
dbms = DBMS()