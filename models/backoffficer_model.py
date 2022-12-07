from models.database.database import Database

class DBMS:
    def __init__(self):
        pass
    def selectVehicle(self):
        return Database["vehicle"]
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
            x for x in Database["vehicle"] if x["available"] > 0 and x["state"] == "sẵn sàng"
        ]
        return data
    def selectRouteforAssign(self):
        data = [
            x for x in Database["route"] if x["available"] > 0
        ]
        return data
    def selectTaskAssignedMCP(self):
        return Database["schedule"]["janitor"]    
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
    def assignJanitor2MCP(self, pairs):
        for d in Database["employee"]:
            if d["id"] in pairs["janitor"]:
                d["state"] = "bận"
        for d in Database["mcp"]:
            if d["id"] in pairs["mcp"]:
                d["available"] = 0
        pairs = [
            { "mcp": pairs["mcp"][0], "janitor": pairs["janitor"][i] } for i in range(len(pairs["janitor"]))
        ]

        return Database["schedule"]["janitor"].extend(pairs)
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
dbms = DBMS()