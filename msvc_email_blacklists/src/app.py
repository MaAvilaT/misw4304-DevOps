from flask import Flask

from msvc_email_blacklists.src.blueprints.msvc_email_blacklists import email_blacklists_blueprint
from msvc_email_blacklists.src.blueprints.msvc_management import management_blueprint
from msvc_email_blacklists.src.database.declarative_base import Base, engine

app = Flask(__name__)

app.register_blueprint(management_blueprint)
app.register_blueprint(email_blacklists_blueprint)

Base.metadata.create_all(engine)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
