# Predictive Maintenance Projesi Final Raporu

**Veri Seti:** UCI AI4I 2020 Predictive Maintenance Dataset

---

## 1. Problem Tanımı ve Veri Analizi (EDA)

**Problem:** Üretim hattındaki makinelerin sensör verilerini (sıcaklık, tork, hız vb.) kullanarak, makine bozulmadan önce arızayı tespit etmek ve plansız duruşların (downtime) maliyetini önlemektir.

### Veri Analizi Bulguları (EDA Docs):
* **Sınıf Dengesizliği (Imbalance):** Veri setinde "Sağlam" sınıfı **%96.6**, "Bozuk" sınıfı ise sadece **%3.4** oranındadır. Bu durum, modelin sadece çoğunluk sınıfını ezberlemesi riskini doğurmuştur.
* **Fiziksel İlişkiler:** `Rotational speed` ve `Torque` arasında güçlü negatif korelasyon **(-0.88)** tespit edilmiştir. Arızaların (Kırmızı noktalar) genellikle Hız-Tork grafiğinin uç sınırlarında (Güç Sınırı) kümelendiği gözlemlenmiştir. 
* **Arıza Türleri:** En sık görülen arızalar **HDF** (Isınma) ve **OSF** (Aşırı Yük) kaynaklıdır. Rastgele arızalar (RNF) ihmal edilebilir düzeydedir.
* **Veri Temizliği:** Modelin "kopya çekmesini" (Data Leakage) önlemek için arıza türünü belirten sütunlar (`TWF`, `HDF`, `PWF`, `OSF`, `RNF`) eğitim setinden çıkarılmıştır.

---

## 2. Metodoloji: Baseline ve Geliştirme Süreci

### 2.1. Baseline Model
* **Model:** Logistic Regression (Varsayılan Ayarlar)
* **Özellik Seti:** Sadece ham sensör verileri (Hız, Tork, Sıcaklık).
* **Sonuç:**
    * **Accuracy:** %97 (Yanıltıcı)
    * **Recall (Arıza Yakalama):** **%10**
* **Değerlendirme:** Model, dengesiz veriyi yönetememiş ve lineer olmayan (eğrisel) arıza sınırlarını çizmekte başarısız olmuştur. **68 arızanın 61'i kaçırılmıştır.**

### 2.2. Feature Engineering (Öznitelik Mühendisliği)
Modelin fiziksel dünyayı anlaması için alan bilgisi (Domain Knowledge) kullanılarak yeni değişkenler türetilmiştir:
* **`Power_W` (Güç):** $Tork \times Hız \times K$. Makinenin harcadığı gerçek eforu gösterir.
* **`Strain` (Zorlanma):** $Tork \times Alet Aşınması$. Makinenin üzerindeki mekanik stresi ifade eder.
* **`Temp_Diff`:** İşlem ve hava sıcaklığı farkı. Isınma problemlerini (HDF) vurgular.

### 2.3. Dengesizlik Stratejisi
Azınlık sınıfını (%3.4) modelin daha iyi öğrenmesi için **SMOTE (Synthetic Minority Over-sampling Technique)** kullanılarak eğitim setindeki bozuk makine sayısı sentetik olarak artırılmış ve denge sağlanmıştır.

---

## 3. Validasyon Şeması ve Model Optimizasyonu

* **Validasyon Şeması:** Stratified Train-Test Split (%80 Eğitim - %20 Test).
* **Neden Seçildi?** Veri aşırı dengesiz olduğu için, rastgele bölme işlemi test setine hiç "Bozuk" makine düşmemesine neden olabilirdi. `Stratify` parametresi ile %3'lük arıza oranının hem eğitim hem test setinde korunması garanti altına alındı.

### Optimizasyon (GridSearch):
* **Denenen Modeller:** Random Forest
* **Parametreler:** `n_estimators` [100, 200], `max_depth` [10, 20, None].
* **En İyi Sonuç:** 200 Ağaç, Derinlik Sınırı Yok (`None`).

---

## 4. Final Model ve Pipeline Seçimi

**Seçilen Model:** **Random Forest Classifier**

**Neden Seçildi?**
1.  **Non-Linearity:** Hız ve Tork arasındaki eğrisel ilişkiyi, karar ağaçları yapısı sayesinde daha iyi modellemiştir.
2.  **Kararlılık (Stability):** Gürültülü verilere karşı dirençlidir ve Overfitting riski (doğru parametrelerle) düşüktür.
3.  **Feature Importance:** Hangi sensörün arızaya neden olduğunu açıklayabilmektedir.

**Final Feature Seti:**
Model eğitiminde en yüksek katkıyı sağlayan özellikler:
* `Torque [Nm]`
* `Power_W` (Türetilmiş)
* `Rotational speed [rpm]`
* `Strain` (Türetilmiş)
* `Tool wear [min]`

---

## 5. Performans Karşılaştırması (Baseline vs Final)

Yapılan mühendislik çalışmaları sonucunda elde edilen başarı artışı:

| Metrik | Baseline (Logistic Reg.) | Final Model (Random Forest + SMOTE) | Değişim |
| :--- | :--- | :--- | :--- |
| **Recall (Arıza Yakalama)** | %10 | **%85.3** | 🔼 **+75 Puan** |
| **Kaçırılan Arıza (FN)** | 61 Adet | **10 Adet** | 📉 Risk %83 Azaldı |
| **ROC-AUC** | 0.90 | **0.98** | 🔼 Mükemmel Ayrım |

---

## 6. Business (İş) Uyumluluğu ve Açıklanabilirlik

* **Business Gereksinimi:** Fabrika ortamında bir makinenin durması (Downtime) çok maliyetlidir. Bu yüzden modelin arızaları kaçırmaması (Yüksek Recall) önceliklidir.
* **Uyumluluk:** Modelimiz **%85 Recall** ile arızaların büyük çoğunluğunu önceden yakalayarak bu gereksinimi karşılar.
* **SHAP Analizi:** Modelin kararları "Kara Kutu" değildir. Force Plot analizleri ile operatöre *"Bu makine bozulacak çünkü Tork değeri 65 Nm üzerine çıktı"* şeklinde fiziksel, mantıklı ve güvenilir açıklamalar sunulmaktadır. 

---

## 7. Canlıya Alma ve İzleme

* **Canlıya Çıkış Stratejisi:** Model `maintenance_model.pkl` olarak serileştirilmiş ve bir **Streamlit** web arayüzü ile sunulmuştur. Gerçek senaryoda bu yapı bir REST API (Flask/FastAPI) arkasında mikroservis olarak çalışacaktır.

### İzlenmesi Gereken Metrikler (Monitoring):
Model canlıya alındıktan sonra şu durumlar takip edilmelidir:
1.  **Data Drift (Veri Kayması):** Sensörlerden gelen Tork veya Sıcaklık ortalamaları zamanla değişiyor mu? (Örn: Yazın sıcaklık artışı).
2.  **Recall Düşüşü:** Modelin sahadaki gerçek arızaları yakalama oranı düşüyor mu?
3.  **Concept Drift:** Makine arıza tipleri değişiyor mu? (Örn: Yeni bir bıçak türü kullanılmaya başlandıysa model güncellenmelidir).