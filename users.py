#Class that holds all user from the start of bot
#Class contains functions which manipulate with user
class Users:
    def __init__(self):
        self.users = []

    def addUser(self, user):
        self.users.append(user)

    def setUser(self, id, location, asked_for_location):
        for x in self.users:
            if x.id == id:
                x.location = location
                x.asked_for_location = asked_for_location

    def findUserById(self, id):
        for x in self.users:
            if x.id == id:
                return x

#Class for creating User model to use them inside Users
class User:
    def __init__(self, id, asked_for_location):
        self.id = id
        self.location = ""
        self.asked_for_location = asked_for_location
