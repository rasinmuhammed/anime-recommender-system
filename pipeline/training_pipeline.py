from utils.common_functions import read_yaml
from src.data_processing import DataProcessor
from src.model_training import ModelTraining
from config.paths_config import *


if __name__=="__main__":

    data_processor = DataProcessor(ANIMELIST_CSV, PROCESSED_DIR)
    data_processor.run()

    model_trainer = ModelTraining(PROCESSED_DIR)
    model_trainer.train_model()