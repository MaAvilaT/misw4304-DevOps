from dotenv import load_dotenv
from flask import Flask

from .blueprints.msvc_email_blacklists import email_blacklists_blueprint
from .blueprints.msvc_management import management_blueprint
from .database.declarative_base import Base, engine

loaded = load_dotenv('.env.development')
application = Flask(__name__)

application.register_blueprint(management_blueprint)
application.register_blueprint(email_blacklists_blueprint)

Base.metadata.create_all(engine)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=True)
