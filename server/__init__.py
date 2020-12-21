from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from server.db.dream import dream_db
from server.db.user import user_db
from server.schema.dream import (
    Dream,
    DreamSchema,
    Dreams,
    dreams_schema,
    DreamSurvey,
    DreamSurveySchema,
    dream_survey_schema,
)
from server.service.dream_service import dream_service


app = Flask(__name__)


# TODO - This should require auth.
# @app.route('/login', methods=['POST'])
# @use_args({"name": fields.Str(required=True)}, location="form")
# def login(args):
#     """
#     "Signs in" a user.

#     For now this doesn't do anything besides returning a user_id.
#     """
#     user_db.get_
#     return ''

@app.route('/dream', methods=['POST'])
@use_args(DreamSchema)  # type: ignore
def add_dream(dream: Dream) -> str:
    """
    Submits a new dream to store for the user.

    Returns a survey for the user to complete which adds more details about the
    dream to the DB, as a JSON string.
    """
    survey = dream_service.add_new_dream(dream)
    return dream_survey_schema.dumps(survey)


@app.route('/dream-survey', methods=['POST'])
@use_args(DreamSurveySchema)  # type: ignore
def submit_dream_survey(survey: DreamSurvey):
    """
    Stores additional survey information for a particular dream.
    """
    dream_service.update_dream_with_survey(survey)
    return ''


# TODO - This should require auth.
@app.route('/dream-log', methods=['GET'])
@use_args({"user_id": fields.Str(required=True)}, location="query")
def get_dream_log(args):
    """
    Returns a list of all of a users dreams, as a JSON string.
    """
    res = Dreams(dreams=[])

    user_id = args['user_id']
    user = user_db.get_by_id(user_id)
    if user is None:
        return dreams_schema.dumps(res)

    for dream_id in user.dream_ids:
        dream = dream_db.get_by_id(dream_id)
        if dream is not None:
            res.dreams.append(dream)

    return dreams_schema.dumps(res)
