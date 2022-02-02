from flask import request
from app.models import DatabaseConnector

class Anime(DatabaseConnector):
    available_keys = ['anime', 'released_date', 'seasons']

    def __init__(self, *args, **kwargs):
        self.anime = kwargs['anime']
        self.released_date = kwargs['released_date']
        self.seasons = kwargs['seasons']

    @classmethod
    def read_animes(cls):
        cls.get_conn_cur()

        query = "SELECT * FROM animes;"

        cls.cur.execute(query)

        animes = cls.cur.fetchall()

        cls.commit_and_close()

        return animes

    @classmethod
    def anime_by_id(cls, anime_id):
        cls.get_conn_cur_without_table_creation()

        query = "SELECT * FROM animes WHERE id = %s;"

        query_id = str(anime_id)

        cls.cur.execute(query, query_id)

        anime = cls.cur.fetchone()

        cls.commit_and_close()

        return anime

    def create_anime(self):
        self.get_conn_cur()

        query = """
            INSERT INTO
                animes (anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING *
            """
        
        query_values = list(self.__dict__.values())

        self.cur.execute(query, query_values)

        inserted_anime = self.cur.fetchone()

        self.commit_and_close()

        return inserted_anime