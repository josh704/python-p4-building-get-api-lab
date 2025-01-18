#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return jsonify(bakeries), 200

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    bakery_data = bakery.to_dict()
    bakery_data['baked_goods'] = [good.to_dict() for good in bakery.baked_goods]

    return jsonify(bakery_data), 200
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([good.to_dict() for good in baked_goods]), 200

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive_good:
        return jsonify(most_expensive_good.to_dict()), 200
    else:
        return jsonify({'error': 'No baked goods found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
