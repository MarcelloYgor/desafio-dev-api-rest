import connexion
from connexion.resolver import RestyResolver

from dao.db import db
from model import models

from config import TestingConfig

app = connexion.FlaskApp(__name__, specification_dir='./swagger/')

webapp = app.app

webapp.config.from_object(TestingConfig())

db.init_app(webapp)

with webapp.app_context():
    db.create_all()

app.add_api('dock_digital.yaml', resolver=RestyResolver('api'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
