import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection =  None
        self.cursor = None
        
    def connect(self):
        """Establish Connection with Database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )    
            self.cursor = self.connection.cursor()
            print("Connected")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection = None
            
    def insert(self, firstname, lastname, email, phone, username, password):
        """Insert New Account"""
        if self.connection:
            try:
                q_insert = """INSERT INTO accounts (first_name, last_name, email, phone, username, password) VALUES (%,%,%,%,%,%)"""
        
                self.cursor.execute(q_insert, (firstname, lastname, email, phone, username, password))
                self.connection.commit()
                print("Account Created Successfully.")
            except mysql.connector.Error as err:
                print(f"Insert Failed: {err}")
                
    def close(self):
        """Closing Database..."""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database Closed")