from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    username: str

class Comment(BaseModel):
    id: int
    body: str
    created_at: datetime
    author: User

class Game(BaseModel):
    id: int
    name: str

class Post(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
    author: User
    game: Optional[Game] = None
    comments: List[Comment] = []

class NewPost(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    body: str = Field(min_length=5)
    game_id: int



USERS = [
    {"id": 1, "username": "adam"},
    {"id": 2, "username": "ola"},
    {"id": 3, "username": "kasia"},
    {
        "id": 4,
        "username": "John",
        "password": "doe"
    }
]

POSTS = [
    {
        "id": 1,
        "title": "Pierwszy wpis",
        "body": "To jest treść mojego pierwszego posta!",
        "created_at": datetime(2025, 9, 19, 14, 35).isoformat(),
        "author": USERS[0],
        "game": {
            "name": "Carcasone",
            "id": 2,
        },
        "comments": [
            {
                "id": 1,
                "body": "Super post! 👏",
                "created_at": datetime(2025, 9, 19, 15, 00).isoformat(),
                "author": USERS[1],
            }
        ],
    },
    {
        "id": 2,
        "title": "Drugi wpis",
        "body": "Trochę krótszy post testowy",
        "created_at": datetime(2025, 9, 19, 16, 10).isoformat(),
        "author": USERS[2],
        "comments": [],
        "game": None
    }
]


def fetch_posts():
    return [Post.model_validate(p) for p in POSTS]

def fetch_post(post_id: int):
    return [Post.model_validate(p) for p in POSTS if p['id'] == post_id][0]

def add_post(post: NewPost):
    POSTS.append(
        Post(
            id= len(POSTS)+1,
            title=post.title,
            body=post.body,
            created_at=datetime(2025, 9, 19, 16, 10).isoformat(),
            author= USERS[2],
        ).model_dump()
    )


def add_user(username: str, passwd: str) -> bool:
    user = [user for user in USERS if user['username'] == username]
    if len(user) == 0:
        USERS.append({
            "id": len(USERS)+1,
            "username": username,
            "password": passwd
        })
        return True
    return False

def check_user(username: str, password: str) -> bool:

    user = [user for user in USERS if user['username'] == username]
    if len(user) != 0:
        if user[0]['password'] == password:
            return True
    return False

def add_comment(post_id: int, comment_content: str, user: str) -> bool:
    post = fetch_post(post_id)
    # user = [user for user in USERS if user['username'] == user][0]
    comment = Comment(
        id=len(post.comments)+1,
        body=comment_content,
        created_at=datetime.now().isoformat(),
        author=User(
            id=1,
            username=user
        )
    )
    POSTS[post_id-1]['comments'].append(comment.model_dump())
    print(POSTS)
    return True
