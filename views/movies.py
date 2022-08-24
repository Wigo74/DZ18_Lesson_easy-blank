# здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки). сюда импортируются сервисы из пакета service

# Пример
from flask import request
from flask_restx import Resource, Namespace
from setup_db import db
from models import Movies, MoviesSchema

movie_ns = Namespace('movies')
movies_schema = MoviesSchema(many=True)
movie_schema = MoviesSchema()


@movie_ns.route("/")
class MoviesView(Resource):
    @movie_ns.response(201, description='Возвращает все фильмы или по ID режиссера или по ID жанра или по обоим ID')
    def get(self):
        movies_query = db.session.query(Movies)
        args = request.args
        director_id = args.get('director_id')
        if director_id is not None:
            movies_query = movies_query.filter(Movies.director_id == director_id)
        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies_query = movies_query.filter(Movies.genre_id == genre_id)
        movies = movies_query.all()
        return movies_schema.dump(movies)

    @movie_ns.response(201, description='Добавляет кино в фильмотеку')
    def post(self):
        movie = movie_schema.load(request.json)
        db.session.add(Movies(**movie))
        db.session.commit()
        return None, 201


@movie_ns.route("/<int:bid>")
class MovieView(Resource):
    @movie_ns.response(200, description='Возвращает фильм по его ID')
    @movie_ns.response(404, description='Фильм не найден')
    def get(self, bid: int):
        movie = db.session.query(Movies).get(bid)
        if not movie:
            return "", 400

        return movie_schema.dump(movie), 200

    @movie_ns.response(204, description='Перезаписывает значения по ID фильма')
    def put(self, bid: int):
        db.session.query(Movies).filter(Movies.id == bid).update(request.json)
        db.session.commit()
        return None, 204

    @movie_ns.response(204, description='Удаляет по ID фильма')
    def delete (self, bid: int):
        db.session.query(Movies).filter(Movies.id == bid).delete()
        db.session.commit()
        return None, 204


