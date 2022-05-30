from flask import request, Blueprint
from flask_restful import Api, Resource

from .schemas import FilmSchema
from ..models import Film, Actor

films_v1_0_bp = Blueprint('films_v1_0_bp', __name__)

films_schema = FilmSchema()

api = Api(films_v1_0_bp)


class FilmListResource(Resource):
    def get(self):
        films = Film.get_all()
        result = films_schema.dump(films, many=True)
        return result

    def post(self):
        data = request.get_json()
        film_dict = films_schema.load(data)
        film = Film(
            title=film_dict['title'],
            length=film_dict['length'],
            year=film_dict['year'],
            director=film_dict['director']
        )

        for actor in film_dict['actors']:
            film.actor.append(Actor(actor['name']))

        film.save()
        resp = films_schema.dump(film)
        return resp, 201


class FilmResource(Resource):
    def get(self, film_id):
        film = Film.get_by_id(film_id)
        resp = films_schema.dump(film)
        return resp


api.add_resource(FilmListResource, '/api/v1.0/films/',
                 endpoint='film_list_resource')
api.add_resource(FilmResource, '/api/v1.0/films/<int:film_id>',
                 endpoint='film_resource')
