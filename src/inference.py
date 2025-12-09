import joblib
import pandas as pd
import numpy as np
import sys
import os

# src modülünü bulabilmesi için
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import MODEL_PATH, FEATURES

def load_model():
    """Eğitilmiş modeli diskten yükler."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model dosyası bulunamadı: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    return model

def predict(input_data):
    """
    Kullanıcıdan gelen ham veriyi alır, özellik mühendisliği yapar ve tahmin üretir.
    
    Args:
        input_data (dict): Kullanıcının girdiği veriler (Örn: {'Torque [Nm]': 40, ...})
        
    Returns:
        prediction (int): 0 (Sağlam) veya 1 (Bozuk)
        probability (float): Arıza olasılığı (0.0 - 1.0 arası)
    """
    # 1. Sözlüğü DataFrame'e çevir
    df = pd.DataFrame([input_data])
    
    # 2. FEATURE ENGINEERING (Model eğitimiyle birebir aynı olmalı!)
    # Kullanıcı sadece Tork ve Hız girer, biz Gücü (Power) hesaplarız.
    
    # Güç Hesabı (P = Tork * Hız * Katsayı)
    df['Power_W'] = df['Torque [Nm]'] * df['Rotational speed [rpm]'] * (2 * np.pi / 60)
    
    # Sıcaklık Farkı
    df['Temp_Diff'] = df['Process temperature [K]'] - df['Air temperature [K]']
    
    # Zorlanma (Strain)
    df['Strain'] = df['Torque [Nm]'] * df['Tool wear [min]']
    
    # Encoding (Type: L, M, H -> 0, 1, 2)
    type_map = {'L': 0, 'M': 1, 'H': 2}
    if df['Type'].dtype == 'O': # Eğer metin olarak geldiyse çevir
        df['Type'] = df['Type'].map(type_map)
        
    # 3. Sütun Sıralaması (Modelin beklediği sıra)
    # Eğer eksik veya fazlalık varsa hata almamak için filtreliyoruz
    df = df[FEATURES]
    
    # 4. Tahmin
    model = load_model()
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1] # 1 sınıfının (Arıza) olasılığı
    
    return prediction, probability