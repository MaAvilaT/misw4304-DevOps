from flask import Flask

from src.blueprints.msvc_email_blacklists import email_blacklists_blueprint
from src.blueprints.msvc_management import management_blueprint
from src.database.declarative_base import Base, engine

application = Flask(__name__)

application.register_blueprint(management_blueprint)
application.register_blueprint(email_blacklists_blueprint)

Base.metadata.create_all(engine)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=True)
