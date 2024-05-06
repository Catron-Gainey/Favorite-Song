from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Song:
    dB = "favorite_song"
    
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.network = data["network"]
        self.release_date = data["release_date"]
        self.comments = data["comments"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # 'None' represents empty space for single user dict
        # song is made by one user
        self.viewer = None
        
        
    # CREATE
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO songs (user_id, title, network, release_date, comments)
            VALUES (%(user_id)s, %(title)s, %(network)s, %(release_date)s, %(comments)s);
        """
        results = connectToMySQL(cls.dB).query_db(query, data)
        return results
        
    # READ
    # get all the user's songs
    @classmethod
    def get_all_songs_with_user(cls):
        query = """
            SELECT *
            FROM songs
            LEFT JOIN users
            ON songs.user_id = users.id;
        """
        results = connectToMySQL(cls.dB).query_db(query)
        all_songs = []
        for row_data in results:
            # create song cls instance from info from each row_data
            one_song = cls(row_data)
            one_song_with_viewer_info = {
                "id": row_data["users.id"],
                "first_name": row_data["first_name"],
                "last_name": row_data["last_name"],
                "email": row_data["email"],
                "password": row_data["password"],
                "created_at": row_data["users.created_at"],
                "updated_at": row_data["users.updated_at"],
            }
            # create user cls instance that is in the user.py model
            owner = user.User(one_song_with_viewer_info)
            one_song.viewer = owner
            all_songs.append(one_song)
        return all_songs
    
    # UPDATE
    @classmethod
    def update(cls, data):
        query = """
            UPDATE songs
            SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, comments = %(comments)s
            WHERE id = %(song_id)s;
        """
        results = connectToMySQL(cls.dB).query_db(query, data)
        return results
    
    # DELETE
    @classmethod
    def destroy_by_song_id(cls, song_id):
        query = """
            DELETE FROM songs
            WHERE id = %(id)s;
        """
        data = {
            "id": song_id
        }
        results = connectToMySQL(cls.dB).query_db(query, data)
        return results
    
    # VALIDATE
    @staticmethod
    def validate_song_info(data):
        
        is_valid = True
        
        if len(data["title"].strip()) == 0 and len(data["network"].strip()) == 0 and len(data["release_date"]) == 0 and len(data["comments"].strip()) == 0:
            flash("All fields required.", "song_info")
            is_valid = False
            return is_valid
            
        if len(data["title"].strip()) < 3:
            flash("Title must be at least 3 characters long.", "song_info")
            is_valid = False
            
        if len(data["network"].strip()) < 3:
            flash("Network name must be at least 3 characters long.", "song_info")
            is_valid = False
            
        if len(data["comments"].strip()) < 3:
            flash("Comments must be at least 3 characters long.", "song_info")
            is_valid = False
            
        if len(data["release_date"]) == 0:
            flash("Release date must be filled.", "song_info")
            is_valid = False
        
        return is_valid
