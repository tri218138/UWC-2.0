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
    def selectScheduleInDate(self, id, datetime):
        ret = {
            "janitor" : [],
            "collector": []
        }

        myschedule = None
        for d in Database["schedule"]["collector"]:
            if d["collector"] == id  and d["datetime"].day == datetime.day and d["datetime"].month == datetime.month:
                myschedule = d
                break
        if myschedule is None:
            return ret
        for d in Database["schedule"]["collector"]:
            if d["route"] == myschedule["route"] and d["datetime"].day == datetime.day and d["datetime"].month == datetime.month:
                ret["collector"].append(d)
        # ret["janitor"] = []
        # for d in Database["schedule"]["collector"]:
        #     if d["datetime"].day == datetime.day and d["datetime"].month == datetime.month:
        #         ret["collector"].append(d)
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
    def selectRouteById(self, id):
        for r in  Database["route"]:
            if r["id"] == id:
                return r
    def selectMCPinRouteId(self, routeid):
        route = self.selectRouteById(routeid)
        if route is None:
            return []
        else:
            ret = []
            for m in Database["mcp"]:
                if m["id"] in route["mcpIDs"]:
                    ret.append(m)
            return ret
dbms = DBMS()
