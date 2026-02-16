import pandas as pd
import numpy as np


class Preprocessor:

    def __init__(self):
        self.area_mean = None
        self.project_mean = None
        self.metro_mean = None
        self.mall_mean = None
        self.landmark_mean = None
        self.global_mean = None
        self.feature_columns = None

    #fit
    def fit(self, df: pd.DataFrame):

        df = df.copy()
        self.area_mean = df.groupby("AREA_EN")["log_price"].mean()
        self.project_mean = df.groupby("PROJECT_EN")["log_price"].mean()
        self.metro_mean = df.groupby("NEAREST_METRO_EN")["log_price"].mean()
        self.mall_mean = df.groupby("NEAREST_MALL_EN")["log_price"].mean()
        self.landmark_mean = df.groupby("NEAREST_LANDMARK_EN")["log_price"].mean()
        self.global_mean = df["log_price"].mean()

    def transform(self, df: pd.DataFrame):
        df = df.copy()
        df["INSTANCE_DATE"] = pd.to_datetime(df["INSTANCE_DATE"])
        df["year"] = df["INSTANCE_DATE"].dt.year
        df["month"] = df["INSTANCE_DATE"].dt.month

        if "USAGE_EN" in df.columns:
            df["ROOM_TYPE"] = df["USAGE_EN"]

        low_card_cols = [
            "IS_OFFPLAN_EN",
            "IS_FREE_HOLD_EN",
            "USAGE_EN",
            "PROP_TYPE_EN",
            "ROOM_TYPE"
        ]

        existing_cols = [c for c in low_card_cols if c in df.columns]
        df = pd.get_dummies(df, columns=existing_cols, drop_first=True)


        df["AREA_TE"] = df["AREA_EN"].map(self.area_mean)
        df["PROJECT_TE"] = df["PROJECT_EN"].map(self.project_mean)
        df["METRO_TE"] = df["NEAREST_METRO_EN"].map(self.metro_mean)
        df["MALL_TE"] = df["NEAREST_MALL_EN"].map(self.mall_mean)
        df["LANDMARK_TE"] = df["NEAREST_LANDMARK_EN"].map(self.landmark_mean)

        encoding_cols = [
            "AREA_TE",
            "PROJECT_TE",
            "METRO_TE",
            "MALL_TE",
            "LANDMARK_TE"
        ]

        for col in encoding_cols:
            df[col] = df[col].fillna(self.global_mean)

        df = df.drop(columns=[
            "MASTER_PROJECT_EN",
            "PARKING",
            "TRANSACTION_NUMBER",
            "GROUP_EN",
            "PROCEDURE_EN",
            "AREA_EN",
            "PROJECT_EN",
            "NEAREST_METRO_EN",
            "NEAREST_MALL_EN",
            "NEAREST_LANDMARK_EN",
            "PROP_SB_TYPE_EN",
            "ROOMS_EN",
            "TRANS_VALUE",
            "INSTANCE_DATE",
            "AREA_EN",
            "log_price"
        ], errors="ignore")


        if self.feature_columns is None:
            self.feature_columns = df.columns.tolist()

        #alignment of columns
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0

        df = df[self.feature_columns]

        return df

    def fit_transform(self, df: pd.DataFrame):
        self.fit(df)
        return self.transform(df)
