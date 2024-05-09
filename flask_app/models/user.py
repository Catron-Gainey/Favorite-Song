from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import song
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    dB = "favorite_song"
    
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.fav_song = []
        
    #! Create
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        result = connectToMySQL(cls.dB).query_db(query, data)
        return result
    
    #! Read
    # get user by email
    @classmethod
    def get_by_email(cls, user_email):
        query = """
            SELECT *
            FROM users
            WHERE email = %(email)s; 
        """
        data = {
            "email": user_email
        }
        user_data = connectToMySQL(cls.dB).query_db(query, data)
        
        if len(user_data) < 1:
            return False
        return cls(user_data[0])
    
    # get user by id
    @classmethod
    def get_by_id(cls, user_id):
        query = """
            SELECT *
            FROM users
            WHERE id = %(id)s;
        """
        data = {
            "id": user_id
        }
        user_data = connectToMySQL(cls.dB).query_db(query, data)
        return cls(user_data[0])
    
    # view one - get user with song
    @classmethod
    def get_user_with_song(cls, song_id):
        query = """
            SELECT *
            FROM users
            LEFT JOIN songs
            ON users.id = songs.user_id
            WHERE songs.id = %(song_id)s;
        """
        data = {
            "song_id": song_id
        }
        user_from_db = connectToMySQL(cls.dB).query_db(query, data)
        user = cls(user_from_db[0])
        
        # connect primary key to foreign key
        for row_data in user_from_db:
            song_info = {
                "id": row_data["songs.id"],
                "title": row_data["title"],
                "artist": row_data["artist"],
                "created_at": row_data["songs.created_at"],
                "updated_at": row_data["songs.updated_at"],
            }
            user.fav_song.append(song.Song(song_info))
        return user
    
    #! Validations
    # validate reg
    @staticmethod
    def validate_register(data):
        is_valid = True
        
        if len(data["email"].strip()) == 0 and len(data["first_name"].strip()) == 0 and len(data["last_name"].strip()) == 0 and len(data["password"].strip()) == 0:
            flash("All fields required.", "register")
            is_valid = False
            return is_valid
        
        if len(data["email"].strip()) == 0:
            flash("Please enter an email address.", "register")
            is_valid = False
            
        # test if email matches format
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email format.", "register")
            is_valid = False
            
        # fn - letters only, at least 2 characters
        if len(data["first_name"].strip()) == 0:
            flash("First name cannot be left blank.", "register")
            is_valid = False
            
        elif len(data["first_name"].strip()) < 2:
            flash("First name must be at least 2 characters long.", "register")
            is_valid = False
            
        elif data["first_name"].isalpha() == False:
            flash("First name must consist of characters only.", "register")
            is_valid = False
            
        # ln - letters only, at least 2 characters
        if len(data["last_name"].strip()) == 0:
            flash("Last name cannot be left blank.", "register")
            is_valid = False
            
        elif len(data["last_name"].strip()) < 2:
            flash("Last name must be at least 2 characters long.", "register")
            is_valid = False
            
        elif data["last_name"].isalpha() == False:
            flash("Last name must consist of characters only.", "register")
            is_valid = False
            
        # password - at least 8 characters
        if len(data["password"].strip()) == 0:
            flash("Password must be filled out.", "register")
            is_valid = False
            
        elif len(data["password"].strip()) < 8:
            flash("Password must be at least 8 characters long.", "register")
            is_valid = False
            
        # pw and confirm_pw match
        if data["password"] != data["confirm_pw"]:
            flash("Password does not match.", "register")
            is_valid = False
            
        return is_valid
    
    # validate login
    @staticmethod
    def validate_login(data):
        is_valid = True
        
        if len(data["email"].strip()) == 0 and len(data["password"].strip()) == 0:
            flash("All fields required.", "login")
            is_valid = False
            return is_valid
        
        if len(data["email"].strip()) == 0:
            flash("Please enter an email address.", "login")
            is_valid = False
            
        # test if email matches format
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email format.", "login")
            is_valid = False
            
        if not User.get_by_email(data["email"]):
            flash("Invalid email/password.", "login")
            is_valid = False
            
        if len(data["password"].strip()) == 0:
            flash("Password must be filled out.", "login")
            is_valid = False
            
        return is_valid