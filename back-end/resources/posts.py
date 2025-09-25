from flask_restful import Resource, request
from database import SessionLocal
import models
from datetime import date
from marshmallow import Schema, fields
from marshmallow import ValidationError




class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()

class CommentsSchema(Schema):
    id = fields.Int()
    author = fields.Nested(UserSchema, many=False)
    content = fields.Str()

class PostDetailsSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    body = fields.Str()
    author = fields.Nested(UserSchema, many=False),
    comments = fields.Nested(UserSchema, many=True),
    created_at = fields.Date()

class PostListSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    author = fields.Nested(UserSchema, many=False),
    created_at = fields.Date()



class PostAddSchema(Schema):
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    author_id = fields.Int(required=True)
    game_id = fields.Int()

details_schema = PostDetailsSchema()
post_list_schema = PostListSchema()
post_add_schema = PostAddSchema()

class PostDetails(Resource):
    def get(self, post_id: int):
        session = SessionLocal()
        post = session.query(models.Post).filter(
            models.Post.id == post_id
        ).first()
        session.close()
        if post:
            return details_schema.dump(post), 200
        else:
            return {"message": "Not found"}, 400

class PostList(Resource):
    def get(self):
        session = SessionLocal()
        posts = session.query(models.Post).all()
        session.close()
        return post_list_schema.dump(posts)

    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "Sent empty request"}, 400
        try:
            data = post_add_schema.load(data)
        except ValidationError as error:
            return {"message": "Wrong request"}, 400
        session = SessionLocal()
        new_post = models.Post(
            title=data["title"],
            body=data["body"],
            author_id=data["author_id"],
            game_id=data.get("game_id"),
            created_at=date.today()
        )
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        session.close()
        return {"id": new_post.id, "title": new_post.title}, 201