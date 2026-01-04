from flask import Flask, jsonify, request
from flask_migrate import Migrate
import os
from db import db

app = Flask(__name__)

# config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'development.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    # import models after db is configured to avoid circular imports
    from models import Hero, Power, HeroPower


@app.route('/heroes')
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([h.to_dict(fields=('id','name','super_name')) for h in heroes])


@app.route('/heroes/<int:hero_id>')
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify(hero.to_dict(include_hero_powers=True))


@app.route('/powers')
def get_powers():
    powers = Power.query.all()
    return jsonify([p.to_dict() for p in powers])


@app.route('/powers/<int:power_id>')
def get_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict())


@app.route('/powers/<int:power_id>', methods=['PATCH'])
def patch_power(power_id):
    power = Power.query.get(power_id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    data = request.get_json() or {}
    description = data.get('description')
    if description is None:
        return jsonify({"errors": ["description is required"]}), 400
    try:
        power.description = description
        db.session.add(power)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        errs = getattr(power, 'errors', None) or [str(e)]
        return jsonify({"errors": errs}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["unexpected error"]}), 500
    return jsonify(power.to_dict())


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json() or {}
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')
    try:
        hp = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)
        db.session.add(hp)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        errs = getattr(hp, 'errors', None) if 'hp' in locals() else None
        errs = errs or [str(e)]
        return jsonify({"errors": errs}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["unexpected error"]}), 500

    # return as specified
    return jsonify(hp.to_dict(include_related=True)), 201


if __name__ == '__main__':
    app.run(debug=True)
