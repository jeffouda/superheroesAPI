from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlachemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

#Flask-SQLAlachemy to handle Naming COnventions(MetaData)

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

#initialize the database
db = SQLAlchemy(metadata=metadata)

#HERO table 
class Hero(db.Model,SerializerMixin):
    __tablename__ = 'heroes'
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    
    hero_powers = db.relationship('HeroPower',back_populates='hero', cascade='all,delete-orphan')
    
    
    powers = association_proxy('hero_powers','power')
    
    
    serialize_rules = (-hero_powers.hero)
    
    def __repr__(self):
        return f'<Hero {self.name}>'
      
      
#POWER
class Power(db.model,SerializerMixin):
    __tablename__ = 'powers'
    
    id = db.Column(db.Integer,primary_key=True) 
    name = db.Column(db.String)
    description = db.Column(db.String)
    
    #Relationship -> One POwer has many HeroPowers
    hero_powers = db.relationship('HeroPower', back_populates='power',cascade='all,delete-orphan')
    
    #Association Proxy
    heroes = association_proxy('hero_powers','hero')
    
    #Serialization -> prevent recursion
    serialize_rules = ('-hero_powers.power',)
    
    #Validation-> desciption must be present and at least 20 characters
    @validates('description')
    def validate_description(self,key,description):
        if not description:
            raise ValueError('Description must be present')
        if len(description) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return description
      
    def __repr__(self):
        return f'<Power {self.name}>' 
      
#HeroPower (Join Table)
class HeroPower(db.Model, SerializerMixin):
    __tablename__= 'hero_powers'
    
    id = db.Column(db.Integer,primary_key=True)
    strength = db.Column(db.String, nullable=False)
    
    #Foreign Keys -> links to Hero and Power tables
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer,db.ForeignKey('powers.id'))
    
    
    #Relationship -> Connect back to the parent models
    hero = db.relationship('Hero',back_populates='hero_powers')
    power = db.relationship('Power',back_populates='hero_powers')  
    
    #Serialization
    serialize_rules = ('-hero.hero_powers','-power.hero_powers') 
    
    
    #Validation -> Strength must be 'Strong , 'weak', or 'Average
    @validates('strength')
    def validate_strength(self,key, strength):
        valid_strengths = ['Strong' ,'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError(f'Strength must be one of: {','.join(valid_strengths)}') 
        return strength
      
    def __repr__(self):
        return f'<HeroPOwer {self.strength}>'       
                   