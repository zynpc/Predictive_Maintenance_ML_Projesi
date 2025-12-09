import os

# Proje ana dizinini bul
PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dosya Yolları
MODEL_PATH = os.path.join(PROJ_ROOT, "models", "maintenance_model.pkl")
DATA_PATH = os.path.join(PROJ_ROOT, "data", "ai4i2020.csv")

# Modelin beklediği sütun sırası (Çok Önemli! Eğitimdeki sırayla aynı olmalı)
FEATURES = [
    'Type',
    'Air temperature [K]',
    'Process temperature [K]',
    'Rotational speed [rpm]',
    'Torque [Nm]',
    'Tool wear [min]',
    'Power_W',    # Bizim türettiğimiz
    'Temp_Diff',  # Bizim türettiğimiz
    'Strain'      # Bizim türettiğimiz
]