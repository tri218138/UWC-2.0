from models.database.database import Database

class DBMS:
    def __init__(self):
        pass
    def checkLogin(self, un, pw):
        for auth in Database["authentication"]:
            if auth["username"] == un and auth["password"] == pw:
                return True, auth
        return False, None

authService = DBMS()