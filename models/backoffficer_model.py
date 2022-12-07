from models.database.database import Database

class DBMS:
    def __init__(self):
        pass
    def selectVehicle(self):
        return Database["vehicle"]
    # by NTM
    def handleActionVehicle(self, data):
        vehicleData = Database["vehicle"]
        action = data["action"]
        data.pop("action")
        if (action == 'create'):
            vehicleData.append(data)
        elif (action == 'update'):
            for idx, item in enumerate(vehicleData):
                if (item['id'] == data['id']):
                    pos = idx
                    break
            if (vehicleData[pos]['state'] == 'sẵn sàng'):
                vehicleData[pos]['state'] = 'hỏng'
            else:
                vehicleData[pos]['state'] = 'sẵn sàng'
        elif (action == 'delete'):
            for idx, item in enumerate(vehicleData):
                if (item['id'] == data['id']):
                    pos = idx
                    break
            vehicleData.pop(pos)
    # end by NTM
    
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