from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=True)

    def __init__(self, make, model, price, description, img_url):
        self.make = make
        self.model = model
        self.price = price
        self.description = description
        self.img_url = img_url

class CarSchema(ma.Schema):
    class Meta:
        fields = ("id", "make",  "model", "price", "description", "img_url")

car_schema = CarSchema()
cars_schema = CarSchema(many=True)

@app.route("/car-add", methods=["POST"])
def add_car():
    make = request.json.get("make") 
    model = request.json.get("model")
    price = request.json.get("price")
    description = request.json.get("description")
    img_url = request.json.get("img_url")

    record = Cars(make, model, price, description, img_url)
    db.session.add(record)
    db.session.commit()

    return jsonify(car_schema.dump(record))

@app.route("/car/get", methods=["GET"])
def get_all_cars():
    all_cars = Cars.query.all()
    return jsonify(cars_schema.dump(all_cars))

@app.route("/car/<id>", methods=["DELETE","GET","PUT"])
def car_id(id):
    car = cars.query.get(id)
    if request.method == "DELETE":
        db.session.delete(car)
        db.session.commit()
    
        return cars_schema.jsonify(car)
    elif request.method == "PUT":
        make = request.json['make']
        model = request.json['model']
        price = request.json['price']
        description = request.json['description']
        img_url = request.json['img_url']

        car.make = make
        car.model = model
        car.price = price
        car.description = description
        car.img_url = img_url

        db.session.commit()
        return car_schema.jsonify(car)
    elif request.method == "GET":
        return car_schema.jsonify(car)


if __name__ == "__main__":
    app.run(debug=True)
    