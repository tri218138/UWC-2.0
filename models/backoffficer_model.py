from models.database.database import Database

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
                    item['color'] = data['color']
                    break
            
        elif (action == 'delete'):
            for idx, item in enumerate(mcpData):
                if (item['id'] == data['id']):
                    pos = idx
                    break
            mcpData.pop(pos)
    # end by NTM
    
    def selectEmployee(self):
        return Database["employee"]
    def selectAllJanitorReady(self):
        data = [
            {'id': x["id"]} for x in Database["employee"] if x["role"] == "janitor" and x["state"] == "sẵn sàng"
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
        return data
    def selectMCPforAssign(self):
        data = [
            x for x in Database["mcp"] if x["available"] > 0 and x["id"] != "mcp0"
        ]
        return data
    def selectVehicleforAssign(self):
        data = [
            x for x in Database["vehicle"] if x["state"] == "sẵn sàng"
        ]
        return data
    def selectRouteforAssign(self):
        data = [
            x for x in Database["route"] if x["available"] > 0
        ]
        return data
    def selectTaskAssignedMCP(self):
        return Database["schedule"]["janitor"]    
    def selectTaskAssignedRoute(self):
        return Database["schedule"]["collector"]    
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
    def assignJanitor2MCP(self, data):
        for d in Database["employee"]:
            if d["id"] in data["janitor"]:
                d["state"] = "bận"
        for d in Database["mcp"]:
            if d["id"] in data["mcp"]:
                d["available"] = 0
        data = [
            { "mcp": data["mcp"][0], "date": data["date"][0], "shift": data["shift"][0], "janitor": data["janitor"][i] } for i in range(len(data["janitor"]))
        ]

        return Database["schedule"]["janitor"].extend(data)
    def assignCollector2Route(self, data):
        for d in Database["employee"]:
            if d["id"] in data["collector"]:
                d["state"] = "bận"
        for d in Database["vehicle"]:
            if d["id"] in data["vehicle"]:
                d["state"] = "đang chạy"
        data = [
            { "route": data["route"][0], "date": data["date"][0], "shift": data["shift"][0], "collector": data["collector"][0], "vehicle": data["vehicle"][0] }
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
    
    def selectScheduleInDate(self, date):
        ret = {}
        ret["janitor"] = []
        for d in Database["schedule"]["janitor"]:
            if d["date"] == date:
                ret["janitor"].append(d)
        return ret

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