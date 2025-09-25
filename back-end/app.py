from flask import Flask
from flask_restful import Api
from database import init_db
from resources.posts import *
from resources.auth import *
app = Flask(__name__)
api = Api(app)

init_db()

api.add_resource(RegisterUser, "/auth/register")
api.add_resource(LoginUser, "/auth/login")
api.add_resource(PostList, "/posts")

if __name__ == "__main__":
    app.run(debug=True)