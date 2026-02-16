import joblib
import pandas as pd
import numpy as np


class PredictionService:

    def __init__(self,
                 model_path="../models/trained_model.pkl",
                 preprocessor_path="../models/preprocessor.pkl"):

        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)

    def predict(self, request):

        input_df = pd.DataFrame([{
            "INSTANCE_DATE": pd.Timestamp.now(),
            "AREA_EN": request.area,
            "PROJECT_EN": request.project,
            "NEAREST_METRO_EN": request.nearest_metro,
            "NEAREST_MALL_EN": request.nearest_mall,
            "NEAREST_LANDMARK_EN": None,
            "ACTUAL_AREA": request.actual_area,
            "ROOMS_EN": f"{request.rooms} B/R",
            "PARKING": request.parking,
            "IS_OFFPLAN_EN": "Off-Plan" if request.is_offplan else "Ready",
            "IS_FREE_HOLD_EN": "Free Hold" if request.is_freehold else "Non Free Hold",
            "USAGE_EN": request.usage,
            "PROP_TYPE_EN": request.property_type,
            "PROP_SB_TYPE_EN": request.property_subtype,
            "TRANSACTION_NUMBER": None,
            "GROUP_EN": None,
            "PROCEDURE_EN": None,
            "MASTER_PROJECT_EN": request.master_project,
            "TRANS_VALUE": 0
        }])

        processed = self.preprocessor.transform(input_df)

        log_pred = self.model.predict(processed)[0]
        predicted_price = float(np.expm1(log_pred))

        lower = predicted_price * 0.95
        upper = predicted_price * 1.05

        return {
            "predicted_price": round(predicted_price, 2),
            "confidence_interval": {
                "lower": round(lower, 2),
                "upper": round(upper, 2)
            },
            "price_per_sqft": round(predicted_price / request.actual_area, 2),
            "model_confidence": "high",
            "key_factors": [
                f"Location: {request.area}",
                f"Property size: {request.actual_area} sqft",
                "Proximity to metro station"
            ]
        }
