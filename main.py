from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

api = Api(app)
migrate = Migrate(app, db)
db.init_app(app)


@app.after_request
def close_request(response):
    db.session.commit()
    return response


[api.add_resource(*route) for route in routes]

if __name__ == "__main__":
    app.run()
