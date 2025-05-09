# 🎬 Reccu - Your Personal Anime Recommendation Engine

<div align="center">

![Reccu Banner](https://img.shields.io/badge/ML-Reccu-ff69b4?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8-blue.svg?style=for-the-badge&logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg?style=for-the-badge&logo=tensorflow)
![Flask](https://img.shields.io/badge/Flask-2.x-green.svg?style=for-the-badge&logo=flask)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg?style=for-the-badge&logo=docker)
![CI/CD](https://img.shields.io/badge/CI%2FCD-Jenkins-red.svg?style=for-the-badge&logo=jenkins)

</div>

<div align="center">
    <img src="https://img.shields.io/maintenance/yes/2025" />
    <img src="https://img.shields.io/github/stars/rasinmuhammed/reccu?style=social" />
    <img src="https://img.shields.io/github/forks/rasinmuhammed/reccu?style=social" />
    <img src="https://img.shields.io/github/issues/rasinmuhammed/reccu" />
    <img src="https://img.shields.io/github/license/rasinmuhammed/reccu" />
</div>

<br />

> **Reccu** is a sophisticated anime recommendation system that leverages hybrid recommendation techniques to deliver highly personalized anime suggestions tailored to your unique taste.

## ✨ Features

<div align="center">
    <table>
        <tr>
            <td align="center">
                <img src="https://img.shields.io/badge/-User_Filtering-5766c3?style=for-the-badge" /><br />
                Collaborative recommendations based on similar users
            </td>
            <td align="center">
                <img src="https://img.shields.io/badge/-Content_Analysis-5766c3?style=for-the-badge" /><br />
                Smart genre and theme-based recommendations
            </td>
            <td align="center">
                <img src="https://img.shields.io/badge/-Anime_Bucket-5766c3?style=for-the-badge" /><br />
                Create collections for targeted suggestions
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="https://img.shields.io/badge/-Neural_Networks-5766c3?style=for-the-badge" /><br />
                Deep learning powered similarity detection
            </td>
            <td align="center">
                <img src="https://img.shields.io/badge/-Cloud_Powered-5766c3?style=for-the-badge" /><br />
                GCP infrastructure for scalability
            </td>
            <td align="center">
                <img src="https://img.shields.io/badge/-CI/CD_Pipeline-5766c3?style=for-the-badge" /><br />
                Automated testing and deployment
            </td>
        </tr>
    </table>
</div>

## 🚀 Tech Stack

<div align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
    <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" />
    <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
    <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
    <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
    <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" />
    <img src="https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white" />
    <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" />
    <img src="https://img.shields.io/badge/GCP-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" />
    <img src="https://img.shields.io/badge/DVC-13ADC7?style=for-the-badge&logo=dvc&logoColor=white" />
</div>

## 📋 Project Structure

```
reccu/
├── config/                  # Configuration files
├── custom_jenkins/          # Custom Jenkins Docker configuration
├── logs/                    # Application logs
├── pipeline/                # ML pipeline modules
│   ├── prediction_pipeline.py    # For generating recommendations
│   └── training_pipeline.py      # For model training
├── src/                     # Core source code
│   ├── base_model.py        # Neural CF model architecture
│   ├── custom_exception.py  # Custom exception handling
│   ├── data_ingestion.py    # Data loading from GCP
│   ├── data_processing.py   # Data preprocessing 
│   ├── logger.py            # Logging configuration
│   └── model_training.py    # Model training logic
├── static/                  # Static assets for web app
├── templates/               # HTML templates
├── utils/                   # Utility functions
│   ├── anime_bucket.py      # Anime bucket recommendation logic
│   ├── common_functions.py  # Common utility functions
│   └── helpers.py           # Helper functions for recommendations
├── .gitignore
├── application.py           # Flask application
├── config.yaml              # Configuration settings
├── deployment.yaml          # Kubernetes deployment configuration
├── Dockerfile               # Docker configuration
├── Jenkinsfile              # CI/CD pipeline definition
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
└── setup.py                 # Package setup configuration
```

## 🏁 Getting Started

### Prerequisites

- Python 3.8+
- Docker (for containerized deployment)
- GCP account (for cloud deployment)
- Git and GitHub account

### Local Development Setup

<details>
<summary>Click to expand setup instructions</summary>

1. **Clone the repository**
   ```bash
   git clone https://github.com/rasinmuhammed/reccu.git
   cd reccu
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

4. **Set up DVC and pull data**
   ```bash
   pip install dvc
   dvc pull
   ```

5. **Run the training pipeline (optional)**
   ```bash
   python pipeline/training_pipeline.py
   ```

6. **Start the Flask application**
   ```bash
   python application.py
   ```

7. **Access the web interface**
   Open your browser and navigate to http://localhost:5001

</details>

### Docker Deployment

<details>
<summary>Click to expand Docker deployment instructions</summary>

1. **Build the Docker image**
   ```bash
   docker build -t reccu:latest .
   ```

2. **Run the container**
   ```bash
   docker run -p 5001:5001 reccu:latest
   ```

3. **Access the web interface**
   Open your browser and navigate to http://localhost:5001

</details>

### GCP and Kubernetes Deployment

<details>
<summary>Click to expand cloud deployment instructions</summary>

The project includes Jenkins pipeline configurations for automated deployment to GCP's Kubernetes Engine:

1. **Set up GCP credentials**
   - Create a service account with appropriate permissions
   - Download the key file and configure it in Jenkins credentials

2. **Configure Jenkins**
   - Add the repository to Jenkins
   - Configure the pipeline to use the Jenkinsfile

3. **Run the pipeline**
   - The Jenkinsfile will handle:
     - Building the Docker image
     - Pushing to Google Container Registry
     - Deploying to Kubernetes cluster

</details>

## 📝 API Reference

### User-Based Recommendations

```python
# Get recommendations based on a user ID
recommendations = getUserBasedRecommendations(user_id)
```

### Bucket-Based Recommendations

```python
# Get recommendations based on a collection of anime
bucket_recommender = AnimeBucketRecommender()
recommendations = bucket_recommender.get_recommendations_from_bucket(anime_bucket)
```

## 🧠 How It Works

<div align="center">
<table>
  <tr>
    <td align="center">
      <b>Step 1</b><br>
      <img src="https://img.shields.io/badge/-Data_Collection-9966ff?style=for-the-badge" /><br>
      User interactions and anime metadata from MyAnimeList
    </td>
    <td align="center">
      <b>Step 2</b><br>
      <img src="https://img.shields.io/badge/-Preprocessing-9966ff?style=for-the-badge" /><br>
      Filtering, normalization, and feature engineering
    </td>
  </tr>
  <tr>
    <td align="center">
      <b>Step 3</b><br>
      <img src="https://img.shields.io/badge/-Model_Training-9966ff?style=for-the-badge" /><br>
      Neural Collaborative Filtering model with embeddings
    </td>
    <td align="center">
      <b>Step 4</b><br>
      <img src="https://img.shields.io/badge/-Recommendation-9966ff?style=for-the-badge" /><br>
      Hybrid integration of collaborative and content-based results
    </td>
  </tr>
</table>
</div>

## 📊 Model Training

The system uses a neural collaborative filtering approach implemented in TensorFlow:

1. **Data Processing**: User-anime interactions are processed and encoded
2. **Embedding Generation**: Both users and anime are embedded in a latent space
3. **Model Training**: A neural network learns to predict user ratings
4. **Weight Extraction**: Embeddings are extracted for recommendation generation

To retrain the model with new data:

```bash
python pipeline/training_pipeline.py
```

## 🔄 CI/CD Pipeline

<div align="center">
  <img src="https://img.shields.io/badge/-Code_Checkout-22272e?style=for-the-badge" /> →
  <img src="https://img.shields.io/badge/-Environment_Setup-22272e?style=for-the-badge" /> →
  <img src="https://img.shields.io/badge/-Data_Versioning-22272e?style=for-the-badge" /> →
  <img src="https://img.shields.io/badge/-Build-22272e?style=for-the-badge" /> →
  <img src="https://img.shields.io/badge/-Deploy-22272e?style=for-the-badge" />
</div>

The project includes a complete CI/CD pipeline using Jenkins that handles everything from code checkout to deployment.

## 🤝 Contributing

<details>
<summary>Contribution guidelines</summary>

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

</details>

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- MyAnimeList for the anime dataset
- The open-source ML community for inspiration and learning resources

---

<div align="center">
  <p>Built with ❤️ by <a href="https://github.com/rasinmuhammed">Muhammed Rasin</a></p>
  <p>
    <a href="https://github.com/rasinmuhammed">
      <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" />
    </a>
    <a href="https://www.linkedin.com/in/rasinmuhammed">
      <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
    </a>
  </p>
</div>
