from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import product
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = "RoyalT_website"

    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.is_admin = data["is_admin"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password, is_admin)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(is_admin)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all_users(cls):
        query = """
        SELECT * FROM users;
        """
        results = connectToMySQL(cls.db).query_db(query)

        all_users = []

        for user in results:
            all_users.append(cls(user))
        return all_users
    
    @classmethod
    def get_by_email(cls,data):
        query = """
        SELECT * FROM users 
        WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query= """
        SELECT * FROM users
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])
    @classmethod
    def admin(cls):
        query= """
        SELECT * FROM users
        WHERE is_admin = 1;
        """
        results = connectToMySQL(cls.db).query_db(query)
        if not results:
            return False
        return cls(results[0])
    
    @staticmethod
    def is_valid_reg(data):
        is_valid = True
        one_user = User.get_by_email(data)

        if one_user:
            is_valid = False
            flash("Please log in", "reg")

        if len(data["first_name"]) < 2:
            is_valid = False
            flash("First name min 2 characters", 'reg')

        if len(data["last_name"]) < 2:
            is_valid = False
            flash("Last name min 2 characters", 'reg')

        if len(data["email"]) == 0:
            is_valid = False
            flash("Email cannot be left empty", 'reg')
        
        if not EMAIL_REGEX.match(data['email']):
            flash('invalid email address!', 'reg')
            is_valid = False
        
        if len(data["password"]) < 8:
            is_valid = False
            flash("Password min 8 characters", 'reg')
        
        if data["password_confirmation"] != data["password"]:
            is_valid = False
            flash("Password must match password confirmation", 'reg')
        return is_valid