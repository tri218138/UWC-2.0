from models.database.database import Database
from controllers.helper_function import *

class DBMS:
    def __init__(self):
        pass
    def selectVehicle(self):
        return Database["vehicle"]
    def handleActionVehicle(self, data):
    # by NTM
        vehicleData = Database["vehicle"]
        action = data["action"]
        data.pop("action")
        if (action == 'create'):
            print(data)
            vehicleData.append(data)
        elif (action == 'update'):
            for item in vehicleData:
                if (item['id'] == data['id']):
                    item['state'] = data['state']
                    item['type'] = data['type']
                    item['available'] = data['available']
                    break
            
        elif (action == 'delete'):
            for idx, item in enumerate(vehicleData):
                if (item['id'] == data['id']):
                    pos = idx
                    break
            vehicleData.pop(pos)
            
    def handleActionMcp(self, data):
        mcpData = Database["mcp"]
        action = data["action"]
        data.pop("action")
        if (action == 'create'):
            mcpData.append(data)
        elif (action == 'update'):
            for item in mcpData:
                if (item['id'] == data['id']):
                    # item['long'] = data['long']
                    # item['lat'] = data['lat']
                    item['available'] = data['available']
                    item['group'] = data['group']
                    break
            
        elif (action == 'delete'):
            for idx, item in enumerate(mcpData):
                if (item['id'] == data['id']):
                    pos = idx
                    break
            mcpData.pop(pos)
    # end by NTM
    
    def selectEmployee(self):
        today = getCurrentDateTime()
        empId = []
        for role in ["janitor", "collector"]:
            for s in Database["schedule"][role]:
                if s["datetime"].day == today.day and s["datetime"].month == today.month:
                    if s["shift"] == "sáng" and time_in_range(MORNING_SHIFT[0], MORNING_SHIFT[1], today.time()):
                        empId.append(s[role])
                    if s["shift"] == "chiều" and time_in_range(AFTERNOON_SHIFT[0], AFTERNOON_SHIFT[1], today.time()):
                        empId.append(s[role])
        for d in Database["employee"]:
            if d["id"] in empId and d["state"]=="sẵn sàng":
                d["state"] = "đang làm việc"
        return Database["employee"]
    def selectEmployeeById(self, id):
        today = getCurrentDateTime()
        for employee in Database["employee"]:
            if employee["id"] == id:
                role = employee["role"]
                if role in ["janitor", "collector"]:
                    for s in Database["schedule"][role]:
                        if s[role] == id and s["datetime"].day == today.day and s["datetime"].month == today.month:
                            if s["shift"] == "sáng" and time_in_range(MORNING_SHIFT[0], MORNING_SHIFT[1], today.time()):
                                employee["state"] = "đang làm việc"
                            if s["shift"] == "chiều" and time_in_range(AFTERNOON_SHIFT[0], AFTERNOON_SHIFT[1], today.time()):
                                employee["state"] = "đang làm việc"
                return employee
        return None
    def selectAllJanitorReady(self, datetime, shift):
        empId = []
        for s in Database["schedule"]["janitor"]:
            # print(s)
            if s["datetime"].day == datetime.day and s["datetime"].month == datetime.month:
                if s["shift"] == shift:
                    empId.append(s["janitor"])
        data = [
            {'id': x["id"]} for x in Database["employee"] if x["role"] == "janitor" and x["id"] not in empId
        ]
        return data
    def selectAllCollectorReady(self):
        data = [
            {'id': x["id"]} for x in Database["employee"] if x["role"] == "collector" and x["state"] == "sẵn sàng"
        ]
        return data
    def selectMCPforView(self):
        data = [
            x for x in Database["mcp"]
        ]
        for d in data:
            d["color"] = COLOR_GROUP[int(d["group"])]
        return data
    def selectMCPbyId(self, id):
        data = [
            x for x in Database["mcp"] if x["id"] == id
        ]
        for d in data:
            d["color"] = COLOR_GROUP[int(d["group"])]
        return data
    def selectMCPforAssign(self):
        data = [
            x for x in Database["mcp"] if int(x["available"]) > 0 and x["id"] != "mcp0"
        ]
        return data
    def selectVehicleforAssign(self):
        data = [
            x for x in Database["vehicle"] if x["state"] == "sẵn sàng"
        ]
        return data
    def selectRouteforAssign(self):
        data = [
            x for x in Database["route"] if int(x["available"]) > 0
        ]
        return data
    def selectTaskAssignedMCP(self, datetime, shift):
        sched = []
        print(datetime, shift, Database["schedule"]["janitor"])
        for s in Database["schedule"]["janitor"]:
            if s["datetime"].day == datetime.day and s["datetime"].month == datetime.month:
                if s["shift"] == shift:
                    sched.append(s)
        return sched
    def selectTaskAssignedRoute(self):
        return Database["schedule"]["collector"]    
    def selectRoute(self):
        return Database["route"]
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
    def assignJanitor2MCP(self, data):
        cnt = 0
        for d in Database["employee"]:
            if d["id"] in data["janitor"]:
                d["state"] = "đang làm việc"
                cnt += 1
        for d in Database["mcp"]:
            if d["id"] in data["mcp"]:
                d["available"] -= cnt
        data = [
            { "mcp": data["mcp"][0], 
            "datetime": data["datetime"][0], 
            "shift": data["shift"][0],
            "janitor": data["janitor"][i] } for i in range(len(data["janitor"]))
        ]

        return Database["schedule"]["janitor"].extend(data)
    def assignCollector2Route(self, data):
        for d in Database["employee"]:
            if d["id"] in data["collector"]:
                d["state"] = "đang làm việc"
        for d in Database["vehicle"]:
            if d["id"] in data["vehicle"]:
                d["state"] = "đang chạy"
        data = [
            { "route": data["route"][0], 
            "datetime": data["datetime"][0], 
            "shift": data["shift"][0],
            "collector": data["collector"][0], 
            "vehicle": data["vehicle"][0] }
        ]

        return Database["schedule"]["collector"].extend(data)
    def removeWorkAssignedJanitor2MCP(self, pair):
        print(Database["schedule"]["janitor"])
        print(pair)
        for p in Database["schedule"]["janitor"]:
            if p["mcp"] == pair["mcp"] and p["janitor"] == pair["janitor"]:
                for mem in Database["employee"]:
                    if mem['id'] == pair["janitor"]:
                        mem['state'] = 'sẵn sàng'
                        break
                for mcp in Database["mcp"]:
                    if mcp['id'] == pair["mcp"]:
                        mcp['available'] += 1
                Database["schedule"]["janitor"].remove(p)
                break
    def removeWorkAssignedCollector2Route(self, pair):
        print(Database["schedule"]["collector"])
        print(pair)
        for p in Database["schedule"]["collector"]:
            if p["route"] == pair["route"] and p["collector"] == pair["collector"]:
                for mem in Database["employee"]:
                    if mem['id'] == pair["collector"]:
                        mem['state'] = 'sẵn sàng'
                        break
                for route in Database["route"]:
                    if route['id'] == pair["route"]:
                        route['available'] += 1
                Database["schedule"]["collector"].remove(p)
                break
    def selectScheduleInDate(self, datetime):
        ret = {
            "janitor" : [],
            "collector": []
        }
        # ret["janitor"] = []
        for d in Database["schedule"]["janitor"]:
            if d["datetime"].day == datetime.day and d["datetime"].month == datetime.month:
                ret["janitor"].append(d)
        # ret["janitor"] = []
        for d in Database["schedule"]["collector"]:
            if d["datetime"].day == datetime.day and d["datetime"].month == datetime.month:
                ret["collector"].append(d)
        return ret

    def getLogMessage(self):
        return Database["log"]

    def addLogMessage(self, log):
        Database["log"].append(log)

    # def selectUserProfile(self, id):
    #     for c in Database["employee"]:
    #         if c["id"] == id:
    #             return c  
    def createNewAuth(self, data):
        # data = {"id" :"", "username": "", "password": "", "role": ""}
        Database["authentication"].append(data)
dbms = DBMS()