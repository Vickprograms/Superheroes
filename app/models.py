from . import db
from sqlalchemy.orm import validates

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    hero_powers = db.relationship("HeroPower", backref="hero", cascade="all, delete")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "super_name": self.super_name}

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    hero_powers = db.relationship("HeroPower", backref="power", cascade="all, delete")

    @validates("description")
    def validate_description(self, key, value):
        if not value or len(value) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return value

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey("hero.id"))
    power_id = db.Column(db.Integer, db.ForeignKey("power.id"))

    @validates("strength")
    def validate_strength(self, key, value):
        if value not in ["Strong", "Average", "Weak"]:
            raise ValueError("Strength must be 'Strong', 'Average', or 'Weak'")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "strength": self.strength,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "hero": self.hero.to_dict(),
            "power": self.power.to_dict()
        }
