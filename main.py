# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import mlflow
from sklearn.model_selection import train_test_split
from src.neuralnet import train_neural_net
from src.gradientboost import train_gbdt
from src.play import play
from src.helper import denorm
from src.logger import log
import shutil
import warnings
import sys
import optuna

shutil.rmtree("./mlruns/")
# shutil.rmtree("./logs/")
experiment_id = mlflow.create_experiment("Predict_Temperature")
np.random.seed = 42
features = [
    "D1",
    "D2",
    "D1D2",
    "Perimeter1",
    "Perimeter2",
    "Area1",
    "Area2",
    "Identifier",
]
labels = ["Temperature"]


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    df = pd.read_excel("data/ML_Data.xlsx")
    df = df.sample(frac=1).reset_index(drop=True)  # Shuffles dataframe rows randomly
    train, test = train_test_split(df, shuffle=False, test_size=0.1)
    test = test.reset_index(drop=True)
    params = [float(i) for i in sys.argv[1:]] if len(sys.argv) > 1 else None

    for ntrial in range(1):
        with mlflow.start_run(experiment_id=experiment_id, source_name="main.py", source_version="0"):
            train = train.sample(frac=1).reset_index(drop=True)
            X_train = train[features]
            y_train = train[labels]
            # train_features['Identifier'] = train_features['Identifier'].map({1: 100, 0: 0})
            method = "stdev"
            model, train_error = train_neural_net(X_train, y_train, params=params)
            # model, difference = train_gbdt(train_features, train_labels)

            X_test = test[features]
            y_test = test[labels]
            test_stats = y_test.describe().transpose()
            norm_predictions = play(model=model, data=X_test, method=method)
            predictions = denorm(norm_predictions, test_stats, method=method)
            test_error = abs((y_test - predictions)["Temperature"])
            log(model=model, error=test_error)
