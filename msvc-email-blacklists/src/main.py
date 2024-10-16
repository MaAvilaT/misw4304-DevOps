from dotenv import load_dotenv
from flask import Flask, jsonify
from .blueprints.msvc_management import management_blueprint
from .blueprints.post_management import posts_blueprint
from .database.declarative_base import Base, engine
from .errors.errors import ApiError

loaded = load_dotenv('.env.development')
app = Flask(__name__)

app.register_blueprint(management_blueprint)
app.register_blueprint(posts_blueprint)

Base.metadata.create_all(engine)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "msg": err.description
    }
    return jsonify(response), err.code