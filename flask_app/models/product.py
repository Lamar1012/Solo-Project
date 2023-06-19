from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Product:
    db = "royalt_website"

    def __init__(self, data):
        self.id = data["id"]
        self.price = data["price"]
        self.product_name = data["product_name"]
        self.product_image = data["product_image"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.customer = None
    
    @classmethod
    def create_product(cls, data):
        query = """
        INSERT INTO products
        (price, product_name, product_image, user_id)
        VALUES(%(price)s, %(product_name)s, %(product_image)s, %(user_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all_products(cls):
        query = """
        SELECT * FROM products
        JOIN users on products.user_id = users.id;
        """
        results = connectToMySQL(cls.db).query_db(query)

        products = []

        for row in results:
            selected_product = cls(row)

            user_data = {
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "is_admin":row["is_admin"],
                "created_at":row["users.created_at"],
                "updated_at":row["users.updated_at"]
            }

            selected_product.customer = user.User(user_data)
            products.append(selected_product)
        return products
    
    @classmethod
    def get_by_id(cls, data):
        query="""
        SELECT * FROM products
        JOIN users on products.user_id = users.id
        WHERE products.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)

        if not results:
            return False
        selected_product = cls(results[0])

        user_data = {
                "id":results[0]["users.id"],
                "first_name":results[0]["first_name"],
                "last_name":results[0]["last_name"],
                "email":results[0]["email"],
                "password":results[0]["password"],
                "is_admin":results[0]["is_admin"],
                "created_at":results[0]["users.created_at"],
                "updated_at":results[0]["users.updated_at"]
            }
        
        selected_product.customer = user.User(user_data)
        return selected_product
    
    @classmethod
    def delete_product(cls,data):
        query="""
        DELETE FROM products 
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update_product(cls, data):
        query="""
        UPDATE products
        SET price=%(price)s, product_name=%(product_name)s, product_image=%(product_image)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_product_id_for_cart(cls, data):
        query= """
        SELECT * FROM products
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        print("In model")
        print(results)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_products(cls):
        query = """
        SELECT * FROM products;
        """
        results = connectToMySQL(cls.db).query_db(query)

        all_products = []

        for user in results:
            all_products.append(cls(user))
        return all_products


    @staticmethod
    def products_validation(data):
        is_valid = True
        if len(data["product_name"]) == 0:
            is_valid = False
            flash("Product name cannot be left empty.", "product")
        if len(data["product_image"]) == 0:
            is_valid = False
            flash("Image must be uploaded.", "product")
        if len(data["price"]) == 0:
            is_valid = False
            flash("Price field cannot be left empty", "product")
        elif int(data["price"]) < 1:
            is_valid = False
            flash("price must be a minimum of $1.", "product")
        return is_valid
