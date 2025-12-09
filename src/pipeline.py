import pandas as pd
import numpy as np
import joblib
import sys
import os

# Scikit-Learn ve Imbalance Kütüphaneleri
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

# Proje dizinini yola ekleme (config dosyasını bulması için)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import DATA_PATH, MODEL_PATH, FEATURES

def run_training():
    print("Pipeline Başlatıldı...")
    

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {DATA_PATH}")
    
    print(f"Veri Yükleniyor: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    
    # FEATURE ENGINEERING (Özellik Mühendisliği)
    print("Feature Engineering yapılıyor...")
    
    # Encoding (Type: L, M, H -> 0, 1, 2)
    type_map = {'L': 0, 'M': 1, 'H': 2}
    df['Type'] = df['Type'].map(type_map)
    
    # Fiziksel Formüller
    # P = 2 * pi * n * T / 60
    df['Power_W'] = df['Torque [Nm]'] * df['Rotational speed [rpm]'] * (2 * np.pi / 60)
    df['Temp_Diff'] = df['Process temperature [K]'] - df['Air temperature [K]']
    df['Strain'] = df['Torque [Nm]'] * df['Tool wear [min]']
    
    # VERİ HAZIRLIĞI (Temizlik ve Split)
    # Hedef ve Özellik Ayrımı
    X = df.drop(['UDI', 'Product ID', 'Machine failure', 'TWF', 'HDF', 'PWF', 'OSF', 'RNF'], axis=1)
    y = df['Machine failure']
    
    # Sütun sırasını garantiye al (Config'deki sıraya göre)
    # Not: drop işlemi sonrası kalan sütunlar config'deki FEATURES ile aynı olmalı
    # (Power, Strain vb. eklendiği için kontrol ediyoruz)
    
    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # DENGESİZLİK GİDERME (SMOTE)
    print("SMOTE ile veri dengeleniyor...")
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    
    # MODEL EĞİTİMİ (Random Forest)
    print("Model Eğitiliyor (Random Forest - 200 Ağaç)...")
    model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X_train_resampled, y_train_resampled)
    
    # DEĞERLENDİRME
    print("Model Test Ediliyor...")
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    print("\n--- Model Performans Raporu ---")
    print(report)
    
    # KAYDETME
    print(f"Model Kaydediliyor: {MODEL_PATH}")
    # Klasör yoksa oluştur
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    
    print("Pipeline Başarıyla Tamamlandı!")

if __name__ == "__main__":
    run_training()