import os
import pandas as pd
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from utils.common_functions import read_yaml
from config.paths_config import *

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):

        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.file_names = self.config['bucket_file_name']
        
        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info("Initializing Data Ingestion")

    def download_csv_from_gcp(self):
        try:
            logger.info("Downloading data from GCS")
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)

            for file_name in self.file_names:
                file_path = os.path.join(RAW_DIR, file_name)

                if file_name == "animelist.csv":
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)
                    logger.info(f"Downloaded {file_name} to {file_path}")

                    data = pd.read_csv(file_path, nrows=55000000)
                    data.to_csv(file_path, index=False)
                    logger.info(f"Large file detected. Downloading first 55 million rows of {file_name}")

                else:
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)
                    logger.info(f"Downloaded {file_name} to {file_path}")

        except Exception as e:
            logger.error(f"Error downloading data from GCS: {e}")
            raise CustomException("Failed to download data from GCS", e)
        
    def run(self):
        try:
            logger.info("Running Data Ingestion")
            self.download_csv_from_gcp()
            logger.info("Data Ingestion completed successfully")
        except Exception as e:
            logger.error(f"Error in Data Ingestion: {e}")
            raise CustomException("Failed in Data Ingestion", e)

if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

            