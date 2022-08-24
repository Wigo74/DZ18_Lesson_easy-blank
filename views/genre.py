from flask_restx import Resource, Namespace
from flask import request
from marshmallow import schema
from models import Genre, GenreSchema
from setup_db import db


genre_ns = Namespace('genre')
genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


@genre_ns.route("/")
class GenresView(Resource):
    def get(self):
        genres = db.session.query(Genre).all()
        return genres_schema.dump(genres)


@genre_ns.route("/<int:genre_id>")
class GenreView(Resource):
    def get(self, genre_id):
        genre = db.session.query(Genre).filter(Genre.id == genre_id).first()
        if not genre:
            return "", 400

        return genre_schema.dump(genre), 200