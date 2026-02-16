from model import ModelTrainer
import pandas as pd
from pathlib import Path

DATA_PATH = Path("../notebooks/transactions-2025-03-21/transactions-2025-03-21.csv")

df = pd.read_csv(DATA_PATH)

trainer = ModelTrainer()
metrics = trainer.train(df)

print(metrics)

trainer.save()
