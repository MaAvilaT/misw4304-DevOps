import logging
import os
import sys

# Add the root directory of the project to PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from blueprints.msvc_email_blacklists import email_blacklists_blueprint
from blueprints.msvc_management import management_blueprint
from database.declarative_base import Base, engine

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.register_blueprint(management_blueprint)
app.register_blueprint(email_blacklists_blueprint)

try:
    app.logger.info('Creating tables')
    Base.metadata.create_all(engine)
except Exception as e:
    app.logger.error(f'Failed to create tables {e}', exc_info=True)

app.logger.info('Tables created')

@app.route('/')
def hello():
    app.logger.info('Hello, world!')
    return 'Hello, world!'


if __name__ == "__main__":
    app.logger.info('Starting the app')
    app.run(host='0.0.0.0', port=5000, debug=True)
