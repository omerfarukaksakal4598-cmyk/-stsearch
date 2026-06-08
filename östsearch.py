import streamlit as st
import sqlite3
from googlesearch import search

# 1. VERİBATANI AYARLARI (Kısayolları kalıcı saklamak için)
conn = sqlite3.connect("ostsearch_browser.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS kisayollar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT,
    url TEXT,
    ikon_renk TEXT
)
""")
conn.commit()

# Varsayılan kısayolları ekle (Eğer veritabanı boşsa görseldeki gibi doldurur)
c.execute("SELECT COUNT(*) FROM kisayollar")
if cursor_count := c.fetchone()[0] == 0:
    varsayilanlar = [
        ("Youtube", "https://youtube.com", "#ef4444"),
        ("Territorial.io", "https://territorial.io", "#22c55e"),
        ("streamlit", "https://streamlit.io", "#ff4b4b"),
        ("ömergpt", "https://omergpt.streamlit.app", "#a855f7"),
        ("market", "https://google.com", "#3b82f6"),
        ("Ömerflix", "https://omerflix.streamlit.app", "#e50914"),
        ("östmail", "https://ostmail.streamlit.app", "#0284c7")
    ]
    c.executemany("INSERT INTO kisayollar (ad, url, ikon_renk) VALUES (?, ?, ?)", varsayilanlar)
    conn.commit()

# Sayfa Genişlik Ayarı
st.set_page_config(page_title="Östsearch - Yeni Sekme", layout="wide", page_icon="🔍")

# 2. GÖRSELDEKİ TARAYICI VE SEKMELERİN CSS TASARIMI (image_98eae0.png ile birebir)
st.markdown("""
    <style>
    /* Tüm Sayfa Arka Planı (Görseldeki Mor/Mürdüm Tonu) */
    .stApp { background-color: #3d293a; color: white; }
    
    /* Mock Tarayıcı Üst Barı */
    .chrome-header { background-color: #2b1a27; padding: 10px; border-radius: 8px 8px 0 0; margin-bottom: 0px; }
    .chrome-tabs { display: flex; gap: 5px; margin-bottom: 5px; }
    .chrome-tab { background-color: #3d293a; padding: 6px 15px; border-radius: 8px 8px 0 0; font-size: 12px; color: #e2e8f0; min-width: 120px; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
    .chrome-tab.active { background-color: #4d374d; font-weight: bold; border-bottom: none; }
    
    /* Adres Çubuğu Satırı */
    .address-bar-row { display: flex; align-items: center; gap: 10px; background-color: #4d374d; padding: 6px; border-radius: 4px; }
    .nav-btn { color: #cbd5e1; font-size: 16px; margin: 0 4px; }
    .address-input { background-color: #3d293a; border: 1px solid #5c435c; border-radius: 20px; padding: 4px 15px; width: 100%; color: #94a3b8; font-size: 13px; }
    
    /* Yer İşaretleri Çubuğu */
    .bookmarks-bar { display: flex; gap: 15px; font-size: 12px; color: #cbd5e1; padding: 8px 5px; border-bottom: 1px solid #5c435c; margin-bottom: 40px; }
    .bookmark-item { display: flex; align-items: center; gap: 5px; cursor: pointer; }

    /* Ana Sayfa Östsearch Başlığı */
    .main-logo { font-size: 75px; font-weight: bold; text-align: center; margin-top: 30px; margin-bottom: 25px; font-family: 'Product Sans', sans-serif; letter-spacing: -2px; }
    .main-logo span:nth-child(1) { color: #ffffff; }
    
    /* Hızlı Erişim Kısayol Kartları */
    .shortcut-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 25px; margin-top: 35px; }
    .shortcut-card { display: flex; flex-direction: column; align-items: center; text-align: center; width: 85px; text-decoration: none; color: white; }
    .shortcut-icon { width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: bold; color: white; margin-bottom: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: 0.2s; }
    .shortcut-icon:hover { transform: scale(1.1); }
    .shortcut-text { font-size: 12px; color: #f1f5f9; text-overflow: ellipsis; white-space: nowrap; overflow: hidden; width: 100%; }
    
    /* Arama Sonuç Kutuları */
    .result-box { padding: 18px; margin-bottom: 15px; background-color: #2b1a27; border-radius: 10px; border-left: 5px solid #a855f7; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .result-title { font-size: 19px; font-weight: bold; color: #c084fc; text-decoration: none; }
    .result-title:hover { text-decoration: underline; }
    .result-url { font-size: 13px; color: #4ade80; margin-bottom: 6px; }
    .result-desc { font-size: 14px; color: #e2e8f0; line-height: 1.5; }
    
    /* Streamlit Input Gizleme/Uyumlaştırma */
    div[data-testid="stTextInput"] input { border-radius: 30px !important; background-color: #ffffff !important; color: #000000 !important; padding: 12px 25px !important; font-size: 16px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. MOCK TARAYICI ARAYÜZÜ (Üst Kısım)
st.markdown("""
<div class="chrome-header">
    <div class="chrome-tabs">
        <div class="chrome-tab">Python ile Görüntü...</div>
        <div class="chrome-tab active">🔍 Östsearch - Streamlit</div>
        <div class="chrome-tab">omerfarukaksakal4598...</div>
        <div class="chrome-tab">➕ Yeni Sekme</div>
    </div>
    <div class="address-bar-row">
        <span class="nav-btn">←</span> <span class="nav-btn">→</span> <span class="nav-btn">↻</span>
        <div class="address-input">https://ostsearch.streamlit.app/</div>
    </div>
</div>
<div class="bookmarks-bar">
    <div class="bookmark-item">🛠️ Uygulamalar</div>
    <div class="bookmark-item">🌐 Chrome Web Mağazası</div>
    <div class="bookmark-item">💬 WhatsApp Web</div>
    <div class="bookmark-item">🎬 Netflix Türkiye</div>
    <div class="bookmark-item">🏫 EBA, EBATV</div>
    <div class="bookmark-item">🚀 ÖmerGPT Ultra</div>
</div>
""", unsafe_allow_html=True)

# 4. ORTA LOGO
st.markdown("<div class='main-logo'><span>Östsearch</span></div>", unsafe_allow_html=True)

# 5. CHROME ENTEGRASYONU (URL Parametresi)
if "q" in st.query_params:
    varsayilan_arama = st.query_params["q"]
else:
    varsayilan_arama = ""

# Arama Formu (Enter'a basınca tetiklenmesi için form içine aldık)
with st.form("search_form", clear_on_submit=False):
    arama_kelimesi = st.text_input("", value=varsayilan_arama, placeholder="Östsearch'te arayın veya URL yazın...", label_visibility="collapsed")
    submit_button = st.form_submit_button("Ara", use_container_width=True)

# 6. ARAMA TETİKLENDİĞİNDE SONUÇLARI GÖSTERME
if arama_kelimesi or submit_button:
    st.query_params["q"] = arama_kelimesi
    st.markdown(f"### 🔎 **'{arama_kelimesi}'** İçin Arama Sonuçları:")
    
    try:
        sonuclar = search(arama_kelimesi, num_results=10, lang="tr", advanced=True)
        for sonuc in sonuclar:
            st.markdown(f"""
            <div class='result-box'>
                <div class='result-url'>{sonuc.url}</div>
                <a href="{sonuc.url}" target="_blank" class='result-title'>{sonuc.title}</a>
                <div class='result-desc'>{sonuc.description}</div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error("Arama sonuçları alınırken bir hata oluştu. Lütfen daha sonra tekrar deneyin.")

# 7. HIZLI ERİŞİM KISAYOLLARI (Görseldeki alt butonlar)
else:
    st.markdown("<div class='shortcut-grid'>", unsafe_allow_html=True)
    
    c.execute("SELECT id, ad, url, ikon_renk FROM kisayollar")
    akis_kisayollar = c.fetchall()
    
    cols = st.columns(len(akis_kisayollar) + 1 if len(akis_kisayollar) < 8 else 8)
    
    for idx, (k_id, ad, url, renk) in enumerate(akis_kisayollar):
        with cols[idx % 8]:
            ilk_harf = ad[0].upper()
            st.markdown(f"""
                <a href="{url}" target="_blank" class="shortcut-card">
                    <div class="shortcut-icon" style="background-color: {renk};">{ilk_harf}</div>
                    <div class="shortcut-text">{ad}</div>
                </a>
            """, unsafe_allow_html=True)
            
    # "Kısayol Ekle" Buton Simülasyonu
    with cols[len(akis_kisayollar) % 8]:
        st.markdown("""
            <div class="shortcut-card" style="cursor: pointer;">
                <div class="shortcut-icon" style="background-color: #5c435c; border: 2px dashed #cbd5e1;">+</div>
                <div class="shortcut-text">Kısayol Ekle</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.write("<br><br><br>", unsafe_allow_html=True)

# 8. YÖNETİM PANELİ (Görseldeki "Chrome'u Özelleştir" işlevi)
with st.expander("⚙️ Östsearch Arayüzünü Özelleştir"):
    tab1, tab2 = st.tabs(["➕ Yeni Kısayol Ekle", "🗑️ Mevcut Kısayolları Sil"])
    
    with tab1:
        yeni_ad = st.text_input("Kısayol Adı")
        yeni_url = st.text_input("Kısayol Linki (URL)")
        secilen_renk = st.color_picker("İkon Yuvarlak Rengi", "#3b82f6")
        
        if st.button("Sisteme Kaydet"):
            if yeni_ad and yeni_url:
                if not yeni_url.startswith(("http://", "https://")):
                    yeni_url = "https://" + yeni_url
                c.execute("INSERT INTO kisayollar (ad, url, ikon_renk) VALUES (?, ?, ?)", (yeni_ad, yeni_url, secilen_renk))
                conn.commit()
                st.success(f"'{yeni_ad}' başarıyla ana sayfa hızlı erişimine eklendi!")
                st.rerun()
            else:
                st.error("Lütfen tüm alanları doldurun!")
                
    with tab2:
        c.execute("SELECT id, ad FROM kisayollar")
        silme_listesi = c.fetchall()
        if silme_listesi:
            silinecek_secim = st.selectbox("Silmek istediğiniz kısayolu seçin:", [ad for k_id, ad in silme_listesi])
            if st.button("Kısayolu Kaldır", type="primary"):
                c.execute("DELETE FROM kisayollar WHERE ad=?", (silinecek_secim,))
                conn.commit()
                st.success(f"'{silinecek_secim}' başarıyla kaldırıldı.")
                st.rerun()
        else:
            st.info("Kaldırılacak kısayol bulunamadı.")
