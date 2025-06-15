from flask import Blueprint, request, jsonify
from .models import db, Hero, Power, HeroPower

bp = Blueprint("api", __name__)

@bp.route("/heroes")
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

@bp.route("/heroes/<int:id>")
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    result = hero.to_dict()
    result["hero_powers"] = [hp.to_dict() for hp in hero.hero_powers]
    return jsonify(result)

@bp.route("/powers")
def get_powers():
    return jsonify([p.to_dict() for p in Power.query.all()])

@bp.route("/powers/<int:id>", methods=["GET", "PATCH"])
def power_details(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    if request.method == "PATCH":
        try:
            data = request.get_json()
            power.description = data.get("description", power.description)
            db.session.commit()
            return jsonify(power.to_dict())
        except:
            return jsonify({"errors": ["validation errors"]}), 400
    return jsonify(power.to_dict())

@bp.route("/hero_powers", methods=["POST"])
def create_hero_power():
    data = request.get_json()
    try:
        new_hp = HeroPower(
            strength=data["strength"],
            hero_id=data["hero_id"],
            power_id=data["power_id"]
        )
        db.session.add(new_hp)
        db.session.commit()
        return jsonify(new_hp.to_dict()), 201
    except:
        return jsonify({"errors": ["validation errors"]}), 400
