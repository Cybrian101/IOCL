import sqlite3

# Connect to SQLite database (this will create the database file if not exists)
conn = sqlite3.connect('database3.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Define ALTER TABLE command to add user_id column before serial_number
alter_commands = [
    '''
    CREATE TABLE IF NOT EXISTS activities (
        user_id TEXT, -- Add user_id column before serial_number
        serial_number INTEGER PRIMARY KEY,
        current_date TEXT,
        down_date TEXT,
        down_time TEXT,
        main_category TEXT,
        sub_category TEXT,
        id_number TEXT,
        ticket_id TEXT,
        remarks TEXT,
        modify_engineer_name TEXT,
        up_time TEXT,
        status TEXT DEFAULT 'Active' -- Default status is 'Active'
    )
    '''
]

# Execute ALTER TABLE commands to modify table schema
for alter_command in alter_commands:
    try:
        cursor.execute(alter_command)
        conn.commit()
        print(f"Table altered successfully: {alter_command}")
    except sqlite3.OperationalError as e:
        print(f"Table alteration error: {e}")

# Close connection
conn.close()
