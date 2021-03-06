# -*- coding: utf-8 -*-
import mlflow
from mlflow import log_metric


def log(model, error):
    log_metric("mae", error.describe().T["mean"])
    log_metric("median_ae", error.describe().T["50%"])
    log_metric("max_ae", error.describe().T["max"])
    log_metric("min_ae", error.describe().T["min"])
    mlflow.keras.log_model(model, "models")
