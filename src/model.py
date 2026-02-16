import joblib
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from preprocessing import Preprocessor
import numpy as np

class ModelTrainer:

    def __init__(self):
        self.preprocessor = Preprocessor()
        self.model = LGBMRegressor(
            learning_rate=0.05,
            num_leaves=31,
            n_estimators=500,

            random_state=42
        )


    def train_og(self, df):

        # Fit preprocessing and transform
        df = df.copy()
        df["log_price"] = np.log1p(df["TRANS_VALUE"])

        processed_df = self.preprocessor.fit_transform(df)

        X = processed_df.drop(columns=["log_price"])
        y = df["log_price"]  # ← take from original df

        # Time-aware split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )

        # Train model
        self.model.fit(X_train, y_train)

        # Evaluate
        preds = self.model.predict(X_test)

        metrics = {
            "MAE_log": mean_absolute_error(y_test, preds),
            "R2": r2_score(y_test, preds)
        }

        return metrics

    def train(self, df):
        df = df.copy()
        df["log_price"] = np.log1p(df["TRANS_VALUE"])

        # IMPORTANT: sort by time first (like notebook)
        df = df.sort_values("INSTANCE_DATE")

        split_index = int(len(df) * 0.8)

        train_df = df.iloc[:split_index]
        test_df = df.iloc[split_index:]

        # 🔥 FIT ONLY ON TRAIN DATA
        self.preprocessor.fit(train_df)

        # Transform separately
        X_train = self.preprocessor.transform(train_df)
        X_test = self.preprocessor.transform(test_df)

        y_train = train_df["log_price"]
        y_test = test_df["log_price"]

        self.model.fit(X_train, y_train)

        preds = self.model.predict(X_test)

        metrics = {
            "MAE_log": mean_absolute_error(y_test, preds),
            "R2": r2_score(y_test, preds)
        }

        return metrics

    def save(self, model_path="../models/trained_model.pkl",
             preprocessor_path="../models/preprocessor.pkl"):

        joblib.dump(self.model, model_path)
        joblib.dump(self.preprocessor, preprocessor_path)
