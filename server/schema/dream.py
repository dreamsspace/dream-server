from typing import List

import datetime
from uuid import uuid4

from marshmallow import Schema, fields, post_load


class InterestItem:
    """
    The container for representing an category of items that appear in a dream.

    e.g. {name: "people", options: ["mother", "father", "pet"]}

    This container is used either for Dream storage, or when sending possible
    survery responses back to users during dream logging.
    """
    def __init__(self, name: str, options: List[str]):
        # The name of the category for this InterestItem.
        self.name: str = name
        # The items relating to the category name.
        self.options: List[str] = options


class InterestItemSchema(Schema):
    name = fields.Str()
    options = fields.List(fields.Str)

    @post_load
    def make_interest_item(self, data, **kwargs):
        return InterestItem(**data)


class DreamSurvey:
    """
    Sent to users to answer questions about a newly logged Dream, also the
    response type, but with some items removed.
    """
    def __init__(self, dream_id: str, interest_items: List[InterestItem]):
        self.dream_id: str = dream_id
        self.interest_items: List[InterestItem] = interest_items


class DreamSurveySchema(Schema):
    dream_id = fields.Str()
    interest_items = fields.Nested(InterestItemSchema, many=True)


class Dream:
    """
    The container for storing information about a single dream for a single user.
    """
    def __init__(self, user_id: str, contents: str):
        self.dream_id: str = str(uuid4())
        self.user_id: str = user_id
        self.created_at: datetime.datetime = datetime.datetime.now()
        self.contents: str = contents
        self.interest_items: List[InterestItem] = []


class DreamSchema(Schema):
    dream_id = fields.Str()
    user_id = fields.Str()
    created_at = fields.DateTime()
    contents = fields.Str()
    interest_items = fields.Nested(InterestItemSchema, many=True)

    @post_load
    def make_dream(self, data, **kwargs):
        return Dream(**data)


class Dreams:
    """
    Response type sent to users for viewing past dream logs.
    """
    def __init__(self, dreams: List[Dream]):
        self.dreams: List[Dream] = dreams


class DreamsSchema(Schema):
    dreams = fields.Nested(DreamSchema, many=True)


dream_schema = DreamSchema()
dreams_schema = DreamsSchema()
dream_survey_schema = DreamSurveySchema()
