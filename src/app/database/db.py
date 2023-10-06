import mysql.connector
import os
import pymysql


def connect_to_database():
    db_password = os.environ.get('DB_PASSWORD')  
    connection = mysql.connector.connect(
        host='flask-app-rds-cluster.chnoobsehdtd.us-east-1.rds.amazonaws.com',
        user='tvbum_admin',
        password=db_password,
        database='flask_app_db'
    )
    return connection

def connect_to_database2():# This is python3 vision, mysql lib can not be used in python3
    # db_password = os.environ.get('DB_PASSWORD')  
    connection = pymysql.connect(
        host='flask-app-rds-cluster.chnoobsehdtd.us-east-1.rds.amazonaws.com',
        user='tvbum_admin',
        password='od9KN7pOhEV32oz',
        database='flask_app_db'
    )
    return connection

def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()

# def insert_user_into_db(first_name, last_name, email, hashed_password):
#     try:
#         # Connect to the database
#         connection = connect_to_database()
#         insert_query = "INSERT INTO users (first_name, last_name, email, hashed_password) VALUES (%s, %s, %s, %s)"
#         data = (first_name, last_name, email, hashed_password)
#         # Execute the SQL query to insert the user data
#         execute_query(connection, insert_query, data)
#         connection.commit()
#         connection.close()
#         return True

#     except Exception as e:
#         # Handle any exceptions 
#         print(f"Error inserting user data into the database: {str(e)}")
#         return False

def insert_user_into_db(first_name, last_name, email, hashed_password,validationcode):
    try:
        # Connect to the database
        connection = connect_to_database2()
        insert_query = "INSERT INTO users (first_name, last_name, email, hashed_password, validationcode, isvalidation) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (first_name, last_name, email, hashed_password,validationcode,0)
        # Execute the SQL query to insert the user data
        execute_query(connection, insert_query, data)
        connection.commit()
        connection.close()
        return True

    except Exception as e:
        # Handle any exceptions 
        print(f"Error inserting user data into the database: {str(e)}")
        return False


def fetch_hashed_password(email):
    try:
        # Connect to the database
        connection = connect_to_database()

        # Define the SQL query to fetch the hashed password based on email
        select_query = "SELECT hashed_password FROM users WHERE email = %s"
        data = (email,)

        cursor = connection.cursor(dictionary=True)
        cursor.execute(select_query, data)

        result = cursor.fetchone()

        cursor.close()
        connection.close()
        if result:
            return result['hashed_password']
        else:
            return None

    except Exception as e:
        # Handle any exceptions or errors that may occur during database retrieval
        print(f"Error fetching hashed password from the database: {str(e)}")
        return None

def isAccountVerified(email):
    try:
        connection = connect_to_database2()
        
        select_query="select isvalidation from users where email = %s"
        data=(email,)

        cursor = connection.cursor()
        cursor.execute(select_query, data)

        result= cursor.fetchone()

        cursor.close()
        connection.close()
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"Error fetching hashed password from the database: {str(e)}")
        return None

def getValidationCode(email):
    try:
        connection = connect_to_database2()
        
        select_query="select validationcode from users where email = %s"
        data=(email,)

        cursor = connection.cursor()
        cursor.execute(select_query, data)

        result= cursor.fetchone()

        cursor.close()
        connection.close()
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"Error fetching hashed password from the database: {str(e)}")
        return None
    
def alterValidationState(email):
    try:
        connection = connect_to_database2()
        
        updata_query="UPDATE users SET isvalidation=true WHERE email = %s"
        data=(email,)

        cursor = connection.cursor()
        cursor.execute(updata_query, data)

        cursor.close()
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error fetching hashed password from the database: {str(e)}")
        return None