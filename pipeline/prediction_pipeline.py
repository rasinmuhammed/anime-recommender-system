from config.paths_config import *
from utils.helpers import *

def hybrid_recommendation(user_id, user_weight=0.5, content_weight=0.5, top_n=10):
    # 1. USER RECOMMENDATION
    similar_users = find_similar_users(user_id, USER_WEIGHTS_PATH, USER2USER_ENCODED, USER2USER_DECODED)
    user_pref = get_user_preferences(user_id, RATING_DF, DF)
    user_recommended_animes = get_user_recommendations(similar_users, user_pref, DF, SYNOPSIS_DF, RATING_DF)

    user_recommended_anime_list = user_recommended_animes["anime_name"].tolist()

    # 2. CONTENT RECOMMENDATION
    content_recommended_animes = []

    for anime in user_recommended_anime_list:
        similar_animes = find_similar_animes(anime, ANIME_WEIGHTS_PATH, ANIME2ANIME_ENCODED, ANIME2ANIME_DECODED, DF, n=top_n)
        if similar_animes is not None and not similar_animes.empty:
            content_recommended_animes.extend(similar_animes.to_dict(orient="records"))
        else:
            print(f"No similar anime found for: {anime}")

    # 3. Combine scores
    combined_scores = {}
    metadata_map = {}

    # Add user-based recommendations
    for i, row in user_recommended_animes.iterrows():
        name = row["anime_name"]
        combined_scores[name] = combined_scores.get(name, 0) + user_weight
        metadata_map[name] = {
            "anime_name": name,
            "Genres": row["Genres"],
            "Synopsis": row["Synopsis"],
            "source": "user",
            "score": combined_scores[name]
        }

    # Add content-based recommendations
    for rec in content_recommended_animes:
        name = rec["name"]
        combined_scores[name] = combined_scores.get(name, 0) + content_weight

        if name in metadata_map:
            metadata_map[name]["score"] = combined_scores[name]
            metadata_map[name]["source"] = "hybrid"
        else:
            # fetch synopsis
            try:
                synopsis = getSynopsis(name, SYNOPSIS_DF)
            except:
                synopsis = "N/A"
            metadata_map[name] = {
                "anime_name": name,
                "Genres": rec["genre"],
                "Synopsis": synopsis,
                "source": "content",
                "score": combined_scores[name]
            }

    # 4. Sort and return as DataFrame
    sorted_animes = sorted(metadata_map.values(), key=lambda x: x["score"], reverse=True)
    return pd.DataFrame(sorted_animes[:top_n])
