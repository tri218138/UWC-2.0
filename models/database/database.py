from models.database.employee import employeeData
from models.database.mcp import MCPData
from models.database.route import routeData
from models.database.schedule import pairWorkData
from models.database.vehicle import vehicleData

Database = {
    "employee": employeeData,
    "mcp": MCPData,
    "route": routeData,
    "schedule": pairWorkData,
    "vehicle": vehicleData
}