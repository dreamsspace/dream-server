from typing import List

from uuid import uuid4

from marshmallow import Schema, fields, post_load


class User:
    """
    Type for user data storage and linking to dreams.
    """
    def __init__(self, name: str):
        self.name: str = name
        self.user_id: str = str(uuid4())
        self.dream_ids: List[str] = []


class UserSchema(Schema):
    name = fields.Str()
    user_id = fields.Str()
    dream_ids = fields.List(fields.Str())

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


user_schema = UserSchema()
