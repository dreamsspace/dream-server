# mypy: ignore-errors

import io
import base64
from wordcloud import WordCloud
# type: ignore
# from server.db.dream import dream_db
# from server.db.user import user_db
from server.schema.dream import Dream


def _create_wordcloud(dream: Dream) -> None:
    '''
    Configures custom wordcloud. See parameters in WordCloud() for customization.
    Inputs:
        - Dictionary of words and their frequency
    Outputs:
        - Wordcloud image
    '''
    wordcloud = WordCloud(
        background_color='black',
        colormap='twilight',
        # colormap='Purples',
        # mask = color_mask,
        random_state=30,
        width=1500,
        height=1200,
        font_path="../resources/sanFransiscoUltraThin.ttf",
        prefer_horizontal=1)
    wordcloud.generate_from_frequencies(frequencies=dream.ranked_keywords)

    # serialize wordcloud image for storage
    buffer = io.BytesIO()
    wordcloud.to_image().save(buffer, 'png')
    dream.wordcloud_base64 = base64.b64encode(buffer.getvalue())

    # to deserialize image ...
    # img = Image.open(io.BytesIO(base64.b64decode(b64)))
    # plt.imshow(img)
    # plt.show()

# Not sure how to call this function on each Dream instance?
# This is the instance that callers should import and interact with.
# wordcloud_service = DreamService()
