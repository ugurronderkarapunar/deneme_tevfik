import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Sayfa Ayarları
st.set_page_config(
    page_title="Filo & Personel Operasyon Paneli",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS (Daha modern ve kurumsal görünüm için)
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #0068c9;
    }
    </style>
""", unsafe_allow_html=True)

# --- ÖRNEK VERİ SETLERİ (İleride Excel'den pd.read_excel() ile çekilecek) ---
@st.cache_data
def load_sample_data():
    # 1. Aktif Gemi ve Personel Verisi
    df_personel = pd.DataFrame({
        "Gemi Adı": ["M/V Moda", "M/V Moda", "M/V Beşiktaş", "M/V Kadıköy", "M/V Karaköy", "M/V Sarıyer"],
        "Personel Adı": ["Ahmet Yılmaz", "Mehmet Demir", "Caner Kaya", "Burak Özkan", "Emre Şahin", "Serkan Arslan"],
        "Görevi": ["Kaptan", "Başmühendis", "Güverte Lostromosu", "Kaptan", "Yağcı", "Çımacı"],
        "İşbaşı Tarihi": ["2026-10-01", "2026-10-15", "2026-11-01", "2026-09-20", "2026-11-05", "2026-10-10"],
        "İzin Bilgisi": ["Aktif Görevde", "Aktif Görevde", "Yıllık İzin (18-25 Kas)", "Aktif Görevde", "Raporlu", "Aktif Görevde"],
        "İzin Bitiş": ["-", "-", "2026-11-25", "-", "2026-11-20", "-"]
    })

    # 2. Gemiye Katılacak (Planlanan) Personel
    df_katilacak = pd.DataFrame({
        "Katılacak Gemi": ["M/V Beşiktaş", "M/V Karaköy", "M/V Moda"],
        "Personel Adı": ["Hakan Çelik", "Volkan Yıldız", "Oğuzhan Aydın"],
        "Görevi": ["Güverte Lostromosu (Yedek)", "Yağcı (Yedek)", "Miço"],
        "Planlanan Katılış Tarihi": ["2026-11-18", "2026-11-19", "2026-11-22"],
        "Durum": ["Evrak Tamam", "STCW Yenileme Bekliyor", "Onaylandı"]
    })

    # 3. Tersanedeki Gemiler
    df_tersane = pd.DataFrame({
        "Gemi Adı": ["M/V Eminönü", "M/V Üsküdar"],
        "Tersane Adı": ["Haliç Tersanesi", "Tuzla Tersanesi"],
        "Giriş Tarihi": ["2026-10-25", "2026-11-02"],
        "Tahmini Çıkış": ["2026-11-28", "2026-12-15"],
        "Bakım Türü": ["Havuzlama & Pervane Bakımı", "Ana Makine Revizyonu"],
        "Sorumlu Mühendis": ["Selim Korkmaz", "Deniz Aksoy"]
    })

    # 4. Nöbet Listesi
    df_nobet = pd.DataFrame({
        "Tarih": ["2026-11-17", "2026-11-17", "2026-11-18", "2026-11-18"],
        "Vardiya": ["Gündüz (08:00-20:00)", "Gece (20:00-08:00)", "Gündüz (08:00-20:00)", "Gece (20:00-08:00)"],
        "Gemi / Lokasyon": ["M/V Moda", "Haliç Tersanesi (M/V Eminönü)", "M/V Kadıköy", "M/V Beşiktaş"],
        "Nöbetçi Personel": ["Ahmet Yılmaz", "Selim Korkmaz", "Burak Özkan", "Hakan Çelik"],
        "İletişim": ["0555-000-01", "0555-000-02", "0555-000-03", "0555-000-04"]
    })

    return df_personel, df_katilacak, df_tersane, df_nobet

df_personel, df_katilacak, df_tersane, df_nobet = load_sample_data()

# --- SOL MENÜ (NAVİGASYON) ---
with st.sidebar:
    st.title("🚢 Filo Operasyon")
    st.caption("Denizcilik Personel & Vardiya Yönetim Sistemi")
    st.divider()
    
    sayfa = st.radio(
        "Modüller",
        [
            "📊 Genel Bakış (Dashboard)",
            "👨‍✈️ Gemi & Personel Listesi",
            "🔄 Katılacak Personel Planı",
            "🏗️ Tersanedeki Gemiler",
            "🛡️ Nöbet Listesi",
            "🤖 AI Operasyon Asistanı (Beta)"
        ]
    )
    
    st.divider()
    st.info("💡 **Veri Kaynağı:** Şu an prototip verileri aktif. Excel yükleme modülü sonraki adımda bağlanacaktır.")

# --- SAYFA 1: GENEL BAKIŞ ---
if sayfa == "📊 Genel Bakış (Dashboard)":
    st.title("📊 Operasyonel Durum Özeti")
    st.markdown(f"**Tarih:** {datetime.now().strftime('%d.%m.%Y')} | **Sistem Durumu:** Aktif")
    
    # Üst Bilgi Kartları (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Aktif Personel", len(df_personel[df_personel["İzin Bilgisi"] == "Aktif Görevde"]), "Görev Başında")
    col2.metric("İzinli / Raporlu", len(df_personel[df_personel["İzin Bilgisi"] != "Aktif Görevde"]), "-2 Eksik", delta_color="inverse")
    col3.metric("Katılacak Personel", len(df_katilacak), "Bu Hafta")
    col4.metric("Tersanedeki Gemiler", len(df_tersane), "Bakımda")

    st.divider()

    # Hızlı Kritik Uyarılar
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("⚠️ Kritik Operasyon Uyarıları")
        st.warning("**M/V Beşiktaş:** Caner Kaya (Güverte Lostromosu) yıllık izinde. Yerine **Hakan Çelik** yarın (18 Kas) katılıyor.")
        st.error("**Evrak Uyarısı:** M/V Karaköy'e katılacak Volkan Yıldız'ın **STCW Yenileme** süreci bekleniyor.")
    
    with col_right:
        st.subheader("🛡️ Bugünün Nöbetçileri (17.11.2026)")
        bugun_nobet = df_nobet[df_nobet["Tarih"] == "2026-11-17"]
        st.dataframe(bugun_nobet[["Vardiya", "Gemi / Lokasyon", "Nöbetçi Personel"]], use_container_width=True, hide_index=True)

# --- SAYFA 2: GEMİ & PERSONEL LİSTESİ ---
elif sayfa == "👨‍✈️ Gemi & Personel Listesi":
    st.title("👨‍✈️ Gemideki Personel & İzin Takibi")
    
    # Filtreleme Seçenekleri
    col1, col2 = st.columns(2)
    secilen_gemi = col1.multiselect("Gemi Filtrele", options=df_personel["Gemi Adı"].unique(), default=df_personel["Gemi Adı"].unique())
    secilen_durum = col2.selectbox("İzin Durumu", ["Tümü", "Sadece Aktif Görevdekiler", "İzinli / Raporlu Olanlar"])

    filtered_df = df_personel[df_personel["Gemi Adı"].isin(secilen_gemi)]
    if secilen_durum == "Sadece Aktif Görevdekiler":
        filtered_df = filtered_df[filtered_df["İzin Bilgisi"] == "Aktif Görevde"]
    elif secilen_durum == "İzinli / Raporlu Olanlar":
        filtered_df = filtered_df[filtered_df["İzin Bilgisi"] != "Aktif Görevde"]

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # Yeni Personel / İzin Güncelleme Formu (Prototip)
    with st.expander("➕ Hızlı İzin / Personel Kaydı Ekle"):
        with st.form("personel_ekle"):
            f_col1, f_col2, f_col3 = st.columns(3)
            gemi = f_col1.selectbox("Gemi Adı", ["M/V Moda", "M/V Beşiktaş", "M/V Kadıköy", "M/V Karaköy", "M/V Sarıyer"])
            ad = f_col2.text_input("Personel Adı Soyadı")
            isbasi = f_col3.date_input("İşbaşı Tarihi")
            izin = st.text_input("İzin Bilgisi", value="Aktif Görevde")
            if st.form_submit_button("Kaydet"):
                st.success(f"{ad} ({gemi}) için kayıt taslağı oluşturuldu! (Excel bağlantısı sonrası kalıcı kaydedilecek)")

# --- SAYFA 3: KATILACAK PERSONEL ---
elif sayfa == "🔄 Katılacak Personel Planı":
    st.title("🔄 Gemiye Katılacak Personel Planlaması")
    st.markdown("İzinli veya raporlu personelin yerine atanan yedek/rotasyon personeli listesi.")
    
    st.dataframe(df_katilacak, use_container_width=True, hide_index=True)

# --- SAYFA 4: TERSANEDEKİ GEMİLER ---
elif sayfa == "🏗️ Tersanedeki Gemiler":
    st.title("🏗️ Tersane & Bakım Takip Listesi")
    
    for index, row in df_tersane.iterrows():
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"### 🚢 {row['Gemi Adı']}")
            c2.markdown(f"**Tersane:** {row['Tersane Adı']}\n\n**Sorumlu:** {row['Sorumlu Mühendis']}")
            c3.markdown(f"**Giriş:** {row['Giriş Tarihi']}\n\n**Tahmini Çıkış:** {row['Tahmini Çıkış']}")
            c4.info(f"**İşlem:** {row['Bakım Türü']}")

# --- SAYFA 5: NÖBET LİSTESİ ---
elif sayfa == "🛡️ Nöbet Listesi":
    st.title("🛡️ Vardiya ve Nöbet Çizelgesi")
    
    tarih_filtre = st.date_input("Tarihe Göre Filtrele", value=datetime(2026, 11, 17))
    st.dataframe(df_nobet, use_container_width=True, hide_index=True)

# --- SAYFA 6: AI OPERASYON ASİSTANI (FDE VİTRİN MODÜLÜ) ---
elif sayfa == "🤖 AI Operasyon Asistanı (Beta)":
    st.title("🤖 AI Filo & Operasyon Asistanı")
    st.markdown("Operasyonel veriler üzerinde doğal dille sorgulama yapın ve otomatik vardiya devir özeti oluşturun.")
    
    soru = st.text_input("Asistana Sor (Örn: 'Şu an izinde olan kimler var ve yerlerine kim katılacak?')")
    if st.button("Analiz Et") and soru:
        with st.spinner("Tablolar taranıyor ve operasyonel özet hazırlanıyor..."):
            st.success("**AI Operasyon Özeti:**\n\n"
                       "1. **M/V Beşiktaş** gemisinde görevli **Caner Kaya** (25 Kasım'a kadar yıllık izinde). Yerine **18 Kasım'da Hakan Çelik** katılacak (Evrakları tamam).\n"
                       "2. **M/V Karaköy** gemisinde görevli **Emre Şahin** raporlu (20 Kasım'a kadar). Yerine planlanan **Volkan Yıldız** için *STCW Yenileme* onayı bekleniyor.\n"
                       "3. **Öneri:** Volkan Yıldız'ın evrak süreci yarın öğlene kadar tamamlanmazsa yedek havuzundan atama yapılmalıdır.")
