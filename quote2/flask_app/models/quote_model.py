from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models.user_model import User

class Quote:
    def __init__(self, data):
        self.id = data['id']
        self.author = data['author']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_all_quote_with_user(cls):
        query = "SELECT * FROM quotes JOIN users ON users.id = quotes.user_id;"
        result = connectToMySQL(DATABASE).query_db(query)
        if len(result) > 0:
            quotes = []
            for row in result:
                one_quote = cls(row)
                user_table = {
                    "id": row['users.id'],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"]
                }
                user = User(user_table)
                one_quote.maker = user
                quotes.append(one_quote)
            return quotes
        else: 
            return None
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO quotes( author, description, created_at, user_id) VALUES (%(author)s, %(description)s, %(created_at)s, %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    #Join Statement
    @classmethod
    def show_one(cls, data):
        query = "SELECT * FROM quotes JOIN users ON users.id = quotes.user_id WHERE quotes.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result) > 0:
            row = result[0]
            one_quote = cls(row)
            user_table = {
                    "id": row['users.id'],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"]
                }
            user = User(user_table)
            one_quote.maker = user
            return one_quote
        else: 
            return None

#edit quotes
    @classmethod
    def edit_quote(cls, data):
        query = " UPDATE quotes SET author = %(author)s, description = %(description)s, created_at = %(created_at)s, user_id = %(user_id)s WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    #edit routes
    @classmethod
    def view_one(cls,data):
        query = "SELECT * FROM quotes WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if len(result) > 0:
            return cls(result[0])
        else: 
            return None

#delete
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM quotes WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

