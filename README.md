# Predictive Maintenance Projesi

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Machine Learning](https://img.shields.io/badge/Model-Random%20Forest-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Proje Kapsamı ve Problem Tanımı
Endüstriyel üretim hatlarında, makinelerin plansız duruşları (downtime) şirketlere milyonlarca dolar zarar ve zaman kaybına neden olmaktadır. Bu projenin amacı; makinelerden gelen sensör verilerini (sıcaklık, tork, devir hızı vb.) analiz ederek, **arızaları gerçekleşmeden önce tespit eden** bir Yapay Zeka modeli geliştirmektir.

Proje, dengesiz veri setleri (Imbalanced Data) ile çalışma, fiziksel öznitelik mühendisliği (Feature Engineering) ve modelin canlıya alınması (Deployment) süreçlerini uçtan uca kapsamaktadır.

---

### Canlı Demo (Inference)
Modelin çalışan canlı versiyonunu aşağıdaki linkten test edebilirsiniz:

**Canlı Uygulama Linki:** [https://predictive-maintenance-ml-projesi.streamlit.app/](https://predictive-maintenance-ml-projesi.streamlit.app/)

---

## Ekran Görüntüleri

### 1. Web Arayüzü (Streamlit)
![Streamlit Arayüz Normal](https://github.com/zynpc/Predictive_Maintenance_ML_Projesi/blob/main/docs/Ekran%20G%C3%B6r%C3%BCnt%C3%BCs%C3%BC%20(1032).png?raw=true)

![Streamlit Arayüz Riskli Durum](https://github.com/zynpc/Predictive_Maintenance_ML_Projesi/blob/main/docs/Ekran%20G%C3%B6r%C3%BCnt%C3%BCs%C3%BC%20(1033).png?raw=true)

### 2. SHAP Analizi (Model Açıklanabilirliği)
![SHAP Analysis](https://github.com/zynpc/Predictive_Maintenance_ML_Projesi/blob/main/docs/output.png?raw=true)

---

## Sektör, Veri ve Pipeline Bilgisi

* **Sektör:** Endüstri 4.0 / Üretim (Manufacturing).
* **Veri Seti:** UCI Machine Learning Repository - **AI4I 2020 Predictive Maintenance Dataset**. 10.000 adet makine kaydı ve 14 öznitelik içerir.
* **Pipeline:**
    1.  **EDA:** Veri dengesizliğinin (%3.4 Arıza) ve fiziksel ilişkilerin tespiti.
    2.  **Preprocessing:** Sızıntı (Leakage) sütunlarının temizlenmesi ve Encoding.
    3.  **Feature Engineering:** `Power` (Güç), `Strain` (Zorlanma) gibi fiziksel formüllerin türetilmesi.
    4.  **Handling Imbalance:** SMOTE tekniği ile azınlık sınıfının artırılması.
    5.  **Modelling:** Random Forest Classifier (GridSearch ile optimize edildi).
* **Kritik Metrik:** **Recall (Duyarlılık)**. Çünkü bir arızayı kaçırmanın maliyeti (False Negative), yanlış alarmdan (False Positive) çok daha yüksektir.

---

## Kullanılan Teknolojiler

* **Dil:** Python 3.x
* **Veri İşleme:** Pandas, NumPy
* **Makine Öğrenmesi:** Scikit-Learn, Imbalanced-learn (SMOTE)
* **Model Açıklanabilirliği:** SHAP
* **Arayüz (Deployment):** Streamlit
* **Versiyon Kontrol:** Git & GitHub

---

## Repo Yapısı

```text
PredictiveMaintenance_Project/
├── data/                   # Ham veri seti (ai4i2020.csv)
├── docs/                   # Detaylı Raporlar ve Görseller
│   └── FINAL_REPORT.md     # Projenin detaylı teknik raporu
├── models/                 # Eğitilmiş Model (.pkl)
├── notebooks/              # Geliştirme Süreci (Jupyter Notebooks)
│   ├── 1_EDA.ipynb
│   ├── 2_Baseline_Model.ipynb
│   ├── 3_Feature_Engineering.ipynb
│   ├── 4_Model_Optimization.ipynb
│   ├── 5_Model_Evaluation_SHAP.ipynb
│   └── 6_Pipeline_Final.ipynb
├── src/                    # Canlı Sistem Kodları
│   ├── app.py              # Streamlit Arayüzü
│   ├── config.py           # Ayar Dosyası
│   ├── inference.py        # Tahmin Motoru
│   └── pipeline.py         # Otomatik Eğitim Scripti
├── requirements.txt        # Kütüphane Listesi
└── README.md               # Proje Özeti (Bu dosya)
