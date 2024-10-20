from dotenv import load_dotenv
from flask import Flask
from .blueprints.msvc_management import management_blueprint
from .blueprints.msvc_email_blacklists import email_blacklists_blueprint
from .database.declarative_base import Base, engine

loaded = load_dotenv('.env.development')
app = Flask(__name__)

app.register_blueprint(management_blueprint)
app.register_blueprint(email_blacklists_blueprint)

Base.metadata.create_all(engine)