from flask import Flask
from flask_restful import Api
from database import init_db
from resources.posts import *
from resources.auth import *
from resources.game import *

from settings import JWT_KEY
from flask_jwt_extended import JWTManager
app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = JWT_KEY
jwt = JWTManager(app)

init_db()

api.add_resource(RegisterUser, "/auth/register")
api.add_resource(LoginUser, "/auth/login")
api.add_resource(PostList, "/posts")
api.add_resource(PostDetails, "/posts/<int:post_id>")  # GET szczegóły posta
api.add_resource(PostComments, "/posts/<int:post_id>/comments")
api.add_resource(GameList, "/games",'/games/<int:game_id>')


if __name__ == "__main__":
    app.run(debug=True)