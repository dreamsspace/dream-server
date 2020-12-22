from typing import List, Optional

import os
import hashlib
from uuid import uuid4

from marshmallow import Schema, fields, post_load


def gen_key(password: str, salt: str) -> str:
    """
    Generate a secure key from the provided password and salt.

    This is used both during key derivation and during validation.
    """
    return hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), bytes.fromhex(salt), 100000, dklen=128).hex()


class User:
    """
    Type for user data storage and linking to dreams.
    """
    def __init__(
        self, name: str,
        user_id: Optional[str] = None,
        dream_ids: Optional[List[str]] = None,
        password: Optional[str] = None,
        salt: Optional[str] = None,
        hashed_password: Optional[str] = None,
    ):
        self.name: str = name

        if user_id is None:
            self.user_id: str = str(uuid4())
        else:
            self.user_id = user_id

        if dream_ids is None:
            self.dream_ids: List[str] = []
        else:
            self.dream_ids = dream_ids

        # If there is a hashed_password, then this is an existing
        # user we are deserializing. Otherwise it is a new user and
        # we need to store a new hash and generate a salt.
        if hashed_password is None and password is not None:
            self.salt: str = os.urandom(16).hex()
            self.hashed_password: str = gen_key(password, self.salt)
        elif hashed_password is not None and salt is not None:
            self.salt = salt
            self.hashed_password = hashed_password
        else:
            raise Exception('Invalid User creation')

    def valid_password(self, password: str) -> bool:
        """
        Returns True if the password provided matches the hash stored for the user.
        """
        return gen_key(password, self.salt) == self.hashed_password


class UserSchema(Schema):
    name = fields.Str()
    hashed_password = fields.Str()
    salt = fields.Str()
    user_id = fields.Str()
    dream_ids = fields.List(fields.Str())

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


user_schema = UserSchema()
