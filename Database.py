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
                # print('listing returned', listings)

            
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
                return True
            
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


    def get_reviews_by_unit_id(
        self, unit_id
    ):  # To retrieve reviews for a specific lising (unit_id).

        # Fetch all reviews for a given unit_id"""
        if self.connection:
            cursor = self.connection.cursor()
            try:
                query = """
                    SELECT username, reviewText, rating 
                    FROM reviews 
                    WHERE unitID = %s
                """
                cursor.execute(query, (unit_id,))
                reviews = cursor.fetchall()

                # Return reviews as a list of dictionaries
                return [
                    {"username": row[0], "text": row[1], "rating": row[2]}
                    for row in reviews
                ]

            except mysql.connector.Error as e:
                print(f"Error fetching reviews: {e}")
                return []

            finally:
                cursor.close()
        return []
    
    def get_users_two_units_same_day(self, feature_x, feature_y):
        # 
        # Retrieve usernames of users who posted two units with specific features on the same day.
        
        if self.connection:
            cursor = self.connection.cursor()
            try:
                query = """
                    SELECT DISTINCT u.username
                    FROM user AS u
                    JOIN units unit1 ON u.username = unit1.username
                    JOIN features f1 ON unit1.unitID = f1.unitID
                    JOIN units unit2 ON u.username = unit2.username
                    JOIN features f2 ON unit2.unitID = f2.unitID
                    WHERE unit1.unitID != unit2.unitID
                    AND DATE(unit1.create_at) = DATE(unit2.create_at)
                    AND f1.featureName = %s
                    AND f2.featureName = %s
                    ORDER BY u.username;
                """
                cursor.execute(query, (feature_x, feature_y))
                results = cursor.fetchall()
                
                # Return a list of usernames
                return [row[0] for row in results]
            
            except mysql.connector.Error as e:
                print(f"Error fetching users with two units same day: {e}")
                return None
            
            finally:
                cursor.close()


    def get_filtered_items(self, filter_type, params=None):
        """
        Retrieve filtered items based on specific filter criteria.
        """
        if self.connection:
            cursor = self.connection.cursor()
            try:
                if filter_type == "most_expensive_features":
                    query = """
                        SELECT u.unitID, u.title, u.description, u.price, f.featureName
                        FROM units u
                        JOIN features f ON u.unitID = f.unitID
                        ORDER BY u.price DESC
                    """
                    cursor.execute(query)
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()

                    # Process the results into a dictionary with unitID as the key and features as a list
                    unit_dict = {}
                    for row in results:
                        listing = dict(zip(columns, row))
                        unit_id = listing['unitID']
                        # Initialize unit if it's not already in the dictionary
                        if unit_id not in unit_dict:
                            unit_dict[unit_id] = {
                                'title': listing['title'],
                                'description': listing['description'],
                                'price': listing['price'],
                                'features': []  # Start with an empty list for features
                            }
                        # Append the feature to the list for the given unit
                        unit_dict[unit_id]['features'].append(listing['featureName'])

                    return unit_dict

                elif filter_type == "units_reviews_good_or_excellent":
                    query = """
                        SELECT u.unitID, u.title, u.description, u.price, f.featureName
                        FROM units u
                        JOIN features f ON u.unitID = f.unitID
                        JOIN reviews r ON u.unitID = r.unitID
                        GROUP BY u.unitID, f.featureName
                        HAVING SUM(CASE WHEN r.rating NOT IN (3, 4) THEN 1 ELSE 0 END) = 0  -- Ensure all reviews are good (3) or excellent (4)
                        ORDER BY u.price DESC
                    """
                    cursor.execute(query)
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()

                    # Process the results into a dictionary with unitID as the key and features as a list
                    unit_dict = {}
                    for row in results:
                        listing = dict(zip(columns, row))
                        unit_id = listing['unitID']
                        # Initialize unit if it's not already in the dictionary
                        if unit_id not in unit_dict:
                            unit_dict[unit_id] = {
                                'title': listing['title'],
                                'description': listing['description'],
                                'price': listing['price'],
                                'features': []  # Start with an empty list for features
                            }
                        # Append the feature to the list for the given unit
                        unit_dict[unit_id]['features'].append(listing['featureName'])

                    return unit_dict

                elif filter_type == "users_only_poor_reviews":
                    query = """
                        SELECT r.username
                        FROM reviews r
                        GROUP BY r.username
                        HAVING COUNT(DISTINCT r.rating) = 1 AND MAX(r.rating) = 1
                        ORDER BY r.username
                    """
                    cursor.execute(query)
                    results = cursor.fetchall()
                    print(f"Users with poor reviews: {results}")

                    # Check if results are empty
                    if not results:
                        print("No users found with poor reviews.")  # Log if no results are found
                        return {}  

                    # Process the results into a dictionary with usernames
                    user_dict = {row[0]: {} for row in results}  # row[0] is the username
                    return user_dict

                #call the funtion for the two units
                elif filter_type == "users_two_units_same_day":
                    feature_x = None
                    feature_y = None
                    users = self.get_users_two_units_same_day(feature_x, feature_y)    
                    return users
                else:
                    print(f"Invalid filter type: {filter_type}")
                    return None

            except Error as e:
                print(f"Error in get_filtered_items: {e}")
                return None

            finally:
                cursor.close()


    def get_users_most_rentals_on_date(self):
            if self.connection:
                cursor = self.connection.cursor()
                try:
                    query = """
                    SELECT username, COUNT(*) AS unit_count
                    FROM units
                    WHERE DATE(create_at) = '2024-10-15'
                    GROUP BY username
                    HAVING COUNT(*) = (
                        SELECT COUNT(*) 
                        FROM units
                        WHERE DATE(create_at) = '2024-10-15'
                        GROUP BY username
                        ORDER BY COUNT(*) DESC
                        LIMIT 1
                    )
                    """
                    cursor.execute(query)
                    return cursor.fetchall()
                except Error as e:
                    print(f"Error: {e}")
                    return None
                finally:
                    cursor.close()
                    
                    
    def get_users_no_poor_reviews(self):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                query = """
                SELECT DISTINCT u.username
                FROM units u
                WHERE EXISTS (
                    SELECT 1
                    FROM units u2
                    WHERE u2.username = u.username
                )
                AND NOT EXISTS (
                    SELECT 1
                    FROM reviews r
                    WHERE r.unitID IN (
                        SELECT unitID
                        FROM units
                        WHERE username = u.username
                    )
                    AND r.rating = 1
                )
                ORDER BY u.username
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Error as e:
                print(f"Error: {e}")
                return None
            finally:
                cursor.close()