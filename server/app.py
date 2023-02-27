#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return jsonify(plants), 200

    def post(self):
        data = request.get_json()
        new_plant = Plant(**data)
        db.session.add(new_plant)
        db.session.commit()
        return new_plant.to_dict(), 201


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first_or_404()
        return plant.to_dict(), 200

    def patch(self, id):
        plant = Plant.query.filter_by(id=id).first_or_404()
        data = request.get_json()
        for attr, value in data.items():
            setattr(plant, attr, value)
        db.session.commit()
        return plant.to_dict(), 200

    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first_or_404()
        db.session.delete(plant)
        db.session.commit()
        return '', 204


api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
