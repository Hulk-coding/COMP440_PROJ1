import mysql.connector


class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
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
        """BY adding %s to parameterized queries to protect from injection attacks"""
        if self.connection:
            try:
                q_insert = """INSERT INTO user (firstName, lastName, email, phone, username, password) VALUES (%s,%s,%s,%s,%s,%s)"""

                self.cursor.execute(
                    q_insert, (firstname, lastname, email, phone, username, password)
                )
                self.connection.commit()
                print("Account Created Successfully.")
            except mysql.connector.Error as err:
                print(f"Insert Failed: {err}")

    # add a function to retrieve user password for verification
    def get_user_password(self, username):
        if self.connection:
            try:
                query = "SELECT password FROM user WHERE username = %s"
                self.cursor.execute(query, (username,))
                result = self.cursor.fetchone()
                if result:
                    return result[0]  # Return the password
                else:
                    print(f"No user found with username: {username}")
                    return None
            except mysql.connector.Error as err:
                print(f"Error retrieving password: {err}")
                return None
        else:
            print("Not connected to the database")
            return None

    # add a function to remove a user from database

    #

    def close(self):
        """Closing Database..."""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database Closed")
