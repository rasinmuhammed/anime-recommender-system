from utils.helpers import *
from config.paths_config import *
from pipeline.prediction_pipeline import hybrid_recommendation
# similar_users = find_similar_users(11880,
#                    USER_WEIGHTS_PATH,
#                    USER2USER_ENCODED,
#                    USER2USER_DECODED
#                   )
# print(similar_users)
# user_preferences = get_user_preferences(11880, RATING_DF, DF)
# print(user_preferences)

print(hybrid_recommendation(22372))


# print(find_similar_animes(
#     "Steins;Gate",
#     ANIME_WEIGHTS_PATH,
#     ANIME2ANIME_ENCODED,
#     ANIME2ANIME_DECODED,
#     DF
# ))

# print(getAnimeFrame(32281,DF))