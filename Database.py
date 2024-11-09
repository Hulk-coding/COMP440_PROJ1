import mysql.connector
import bcrypt
from PyQt5.QtWidgets import QMessageBox
from mysql.connector import Error

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

    def insert_new_user(self, firstname, lastname, email, phone, username, password):
        """Insert New Account"""
        """BY adding %s to parameterized queries to protect from injection attacks"""
        if self.connection:
            try:
                q_insert = """INSERT INTO user (firstName, lastName, email, phone, username, password) VALUES (%s,%s,%s,%s,%s,%s)"""

                self.cursor.execute(
                    q_insert, (firstname, lastname, email, phone, username, password)
                )
                self.connection.commit()
                return True
                
            except mysql.connector.Error as err:
                print(f"Insert Failed: {err}")
                return False
            
    def obtain_listings(self, city, description, feature, price):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                
                query = """
                SELECT u.unitID, u.title, u.description, u.price, u.username, u.create_at, f.featureName
                FROM units u
                JOIN features f ON u.unitID = f.unitID
                WHERE u.unitID IN (
                    SELECT unitID FROM features WHERE featureName = %s
                );
                
               
                
                """""
                cursor.execute(query, (feature,))
                
                 
                columns = [col[0] for col in cursor.description]  
                listings = cursor.fetchall()
                print('listing returned', listings)

            
                unit_dict = {}
                for row in listings:
                    listing = dict(zip(columns, row))
                    unit_id = listing['unitID']
                    if unit_id not in unit_dict:
                       
                        unit_dict[unit_id] = {
                            'title': listing['title'],
                            'description': listing['description'],
                            'price': listing['price'],
                            'username': listing['username'],
                            'create_at': listing['create_at'],
                            'features': []  
                        }
                   
                    unit_dict[unit_id]['features'].append(listing['featureName'])

                return unit_dict
                        
                       
            except Error as e:
                print(f"Error: {e}")
                return None 
                
            finally:
                if self.connection:
                    cursor.close()
                    self.connection.close()
 
            
    # insert new listing 
    def insert_new_unit (self, title, description, price, username, features):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.callproc('AddRental', (title, description, price, username, features))
                self.connection.commit()
                
                print('Unit added to DB success')
            
            except Error as e:
                print(f"Error: {e}")
                
            finally:
                if self.connection:
                    cursor.close()
                    self.connection.close()
                    
                    
    def submit_review(self, unit_id, username, review_text, rating):
        if self.connection:
            cursor = self.connection.cursor()

        try:
        

            # Call the procedure
            cursor.callproc(
                "AddReview",
                (unit_id, username, review_text, rating),
            )

            # Commit the transaction
            self.connection.commit()

            print('review added to database')
            self.close()

        except mysql.connector.Error as e:
            print(f"Error: {e}")

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()

                
            
                
    #add a function to retrieve user password for verification
    def check_password(self, username, password):
      
        cursor = self.connection.cursor()
        cursor.execute("SELECT password FROM user WHERE username = %s", (username,))
        result = cursor.fetchone()
        
        if result:
            stored_hash=result[0]
            return bcrypt.checkpw(password.encode("utf-8"), stored_hash)
        return False
    
    
    #add a function to remove a user from database
                
    def close(self):
        """Closing Database..."""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database Closed")
