from flask import session
ACCESS = {
    'user': 1,
    'admin': 2
}

class User():
    def __init__(self, username, email, password, access=ACCESS['user']):
        self.username = username
        self.email = email
        self.password = password
        self.access = access
        
    def is_admin(self):
        self.access = ACCESS['admin']
        return self.access