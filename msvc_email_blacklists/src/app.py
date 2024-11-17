import os
import sys

# Add the root directory of the project to PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from blueprints.msvc_email_blacklists import email_blacklists_blueprint
from blueprints.msvc_management import management_blueprint
from database.declarative_base import Base, engine

app = Flask(__name__)

app.register_blueprint(management_blueprint)
app.register_blueprint(email_blacklists_blueprint)

Base.metadata.create_all(engine)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
