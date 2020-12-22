from typing import Optional, List

from server.schema.dream import Dream
from server.schema.user import User
from server.db.dream import dream_db
from server.db.user import user_db


class UserService:
    def __init__(self):
        pass

    def get_or_create_if_valid_login(self, username: str, password: str) -> Optional[User]:
        """
        If a User with this username exists, validate the password, if no user already
        exists, then create a new one. Return the User object as long as the account
        if new OR existing and the password is valid. Otherwise return None.
        """
        user = user_db.get_by_username(username)
        if user is None:
            user = User(name=username, password=password)
            user_db.store_user(user)

        if not user.valid_password(password):
            return None

        return user

    def get_dreams(self, user_id: str) -> List[Dream]:
        """
        Return all of the user's dreams.
        """
        res: List[Dream] = []
        user = user_db.get_by_id(user_id)
        if user is None:
            return res

        for dream_id in user.dream_ids:
            dream = dream_db.get_by_id(dream_id)
            if dream is not None:
                res.append(dream)

        return res


# This is the instance that callers should import and interact with.
user_service = UserService()
