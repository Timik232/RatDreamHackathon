import os

import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.fft import rfft, rfftfreq, irfft
from scipy.signal import butter, filtfilt, find_peaks
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from joblib import load

models_path = "models/"
model_start = os.path.join(models_path, "start_model.joblib")
model_end = os.path.join(models_path, "end_model.joblib")


class MLModels:
    def __init__(self):
        self.model_start = load(model_start)
        self.model_end = load(model_end)
        self.current_model = model_start

    def predprocessing(self, predchunk, chunk, metainfo):
        return np.sum(chunk["y"], axis=0)

    def predict(self, predchunk, chunk, metainfo, mode):
        data = self.predprocessing(predchunk, chunk, metainfo)

        if mode == "start":
            self.current_model = self.model_start
        else:
            self.current_model = self.model_end

        pred = self.current_model.predict(data)

        if pred != "none" and mode == "start":
            mode = "end"
        elif pred != "none":
            mode = "start"

        return {"x": np.mean(chunk["x"][750]), "y": pred, "mode": mode}
