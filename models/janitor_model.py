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
    def selectScheduleInDate(self, id, datetime):
        ret = {
            "janitor" : [],
            "collector": []
        }

        myschedule = None
        for d in Database["schedule"]["janitor"]:
            if d["janitor"] == id  and d["datetime"].day == datetime.day and d["datetime"].month == datetime.month:
                myschedule = d
                break
        if myschedule is None:
            return ret
        for d in Database["schedule"]["janitor"]:
            if d["mcp"] == myschedule["mcp"] and d["datetime"].day == datetime.day and d["datetime"].month == datetime.month:
                ret["janitor"].append(d)
        # ret["janitor"] = []
        # for d in Database["schedule"]["collector"]:
        #     if d["datetime"].day == datetime.day and d["datetime"].month == datetime.month:
        #         ret["collector"].append(d)
        return ret
    def selectScheduleInMonth(self, id, month):
        for d in Database["schedule"]["janitor"]:
            if d["janitor"] == id:
                myschedule = d
        # if myschedule is None:
        #     return ret
        # for d in Database["schedule"]["janitor"]:
        #     if d["mcp"] == myschedule["mcp"] and d["datetime"].day == datetime.day and d["datetime"].month == datetime.month:
        #         ret["janitor"].append(d)
dbms = DBMS()
