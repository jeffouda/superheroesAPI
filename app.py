from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
from flask_mail import Mail, Message

# Configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///superhero.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Flask mail configuration
app.config["MAIL_SERVER"] = "localhost"
app.config["MAIL_PORT"] = 2525
app.config["MAIL_USERNAME"] = None
app.config["MAIL_PASSWORD"] = None
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = False



mail = Mail(app)

# initialize migration and database
migrate = Migrate(app, db)
db.init_app(app)

# Routes


@app.route("/")
def index():
    return "<hi>Superheroes API</h1>"


# GET /heroes -> returns a list of heroes


@app.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()
    heroes_dict = [hero.to_dict(rules=("-hero_powers",)) for hero in heroes]
    return make_response(jsonify(heroes_dict), 200)


# GET /heroes/:id -> returns a specific hero with their powers
@app.route("/heroes/<int:id>", methods=["GET"])
def get_hero_by_id(id):
    hero = Hero.query.filter_by(id=id).first()

    if not hero:
        return make_response(jsonify({"error": "Hero not found"}), 404)
    return make_response(jsonify(hero.to_dict()), 200)


# GET /powers -> returns a list of power
@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    powers_dict = [p.to_dict(rules=("-hero_powers",)) for p in powers]
    return make_response(jsonify(powers_dict), 200)


# GET /powers/:id -> returns a specific power
@app.route("/powers/<int:id>", methods=["GET"])
def get_power_by_id(id):
    power = Power.query.filter_by(id=id).first()

    if not power:
        return make_response(jsonify({"error": "Power not found"}), 404)

    return make_response(jsonify(power.to_dict(rules=("-hero_powers",))), 200)


# Patch /powers/:id -> updating an existing power's description
@app.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):
    power = Power.query.filter_by(id=id).first()

    if not power:
        return make_response(jsonify({"error": "Power not found"}), 404)

    data = request.get_json()

    try:
        # Update the description
        if "description" in data:
            power.description = data["description"]

        db.session.add(power)
        db.session.commit()

        return make_response(jsonify(power.to_dict(rules=("-hero_powers",))), 200)

    except ValueError:
        return make_response(jsonify({"error": ["validation errors"]}), 400)


# Post /hero_powers -> creates new relationship between a Hero and a power
@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    data = request.get_json()

    try:
        new_hp = HeroPower(
            strength=data["strength"],
            power_id=data["power_id"],
            hero_id=data["hero_id"],
        )

        db.session.add(new_hp)
        db.session.commit()
        return make_response(jsonify(new_hp.to_dict()), 200)

    except ValueError:
        return make_response(jsonify({"errors": ["validation errors"]}), 400)
    except Exception:
        return make_response(jsonify({"errors": ["validation errors"]}), 400)


# Email Route -> A simple route to prove the app can "send" email.
@app.route("/send_email", methods=["GET"])
def send_test_email():
    msg = Message(
        "Hello from Superheroes API",
        sender="noreply@superheroes.com",
        recipients=["test@example.com"],
    )
    msg.body = "This is a test email from the Superheroes API."

    try:
        mail.send(msg)
        return make_response(jsonify({"message": "Email sent successfully!"}), 200)

    except Exception:
        # we print to console.
        print(
            f"\n SIMULATED EMAIL SENT:\n-------------------------\nTo: test@example.com\nSubject: Hello from Superheroes API\nBody: {msg.body}\n-------------------------\n"
        )
        return make_response(
            jsonify({"message": "Email sent successfully (simulated mode)!"}), 200
        )


if __name__ == "__main__":
    app.run(debug=True)
