import streamlit as st
import sys
import os

# src klasörünü yola ekle (import hatası almamak için)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.inference import predict

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    page_icon="🏭",
    layout="wide"
)

# --- BAŞLIK ---
st.title("🏭 Fabrika Bakım Paneli")
st.markdown("""
Bu sistem, makine sensör verilerini analiz ederek **olası arızaları önceden tahmin eder.**
""")

# --- SOL PANEL (INPUTLAR) ---
st.sidebar.header("⚙️ Sensör Verileri")
st.sidebar.info("Aşağıdaki değerleri değiştirerek simülasyon yapabilirsiniz.")

# Kullanıcı Girişleri
air_temp = st.sidebar.slider("Hava Sıcaklığı [K]", 295.0, 305.0, 300.0)
process_temp = st.sidebar.slider("İşlem Sıcaklığı [K]", 305.0, 315.0, 310.0)
rpm = st.sidebar.number_input("Dönüş Hızı [rpm]", 1000, 3000, 1500)
torque = st.sidebar.slider("Tork [Nm]", 10.0, 100.0, 40.0)
tool_wear = st.sidebar.slider("Alet Aşınması [dk]", 0, 300, 100)
type_val = st.sidebar.selectbox("Ürün Kalite Tipi", ['L', 'M', 'H'])

# --- TAHMİN BUTONU ---
if st.sidebar.button("🔍 DURUMU ANALİZ ET"):
    
    # Girdileri paketle
    input_data = {
        'Type': type_val,
        'Air temperature [K]': air_temp,
        'Process temperature [K]': process_temp,
        'Rotational speed [rpm]': rpm,
        'Torque [Nm]': torque,
        'Tool wear [min]': tool_wear
    }
    
    # Tahmin Al (inference.py dosyasındaki fonksiyonu çağır)
    result, prob = predict(input_data)
    
    # --- SONUÇ EKRANI ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Analiz Sonucu")
        if result == 1:
            st.error("🔴 RİSKLİ DURUM TESPİT EDİLDİ!")
            st.markdown(f"**Arıza Olasılığı:** %{prob*100:.2f}")
            st.warning("⚠️ **ÖNERİ:** Makineyi durdurun ve bakım ekibini yönlendirin.")
        else:
            st.success("🟢 MAKİNE SAĞLAM")
            st.markdown(f"**Arıza Olasılığı:** %{prob*100:.2f}")
            st.info("✅ **ÖNERİ:** Üretime devam edilebilir.")
            
    with col2:
        st.subheader("📈 Kritik Metrikler")
        # Hesaplanan değerleri gösterelim (Kullanıcı bunları görmedi ama model kullandı)
        power = torque * rpm * (2 * 3.14159 / 60)
        strain = torque * tool_wear
        
        st.metric("Hesaplanan Güç (Power)", f"{power:.2f} W")
        st.metric("Zorlanma İndeksi (Strain)", f"{strain:.0f}")
        
else:
    st.info("👈 Lütfen sol panelden değerleri girip 'Analiz Et' butonuna basın.")