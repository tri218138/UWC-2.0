from models.database.database import Database
import pandas as pd

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
    def selectScheduleInDate(self, date):
        ret = {}
        ret["collector"] = []
        for d in Database["schedule"]["collector"]:
            if d["date"] == date:
                ret["collector"].append(d)
        return ret


    def selectEmployee(self):
        pairWork = Database["employee"]
        lis = []
        for x in pairWork:
            if x["role"] == "collector" :
                lis.append(x)
        return lis

    def getLogMessage(self):
        return Database["log"]

    def addLogMessage(self, log):
        Database["log"].append(log)

    def selectUserProfile(self, id):
        for c in Database["employee"]:
            if c["id"] == id:
                return c    

dbms = DBMS()
