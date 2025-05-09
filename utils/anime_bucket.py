import pandas as pd
import numpy as np
import joblib
from config.paths_config import *
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class AnimeBucketRecommender:
    """
    A class to handle anime bucket recommendations, allowing users to get
    recommendations based on a collection of their favorite anime.
    """
    
    def __init__(self):
        try:
            # Load required resources
            self.df = pd.read_csv(DF)
            self.synopsis_df = pd.read_csv(SYNOPSIS_DF)
            self.anime_weights = joblib.load(ANIME_WEIGHTS_PATH)
            self.anime2anime_encoded = joblib.load(os.path.join(PROCESSED_DIR, "anime2anime_encoded.pkl"))
            self.anime2anime_decoded = joblib.load(os.path.join(PROCESSED_DIR, "anime2anime_decoded.pkl"))
            logger.info("AnimeBucketRecommender initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing AnimeBucketRecommender: {e}")
            raise CustomException("Failed to initialize AnimeBucketRecommender", e)
    
    def get_anime_names(self, query_term=None, limit=10):
        """
        Get a list of anime names that match the query term for autocomplete
        
        Args:
            query_term (str): The search query
            limit (int): Maximum number of results to return
            
        Returns:
            list: List of anime names matching the query
        """
        try:
            if query_term is None or query_term == "":
                # Return popular anime if no query
                return self.df.sort_values(by="Score", ascending=False).head(limit)["eng_version"].tolist()
            
            # Case-insensitive search
            matches = self.df[self.df["eng_version"].str.lower().str.contains(query_term.lower())]
            return matches.sort_values(by="Score", ascending=False).head(limit)["eng_version"].tolist()
        except Exception as e:
            logger.error(f"Error getting anime names: {e}")
            raise CustomException("Failed to get anime names", e)
    
    def get_anime_details(self, anime_name):
        """
        Get details for a specific anime
        
        Args:
            anime_name (str): The name of the anime
            
        Returns:
            dict: Details of the anime
        """
        try:
            anime_row = self.df[self.df["eng_version"] == anime_name]
            if anime_row.empty:
                return None
                
            anime_id = anime_row["anime_id"].values[0]
            
            # Get synopsis
            synopsis = None
            try:
                synopsis_row = self.synopsis_df[self.synopsis_df["MAL_ID"] == anime_id]
                if not synopsis_row.empty:
                    synopsis = synopsis_row["sypnopsis"].values[0]
            except Exception as e:
                logger.warning(f"Could not get synopsis for {anime_name}: {e}")
            
            return {
                "anime_id": int(anime_id),
                "name": anime_name,
                "score": float(anime_row["Score"].values[0]) if not np.isnan(anime_row["Score"].values[0]) else None,
                "genres": anime_row["Genres"].values[0],
                "episodes": anime_row["Episodes"].values[0],
                "type": anime_row["Type"].values[0],
                "premiered": anime_row["Premiered"].values[0],
                "synopsis": synopsis
            }
        except Exception as e:
            logger.error(f"Error getting anime details: {e}")
            raise CustomException(f"Failed to get details for anime {anime_name}", e)
    
    def get_recommendations_from_bucket(self, anime_bucket, limit=10):
        """
        Get recommendations based on a bucket of favorite anime
        
        Args:
            anime_bucket (list): List of anime names in the bucket
            limit (int): Maximum number of recommendations to return
            
        Returns:
            list: List of recommended anime with details
        """
        try:
            if not anime_bucket:
                return []
                
            # Get encoded indices for anime in bucket
            encoded_indices = []
            for anime_name in anime_bucket:
                anime_details = self.get_anime_details(anime_name)
                if anime_details:
                    anime_id = anime_details["anime_id"]
                    encoded_index = self.anime2anime_encoded.get(anime_id)
                    if encoded_index is not None:
                        encoded_indices.append(encoded_index)
            
            if not encoded_indices:
                return []
                
            # Calculate average embedding for the bucket
            bucket_embedding = np.mean(self.anime_weights[encoded_indices], axis=0)
            bucket_embedding = bucket_embedding / np.linalg.norm(bucket_embedding)
            
            # Calculate similarity with all anime
            similarities = np.dot(self.anime_weights, bucket_embedding)
            sorted_indices = np.argsort(similarities)[::-1]  # Sort in descending order
            
            # Build recommendations
            recommendations = []
            count = 0
            for idx in sorted_indices:
                if count >= limit:
                    break
                    
                anime_id = self.anime2anime_decoded.get(idx)
                if anime_id is None:
                    continue
                    
                anime_row = self.df[self.df["anime_id"] == anime_id]
                if anime_row.empty:
                    continue
                    
                anime_name = anime_row["eng_version"].values[0]
                
                # Skip anime that are already in the bucket
                if anime_name in anime_bucket:
                    continue
                    
                # Get details
                anime_details = self.get_anime_details(anime_name)
                if anime_details:
                    anime_details["similarity"] = float(similarities[idx])
                    recommendations.append(anime_details)
                    count += 1
            
            return recommendations
        except Exception as e:
            logger.error(f"Error getting recommendations from bucket: {e}")
            raise CustomException("Failed to get recommendations from bucket", e)