from models.database.database import Database

class DBMS:
    def __init__(self):
        pass
    
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
    def selectEmployee(self):
        return Database["employee"]

    def getLogMessage(self):
        return Database["log"]

    def addLogMessage(self, log):
        Database["log"].append(log)

    def selectUserProfile(self, id):
        for c in Database["employee"]:
            if c["id"] == id:
                return c    

dbms = DBMS()