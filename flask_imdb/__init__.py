from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = {'DB': "imdb"}

# defining the mongoeninge orm
db = MongoEngine(app)

def register_blueprints(app):
    # prevents circular imports
    from flask_imdb.views import movies 

    # in case more than one application working with movies exists
    # define url_prefix for each of them, e.g. url_prefix="/imdb"
    app.register_blueprint(movies)

register_blueprints(app)

if __name__ == '__main__':
        app.run()
