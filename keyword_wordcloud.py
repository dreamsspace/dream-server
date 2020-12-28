import yake
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from PIL import Image
from wordcloud import WordCloud
from matplotlib import pyplot as plt


text1 = "I was running away from something that I do not remember, only knowing that I was in danger. I was hitch hiking and got a ride from a man in an old truck. We drove for a long time until we got to a fork in the road. I asked him if this is where the chimera zone was, pointing to the steep hill of a road straight through the intersection. He said yes and with fear, told me that I shouldnt go in there because it was very dangerous. No one who went in came out he said. I knew this and was okay with it, for it was preferred over being caught by the group chasing me. I got out and ran across the road and climbed the hill to get in. It didn't look steep, but the road was so steep that I had to climb by grabbing the pushes as handholds on the side. When I climbed to the top, the road was so steep and the decline on the other side was so steep that I was able to straddle the top. I sat at the top with legs over both sides, took a final look at he concerned man who helped me, and then swung my legs over into the dark, heavily vegetated chimera zone. It was like a rainforest and I saw a flower that was half white and half red, with the colors splitting perfectly down the middle."
text2 = "I was in the reddish brown desert of Utah or Colorado on a hill side with large rocks everywhere. It was very crowded and appeard to be a mining operation. Below, an impressive array of dynamite was set off the the explosion was orderly, loud, and exciting. Shortly after, a rock slide started. It started below me and I watched from safety. It was very large and many huge rocks fell. It looked like people were getting injured. As I noticed that, I looked up and saw the rock slide starting above me. I hid under the steep face of a small cliff and was protected. Every once in a while I would look up, only to have a massive rock fly right by my head and I would duck again. This went on for some time until someone shouted the rocks had stopped. They pointed out a road to the top of the hill and we climbed it to safety. We had to run but I was worried about a calf injury I had in real life, but it was fine. At the top, there were many people and well organized ultramarathon appeard to be happening. I was invited to join. While I hesitated due to my injury and the frightening situation, not knowing if it was safe or not, I joined for the down hill portion. It was great fun. There was a river crossing at the bottom over loose logs. At one point in the middle, there was a log that would only support 2 people but I was with hannah and sadie. I volunteered to have them cross safely and I would swim. I swam until the next log where I climbed to safety with great difficulty."

def keyword_extraction(text):
    '''
    This function configures YAKE parameters for keyword extraction.
    Inputs:
        - Raw text for keyword extraction
    Outputs:
        - n number of keywords and their importance value (list of 2 tuples)
    '''

    # custom parameters
    language = "en"
    max_ngram_size = 2
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 20

    custom_kw_extractor = yake.KeywordExtractor(
        lan=language,
        n=max_ngram_size,
        dedupLim=deduplication_thresold,
        dedupFunc=deduplication_algo,
        windowsSize=windowSize,
        top=numOfKeywords,
        features=None
        )

    keywords = custom_kw_extractor.extract_keywords(text)
    
    return keywords


def rank_words(keywords):
    '''
    Wordcloud has the ability to generate text size by frequency.
    To do this, we use the value determined by the keyword extractor.
    Must be a dictionary with key-value being word-frequency.
    Inputs:
        - List of 2 tuples of keywords and importance value
    Outputs:
        - Dictionary of keywords and value
    '''

    d = {
        w: f for w, f in keywords
    }

    return d


def create_wordcloud(ranked_words):
    '''
    Configures custom wordcloud. See parameters in WordCloud() for customization.
    Inputs:
        - Dictionary of words and their frequency
    Outputs:
        - Wordcloud image
    '''

    # custom font
    # font_path = "../../../Downloads/sanFransiscoThin.ttf"
    font_path = "sanFransiscoUltraThin.ttf"
    wordcloud = WordCloud(
        background_color='black',
        colormap='twilight',
        # colormap='Purples',
        # mask = color_mask,
        random_state=30,
        width=1500,
        height=1200,
        font_path = font_path,
        prefer_horizontal=1)
    wordcloud.generate_from_frequencies(frequencies=d)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()


# Extract keywords with Yake
keywords = keyword_extraction(text2)
# Create word-frequency dictionary
d = rank_words(keywords)
# Print out keywords and their importance
for kw in keywords:
        print(kw)
# Generate wordcloud
create_wordcloud(d)
