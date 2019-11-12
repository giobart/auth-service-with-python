from flask import Flask
from flask_jwt_extended import JWTManager
from auth.database import DATABASE_NAME, db
from auth.views import blueprints

app = Flask(__name__)


def create_app(database=DATABASE_NAME):
    '''
    Prepares initializes the application and its utilities.
    '''

    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT TOKEN CONFIGURATION
    app.config['SECRET_KEY'] = 'some-secret-string-CHANGE-ME'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-CHANGE-ME'
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/auth/token_refresh'

    # Set True in production environment, False only for debugging purpose
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False

    # Only allow JWT cookies to be sent over https. In production, this
    # should likely be True
    app.config['JWT_COOKIE_SECURE'] = False

    jwt = JWTManager(app)
    db.init_app(app)

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    return app


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app = create_app()
    app.run()
