from typing import Optional

import dbm
import os.path

from server.schema.dream import Dream, DreamSurvey, dream_schema


DB_STORE_PATH = os.path.expanduser('~/db')
DB_NAME = 'dream.db'


class DreamDB:
    """
    A singleton meant to be instantiated at server startup that stores Dream data models.
    """
    def __init__(self, db_path: Optional[str] = None):
        db_store_path = DB_STORE_PATH
        # Use a dir path if provided, this is for easy testing and cleanup.
        # Otherwise use the default DB_STORE_PATH.
        if db_path is not None:
            db_store_path = db_path
        elif not os.path.isdir(DB_STORE_PATH):
            os.mkdir(DB_STORE_PATH)

        db_abs_path = os.path.join(db_store_path, DB_NAME)

        # Open DB file for read/write, create new file if not already present.
        # Uses "sync" mode so all writes are flushed to disk.
        self._store = dbm.open(db_abs_path, flag='cs')

    def get_by_id(self, dream_id: str) -> Optional[Dream]:
        """
        Returns a Dream object if present in the DB, otherwise returns None.

        Assumes all items in the DB are valid.
        """
        data = self._store.get(dream_id)
        if data is None:
            return None

        # There are some inconsistencies with dbm storage types. It is possible
        # this needs to be revisted and string types must be enforced.
        return dream_schema.loads(data)  # type: ignore

    def store_dream(self, dream: Dream) -> None:
        """
        Store a Dream object in the DB, overwriting the existing item if present.
        """
        # Save a JSON serialization of the Dream object.
        self._store[dream.dream_id] = dream_schema.dumps(dream)

    def add_dream_survey(self, survey: DreamSurvey) -> None:
        """
        Update the Dream referenced by the DreamSurvey with user provided survey responses.
        """
        dream = self.get_by_id(survey.dream_id)
        if dream is None:
            return

        dream.interest_items.extend(survey.interest_items)
        self.store_dream(dream)


# This is the instance that callers should import and interact with.
dream_db = DreamDB()
