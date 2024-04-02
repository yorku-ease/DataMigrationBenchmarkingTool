

class ConnectionManager:

    def __init__(self, host,database,username,password):
        # Define the SSH parameters
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection  = None
    def connect(self):
        pass
    
    def deleteTables(self,tables):
        pass
