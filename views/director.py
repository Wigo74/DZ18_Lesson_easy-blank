from flask_restx import Resource, Namespace
from setup_db import db
from models import DirectorSchema, Director

director_ns = Namespace('director')
directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()



@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        directors = db.session.query(Director).all()
        return directors_schema.dump(directors)


@director_ns.route("/<int:director_id>")
class DirectorView(Resource):
    def get(self, director_id):
        director = db.session.query(Director).filter(Director.id == director_id).first()
        if not director:
            return "", 400

        return director_schema.dump(director), 200
