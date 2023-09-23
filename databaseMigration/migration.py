import mysql.connector


# Specify the tdatabase name you want to transfer
database_name='classicmodels'
# Specify the table name
table_name = 'customers'


# Connect to the source database
source_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database=database_name
)

# Connect to the destination database
target_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    port="3307"
)

# Create cursor objects for both databases
source_cursor = source_db.cursor()
#destination_cursor = destination_db.cursor()
target_cursor = target_db.cursor()


#Create the Database
create_db_query = f"CREATE DATABASE {database_name}"
target_cursor.execute(create_db_query)

#selecte target database
target_db.database = database_name

# Execute the query to list all tables
query = "SHOW TABLES"
source_cursor.execute(query)

# Fetch all the tables
tables = source_cursor.fetchall()

# Print the table names
for table in tables:
    table_name = table[0]


    # Retrieve the table schema from the source database
    describe_query = f"DESCRIBE {table_name}"
    source_cursor.execute(describe_query)
    table_schema = source_cursor.fetchall()

    # Generate the SQL query to create the table in the target database
    create_table_query = f"CREATE TABLE {table_name} ("

    column_names = []
    for column in table_schema:
        column_name = column[0]
        column_names.append(column_name)
        column_type = column[1].decode('utf-8')
        create_table_query += f"{column_name} {column_type}, "
    create_table_query = create_table_query.rstrip(', ')
    create_table_query += ")"

    # Execute the CREATE TABLE query in the target database
    target_cursor.execute(create_table_query)


    columns = column_names
    # Retrieve the data from the source table
    select_query = f"SELECT {', '.join(columns)} FROM {table_name}"
    source_cursor.execute(select_query)
    data = source_cursor.fetchall()

    
    # Insert the data into the destination table
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(columns))})"
    target_cursor.executemany(insert_query, data)

# Commit the changes and close the connections
target_db.commit()
source_cursor.close()
source_db.close()
target_cursor.close()
target_db.close()