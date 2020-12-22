from typing import Optional

import dbm
import os.path

from server.schema.user import User, user_schema

USERNAME_PREFIX = 'username_'

DB_STORE_PATH = os.path.expanduser('~/db')
DB_NAME = 'user.db'
DB_ABS_PATH = os.path.join(DB_STORE_PATH, DB_NAME)


class UserDB:
    """
    A singleton meant to be instantiated at server startup that stores user data models.
    """
    def __init__(self):
        if not os.path.isdir(DB_STORE_PATH):
            print('DB store path not present, mkdir...')
            os.mkdir(DB_STORE_PATH)

        # Open DB file for read/write, create new file if not already present.
        # Uses "sync" mode so all writes are flushed to disk.
        self._store = dbm.open(DB_ABS_PATH, flag='cs')

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Returns a User object if present in the DB, otherwise returns None.
        """
        user_id = self._store.get(USERNAME_PREFIX + username)
        if user_id is None:
            return None

        return self.get_by_id(user_id)

    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Returns a User object if present in the DB, otherwise returns None.

        Assumes all items in the DB are valid.
        """
        data = self._store.get(user_id)
        if data is None:
            return None

        return user_schema.loads(data)

    def store_user(self, user: User) -> None:
        """
        Store a User object in the DB, overwriting the existing item if present.
        """
        # Save a JSON serialization of the User object.
        self._store[user.user_id] = user_schema.dumps(user)

    def add_dream_to_user(self, user_id: str, dream_id: str) -> None:
        """
        Associate the provided dream_id with the user_id.
        """
        user = self.get_by_id(user_id)
        if user is None:
            return

        user.dream_ids.append(dream_id)
        self.store_user(user)


# This is the instance that callers should import and interact with.
user_db = UserDB()
