# mypy: ignore-errors

from flask import Flask, make_response, session
from webargs import fields
from webargs.flaskparser import use_args

from server.schema.dream import (
    Dream,
    DreamSchema,
    Dreams,
    dreams_schema,
    DreamSurvey,
    DreamSurveySchema,
    dream_survey_schema
    )
from server.schema.user import LoginSchema
from server.service.dream_service import dream_service
from server.service.user_service import user_service


app = Flask(__name__)
# TODO - use os.urandom and secret sharing, this is just for dev.
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def healthcheck():
    return ''


@app.route('/login', methods=['POST'])
@use_args(LoginSchema)  # type: ignore
def login(args):
    user = user_service.get_or_create_if_valid_login(args['username'], args['password'])
    if user is None:
        return make_response({'message': 'invalid login'}, 401)
    else:
        session['username'] = user.name
        session['user_id'] = user.user_id

    return {'message': 'logged in', 'user_id': user.user_id}


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return ''


@app.route('/dream', methods=['POST'])
@use_args(DreamSchema)  # type: ignore
def add_dream(dream: Dream):
    """
    Submits a new dream to store for the user.

    Returns a survey for the user to complete which adds more details about the
    dream to the DB, as a JSON string.
    """
    survey = dream_service.add_new_dream(dream)
    return dream_survey_schema.dump(survey)


@app.route('/dream-survey', methods=['POST'])
@use_args(DreamSurveySchema)  # type: ignore
def submit_dream_survey(survey: DreamSurvey):
    """
    Stores additional survey information for a particular dream.
    """
    dream_service.update_dream_with_survey(survey)
    return ''


@app.route('/dream-log', methods=['GET'])
@use_args({"user_id": fields.Str(required=True)}, location="query")
def get_dream_log(args):
    """
    Returns a list of all of a users dreams, as a JSON string.
    """
    user_id = args['user_id']
    auth_user = session.get('user_id')
    if auth_user is None or auth_user != user_id:
        return make_response({'message': 'not logged in for this user'}, 401)

    res = user_service.get_dreams(user_id)
    return dreams_schema.dump(Dreams(dreams=res))
