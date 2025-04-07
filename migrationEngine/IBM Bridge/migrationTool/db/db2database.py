import ibm_db,sys,ibm_db_dbi,time,paramiko

class Db2Database : 
    def __init__(self, DB2host,DB2Username,DB2Password,DB2Port,DB2type,DBname,DBschema,ssl=False):
        self.DB2host = DB2host
        self.DB2Username = DB2Username
        self.DB2Password = DB2Password
        self.DB2Port = DB2Port
        self.DB2type = DB2type
        self.DBschema = DBschema
        self.DBname = DBname
        self.dsn = (
    f"DATABASE={self.DBname};"
    f"HOSTNAME={self.DB2host};"
    f"PORT={self.DB2Port};"
    f"PROTOCOL=TCPIP;"
    f"UID={self.DB2Username};"
    f"PWD={self.DB2Password};"
)
        self.ssl = ssl
    
    def test_connection(self, client):
        payload = {
            "host": self.DB2host,
            "database_name": self.DBname,
            "database_port": self.DB2Port,
            "ssl": self.ssl,
            "username": self.DB2Username,
            "password": self.DB2Password
        }
        return client.post("/migration/test-connection/", payload)
    
    def clearDB(self,tables):
        try:
            self.tablesToMigrate  = [string.lower() for string in tables]
            ibm_db_conn = ibm_db.connect(self.dsn , "", "")
            conn = ibm_db_dbi.Connection(ibm_db_conn)
            tables = conn.tables(self.DBschema, '%')
            for table in tables:
                if table['TABLE_NAME'].lower() not in self.tablesToMigrate :
                    print("table " + str(table['TABLE_NAME']) + " is not in the list of tables to be migrated. No need to delete") 
                    continue
                table_name = table['TABLE_NAME']
                print(f"Dropping table: {table_name}")
                drop_sql = f"DROP TABLE {self.DBschema}.{table_name}"
                ibm_db.exec_immediate(ibm_db_conn, drop_sql)
                print(f"Executed: {drop_sql}")
                # Wait until the table is deleted
                while True:
                    tables = conn.tables(self.DBschema, '%')
                    if not any(t['TABLE_NAME'] == table_name for t in tables):
                        print(f"Table {table_name} has been dropped.")
                        break
                    else:
                        print(f"Waiting for table {table_name} to be dropped...")
                        time.sleep(2)


        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

        finally:
            # Close the connection
            ibm_db.close(ibm_db_conn)
            print("Connection closed")