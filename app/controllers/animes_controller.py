from flask import jsonify, request
from psycopg2.errors import UniqueViolation, UndefinedTable

from app.models.anime_model import Anime

def animes():
    animes = Anime.read_animes()

    animes_keys = ['id', 'anime', 'released_date', 'seasons']

    animes_list = [dict(zip(animes_keys, anime)) for anime in animes]

    return {"data": animes_list}, 200

def select_by_id(anime_id):
    try:
        anime = Anime.anime_by_id(anime_id)

        animes_keys = ['id', 'anime', 'released_date', 'seasons']

        anime = dict(zip(animes_keys, anime))

        return {"data": anime}, 200

    except (TypeError, UndefinedTable):
        return {"error": "Not Found"}, 404

def create():
    data = request.get_json()
    wrong_keys_sent = list(set(data.keys() - Anime.available_keys))

    try:
        data_to_post = {}
        data_to_post['anime'] = data['anime'].title()
        data_to_post['released_date'] = data['released_date']
        data_to_post['seasons'] = data['seasons']

        anime = Anime(**data_to_post)

        inserted_anime = anime.create_anime()
    
    except UniqueViolation:
        return jsonify({'error': 'anime already exists'}), 422
    
    except KeyError as k:
        return {
            "available_keys": Anime.available_keys,
            "wrong_keys_sent": wrong_keys_sent
        }, 422
    
    animes_keys = ['id', 'anime', 'released_date', 'seasons']

    inserted_anime = dict(zip(animes_keys, inserted_anime))

    return jsonify(inserted_anime), 201

