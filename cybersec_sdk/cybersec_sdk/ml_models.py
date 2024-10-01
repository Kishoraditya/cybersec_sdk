# Copyright [2024] [Kishoraditya]
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/

# cybersec_sdk/ml_models.py

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from typing import List, Dict

class AnomalyDetector:
    """
    Implements an anomaly detection model using Isolation Forest.
    """

    def __init__(self):
        self.model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)

    def train(self, data: pd.DataFrame):
        """
        Trains the model on provided data.
        """
        self.model.fit(data)

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """
        Predicts anomalies in the data.
        Returns -1 for anomalies, 1 for normal instances.
        """
        return self.model.predict(data)
