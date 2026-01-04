from db import db
from sqlalchemy.orm import validates


class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    def to_dict(self, fields=None, include_hero_powers=False):
        if fields:
            return {f: getattr(self, f) for f in fields}
        data = {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name
        }
        if include_hero_powers:
            data['hero_powers'] = [hp.to_dict(include_power=True) for hp in self.hero_powers]
        return data


class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.errors = []

    @validates('description')
    def validate_description(self, key, description):
        self.errors = []
        if description is None or len(description.strip()) < 20:
            self.errors.append('description must be at least 20 characters')
            raise ValueError('description validation failed')
        return description

    def to_dict(self, fields=None):
        if fields:
            return {f: getattr(self, f) for f in fields}
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    strength = db.Column(db.String, nullable=False)

    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    VALID_STRENGTHS = ('Strong', 'Weak', 'Average')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.errors = []

    @validates('strength')
    def validate_strength(self, key, strength):
        self.errors = []
        if strength not in self.VALID_STRENGTHS:
            self.errors.append(f"strength must be one of: {', '.join(self.VALID_STRENGTHS)}")
            raise ValueError('strength validation failed')
        return strength

    def to_dict(self, include_power=False, include_hero=False, include_related=False):
        data = {
            'id': self.id,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'strength': self.strength
        }
        if include_power or include_related:
            data['power'] = self.power.to_dict()
        if include_hero or include_related:
            data['hero'] = self.hero.to_dict()
        return data
