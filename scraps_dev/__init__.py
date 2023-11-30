from flask import (
    Flask,
    render_template,
)
from flask_session import Session

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config["SESSION_TYPE"] = "filesystem"
    app.secret_key = "test_key"
    Session(app)

    @app.route("/")
    def index():
        return render_template("home.html")

    @app.route("/home")
    def home():
        return render_template("home.html")

    from . import auth, recipe, profile, search

    app.register_blueprint(auth.bp)
    app.register_blueprint(recipe.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(search.bp)

    return app
