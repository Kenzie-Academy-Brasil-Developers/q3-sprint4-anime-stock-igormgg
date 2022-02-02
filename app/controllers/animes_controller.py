from flask import jsonify, request

from app.models.anime_model import Anime
from psycopg2.errors import UniqueViolation, UndefinedTable

def animes():
    animes = Anime.read_animes()

    animes_list = Anime.serialize_anime(animes)

    return {"data": animes_list}, 200

def select_by_id(anime_id):
    try:
        anime = Anime.anime_by_id(anime_id)

        anime = Anime.serialize_anime(anime)

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
        return jsonify({'error': 'anime already exists'}), 409
    
    except KeyError as k:
        return {
            "available_keys": Anime.available_keys,
            "wrong_keys_sent": wrong_keys_sent
        }, 422

    inserted_anime = Anime.serialize_anime(inserted_anime)

    return jsonify(inserted_anime), 201

def update(anime_id):
    try:
        existing_ids = []
        for anms in animes()[0].get("data"):
            existing_ids.append(anms.get("id"))
        if anime_id not in existing_ids:
            raise TypeError

        data = request.get_json()

        wrong_keys_sent = list(set(data.keys() - Anime.available_keys))

        data['anime'] = data['anime'].title()

        updated_anime = Anime.update_anime(anime_id, data)

    except KeyError as k:
        return {
            "available_keys": Anime.available_keys,
            "wrong_keys_sent": wrong_keys_sent
        }, 422
    
    except (TypeError, UndefinedTable):
        return {"error": "Not Found"}, 404
    
    except UniqueViolation:
        return jsonify({'error': 'anime already exists'}), 409
    
    patched_anime = Anime.serialize_anime(updated_anime)

    return jsonify(patched_anime), 200

def delete(anime_id):
    try:
        existing_ids = []
        for anms in animes()[0].get("data"):
            existing_ids.append(anms.get("id"))

        if anime_id not in existing_ids:
            print('anime_id not in existing_ids')
            raise TypeError

        Anime.delete_anime(anime_id)

        return {}, 204
    
    except (TypeError, UndefinedTable):
        return {"error": "Not Found"}, 404