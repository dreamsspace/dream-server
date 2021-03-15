from server.service.dream_service import dream_service
from server.schema.dream import Dream


def test_keyword_extraction():
    dream = Dream(user_id='connor',
     contents='this is a dream where i flew in space a a a a bug bug bug words words like the and blah')
    assert dream.ranked_keywords == {}
    dream_service._create_keywords(dream)
    assert len(dream.ranked_keywords) == 5
