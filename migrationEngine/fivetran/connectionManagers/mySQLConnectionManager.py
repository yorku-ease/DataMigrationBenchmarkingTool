import mysql.connector
import time
from connectionManagers.connectionManager import ConnectionManager


class MySQLConnectionManager(ConnectionManager):

    def connect(self):
        # Connect to your MySQL database
        self.connection = mysql.connector.connect(host=self.host,user=self.username,password=self.password,database=self.database)
        self.cursor = self.connection.cursor()
        
    def table_exists(self,cursor,table_name):
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        return cursor.fetchone() is not None
    def deleteTables(self,tables):
        for table in tables:
            table = table.lower()
            query = f"DROP TABLE IF EXISTS {table}"
            print(query)
            self.cursor.execute(query)
            self.connection.commit()
            while self.table_exists(self.cursor, table):
                print(f"Table '{table}' exists.")
                time.sleep(5)  # Adjust the sleep duration as needed
            print(f"Table '{table}' is deleted")
    
    def close(self):
        if self.connection is not None:
            self.connection.cursor().close()
            self.connection.close()