from server.db.dream import dream_db
from server.db.user import user_db
from server.schema.dream import Dream, DreamSurvey, InterestItem


class DreamService:
    def __init__(self):
        # TODO - any one-time initialization, like loading models etc
        pass

    def _create_dream_survey(self, dream: Dream) -> DreamSurvey:
        """
        Parse and analyze the provided dream and return a custom DreamSurvey
        incorporating details about the user dream.
        """
        # TODO - This is just a static survey, this method should handle parsing
        # and lexical analysis to produce a custom survey.
        return DreamSurvey(
            dream_id=dream.dream_id,
            interest_items=[
                InterestItem(
                    name='people',
                    options=['man', 'father', 'wife', 'boss'],
                ),
                InterestItem(
                    name='actions',
                    options=['running', 'climbing', 'chasing', 'crying'],
                ),
            ],
        )

    def add_new_dream(self, dream: Dream) -> DreamSurvey:
        """
        Saves a new dream for a user, parses its content, and returns a DreamSurvey
        that the user can complete to provide more information.
        """
        dream_db.store_dream(dream)
        user_db.add_dream_to_user(dream.user_id, dream.dream_id)
        return self._create_dream_survey(dream)

    def update_dream_with_survey(self, survey: DreamSurvey) -> None:
        """
        Update stored Dream with new survey response from user.
        """
        dream_db.add_dream_survey(survey)


# This is the instance that callers should import and interact with.
dream_service = DreamService()
