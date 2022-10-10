from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod   #decorator
    def register_user(cls,data): #save the registration
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s );"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result 
        
    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all_user(cls, data):
        query = "SELECT * FROM users;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        if len(result) < 1:
            return None
        return cls(result[0])

    # Validation!
    @staticmethod
    def validate_session():
        if "user_id" not in session:
            return False
        else:
            return True

    @staticmethod
    def validate_registration(data): #data is accepting request.form from app.route "/register" is being used to the register app.route in user_controller
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result) >= 1:
            flash("Email not available.","register")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(data['first_name']) < 2:
            flash("Name needs to be at least 2 characters","register")
            is_valid= False
        if len(data['last_name']) < 2:
            flash("Needs to must be at least 2 characters","register")
            is_valid= False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if data['password'] != data['confirm']:
            flash("Passwords don't match","register")
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        if data['email'] == "":
            flash("*Please enter a email.", "login_error")
            is_valid = False
        if data['password'] == "":
            flash("*Please enter a password.", "login_error")
            is_valid = False
        return is_valid

