from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import pandas as pd
import numpy as np
import joblib
import os
import sys
from config.paths_config import *
from utils.anime_bucket import AnimeBucketRecommender
from src.logger import get_logger
from src.custom_exception import CustomException
from pipeline.prediction_pipeline import hybrid_recommendation

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

logger = get_logger(__name__)

# Initialize bucket recommender
bucket_recommender = AnimeBucketRecommender()

def getUserBasedRecommendations(user_id):
    """Get recommendations based on user ID"""
    try:
        return hybrid_recommendation(user_id)
        
    except Exception as e:
        logger.error(f"Error getting user-based recommendations: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = None
    bucket_recommendations = None
    user_id = None
    anime_bucket = session.get('anime_bucket', [])
    
    if request.method == 'POST':
        # User ID based recommendation
        if 'userID' in request.form:
            try:
                user_id = int(request.form['userID'])
                recommendations = getUserBasedRecommendations(user_id)
                if isinstance(recommendations, pd.DataFrame):
                    recommendations = recommendations.to_dict(orient='records')

            except Exception as e:
                logger.error(f"Error processing user ID: {e}")
                
        # Bucket based recommendation
        if 'get_bucket_recommendations' in request.form:
            try:
                bucket_recommendations = bucket_recommender.get_recommendations_from_bucket(anime_bucket)
            except Exception as e:
                logger.error(f"Error getting bucket recommendations: {e}")
                
    return render_template(
        'index.html', 
        recommendations=recommendations, 
        userID=user_id,
        anime_bucket=anime_bucket,
        bucket_recommendations=bucket_recommendations
    )

@app.route('/search_anime', methods=['GET'])
def search_anime():
    """API endpoint for anime name autocomplete"""
    query = request.args.get('q', '')
    try:
        results = bucket_recommender.get_anime_names(query)
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error in anime search: {e}")
        return jsonify([])

@app.route('/add_to_bucket', methods=['POST'])
def add_to_bucket():
    """Add an anime to the user's bucket"""
    anime_name = request.form.get('anime_name')
    
    if not anime_name:
        return redirect(url_for('index'))
        
    # Initialize bucket if not exists
    if 'anime_bucket' not in session:
        session['anime_bucket'] = []
        
    # Add anime if not already in bucket
    if anime_name not in session['anime_bucket']:
        # Verify anime exists in database
        try:
            details = bucket_recommender.get_anime_details(anime_name)
            if details:
                session['anime_bucket'].append(anime_name)
                session.modified = True  # Important for session persistence
        except Exception as e:
            logger.error(f"Error adding anime to bucket: {e}")
            
    return redirect(url_for('index'))

@app.route('/remove_from_bucket', methods=['POST'])
def remove_from_bucket():
    """Remove an anime from the user's bucket"""
    anime_name = request.form.get('anime_name')
    
    if not anime_name or 'anime_bucket' not in session:
        return redirect(url_for('index'))
        
    # Remove anime if found
    if anime_name in session['anime_bucket']:
        session['anime_bucket'].remove(anime_name)
        session.modified = True
        
    return redirect(url_for('index'))

@app.route('/clear_bucket', methods=['POST'])
def clear_bucket():
    """Clear the user's anime bucket"""
    session['anime_bucket'] = []
    session.modified = True
    return redirect(url_for('index'))

@app.route('/anime_details/<anime_name>')
def anime_details(anime_name):
    """Show details for a specific anime"""
    try:
        details = bucket_recommender.get_anime_details(anime_name)
        if details:
            return render_template('anime_details.html', anime=details)
        else:
            return "Anime not found", 404
    except Exception as e:
        logger.error(f"Error showing anime details: {e}")
        return "Error loading anime details", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)