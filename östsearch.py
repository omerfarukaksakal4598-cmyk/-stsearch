import streamlit as st
import sqlite3
from googlesearch import search

# 1. VERİBATANI AYARLARI (Kısayollar için)
conn = sqlite3.connect("ostsearch_browser_v2.db", check_same_thread=False)
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

# Veritabanı boşsa varsayılan kısayolları yükle
c.execute("SELECT COUNT(*) FROM kisayollar")
if c.fetchone()[0] == 0:
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

# Sayfa Ayarları
st.set_page_config(page_title="Östsearch - Yeni Sekme", layout="wide", page_icon="🔍")

# URL'den gelen güncel arama parametresini alalım
aktif_sorgu = st.query_params.get("q", "")

# 2. GELİŞMİŞ GÖRSEL TASARIM (CSS)
st.markdown("""
    <style>
    /* Arka Plan Tonu */
    .stApp { background-color: #3d293a; color: white; }
    
    /* Sekme Tasarımları */
    .chrome-header { background-color: #2b1a27; padding: 10px 10px 5px 10px; border-radius: 8px 8px 0 0; }
    .chrome-tabs { display: flex; gap: 5px; margin-bottom: 5px; }
    .chrome-tab { background-color: #2b1a27; padding: 8px 20px; border-radius: 8px 8px 0 0; font-size: 13px; color: #cbd5e1; text-decoration: none; }
    .chrome-tab.active { background-color: #3d293a; font-weight: bold; color: white; }
    .chrome-tab:hover:not(.active) { background-color: #4d374d; color: white; }
    
    /* Yer İşaretleri */
    .bookmarks-bar { display: flex; gap: 18px; font-size: 12px; color: #cbd5e1; padding: 8px 15px; border-bottom: 1px solid #5c435c; margin-bottom: 30px; background-color: #2b1a27; border-radius: 0 0 8px 8px; }
    
    /* Büyük Logo */
    .main-logo { font-size: 75px; font-weight: bold; text-align: center; margin-top: 50px; margin-bottom: 30px; font-family: 'Product Sans', sans-serif; }
    
    /* Kısayol Kartları */
    .shortcut-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 25px; margin-top: 35px; }
    .shortcut-card { display: flex; flex-direction: column; align-items: center; text-align: center; width: 85px; text-decoration: none; color: white; }
    .shortcut-icon { width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: bold; color: white; margin-bottom: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: 0.2s; }
    .shortcut-icon:hover { transform: scale(1.1); }
    .shortcut-text { font-size: 12px; color: #f1f5f9; text-overflow: ellipsis; white-space: nowrap; overflow: hidden; width: 100%; }
    
    /* Sonuç Kutuları */
    .result-box { padding: 18px; margin-bottom: 15px; background-color: #2b1a27; border-radius: 10px; border-left: 5px solid #c084fc; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .result-title { font-size: 19px; font-weight: bold; color: #c084fc; text-decoration: none; }
    .result-title:hover { text-decoration: underline; }
    .result-url { font-size: 13px; color: #4ade80; margin-bottom: 6px; }
    .result-desc { font-size: 14px; color: #e2e8f0; line-height: 1.5; }
    
    /* Streamlit Input Alanlarını Tarayıcı Çubuğuna Benzetme */
    .address-col div[data-testid="stTextInput"] input { background-color: #3d293a !important; color: #ffffff !important; border: 1px solid #5c435c !important; border-radius: 20px !important; padding: 4px 15px !important; }
    .center-search div[data-testid="stTextInput"] input { background-color: #ffffff !important; color: #000000 !important; border-radius: 30px !important; padding: 12px 25px !important; font-size: 16px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. TARAYICI ÜST BARU (İstediğin Düzenlemeler Yapıldı)
st.markdown('<div class="chrome-header">', unsafe_allow_html=True)
tabs_html = """
<div class="chrome-tabs">
    <a href="#" class="chrome-tab active">🔍 Östsearch - Streamlit</a>
    <a href="https://ostsearch.streamlit.app/" target="_self" class="chrome-tab">➕ Yeni Sekme</a>
</div>
"""
st.markdown(tabs_html, unsafe_allow_html=True)

# Adres Çubuğunu Gerçek Bir Input Yapıyoruz
cols_nav = st.columns([1, 8])
with cols_nav[0]:
    st.markdown("<div style='margin-top: 5px; color: #cbd5e1;'>&nbsp;&nbsp;← &nbsp; → &nbsp; ↻</div>", unsafe_allow_html=True)

with cols_nav[1]:
    st.markdown('<div class="address-col">', unsafe_allow_html=True)
    adres_girdisi = st.text_input(
        "Address Bar", 
        value=aktif_sorgu if aktif_sorgu else "https://ostsearch.streamlit.app/", 
        key="address_bar_input", 
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Yer İşaretleri Çubuğu
st.markdown("""
<div class="bookmarks-bar">
    <div>🛠️ Uygulamalar</div><div>🌐 Chrome Web Mağazası</div><div>💬 WhatsApp Web</div><div>🎬 Netflix Türkiye</div><div>🏫 EBA, EBATV</div><div>🚀 ÖmerGPT Ultra</div>
</div>
""", unsafe_allow_html=True)

# Eğer adres çubuğuna link değil de arama kelimesi yazılıp Enter'a basıldıysa parametreyi güncelle
if adres_girdisi and adres_girdisi != "https://ostsearch.streamlit.app/" and adres_girdisi != aktif_sorgu:
    # Kullanıcı doğrudan temiz kelime yazdıysa veya URL'yi değiştirdiyse tetiklenir
    st.query_params["q"] = adres_girdisi
    st.rerun()

# 4. DURUM KONTROLÜ (Arama Yapıldı mı?)
if aktif_sorgu and aktif_sorgu != "https://ostsearch.streamlit.app/":
    # --- SADECE ARAMA SONUÇLARI EKRANI ---
    st.markdown(f"### 🔎 **'{aktif_sorgu}'** için arama sonuçları:")
    st.write("---")
    
    try:
        sonuclar = search(aktif_sorgu, num_results=10, lang="tr", advanced=True)
        for sonuc in sonuclar:
            st.markdown(f"""
            <div class='result-box'>
                <div class='result-url'>{sonuc.url}</div>
                <a href="{sonuc.url}" target="_blank" class='result-title'>{sonuc.title}</a>
                <div class='result-desc'>{sonuc.description}</div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error("Google sunucularından sonuçlar alınırken bir sorun oluştu.")

else:
    # --- ANA SAYFA (YENİ SEKME) EKRANI ---
    st.markdown("<div class='main-logo'>Östsearch</div>", unsafe_allow_html=True)
    
    # Merkezdeki Büyük Arama Çubuğu
    st.markdown('<div class="center-search">', unsafe_allow_html=True)
    merkez_girdisi = st.text_input("Search", placeholder="Östsearch'te arayın veya URL yazın...", key="center_search_input", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if merkez_girdisi:
        st.query_params["q"] = merkez_girdisi
        st.rerun()
        
    # Hızlı Erişim Kısayolları
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
            
    # Sabit Kısayol Ekleme Görseli
    with cols[len(akis_kisayollar) % 8]:
        st.markdown("""
            <div class="shortcut-card" style="opacity: 0.7;">
                <div class="shortcut-icon" style="background-color: #5c435c; border: 2px dashed #cbd5e1;">+</div>
                <div class="shortcut-text">Kısayol Ekle</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Özelleştirme Paneli (Sayfa düzenini bozmamak için en altta gizlenebilir kutuda)
    st.write("<br><br>", unsafe_allow_html=True)
    with st.expander("⚙️ Kısayolları Özelleştir (Ekle / Sil)"):
        tab1, tab2 = st.tabs(["➕ Ekle", "🗑️ Sil"])
        with tab1:
            y_ad = st.text_input("Site Adı")
            y_url = st.text_input("Site URL")
            y_renk = st.color_picker("İkon Rengi", "#3b82f6")
            if st.button("Kaydet"):
                if y_ad and y_url:
                    if not y_url.startswith(("http://", "https://")):
                        y_url = "https://" + y_url
                    c.execute("INSERT INTO kisayollar (ad, url, ikon_renk) VALUES (?, ?, ?)", (y_ad, y_url, y_renk))
                    conn.commit()
                    st.rerun()
        with tab2:
            c.execute("SELECT ad FROM kisayollar")
            mevcutlar = [row[0] for row in c.fetchall()]
            silinecek = st.selectbox("Silinecek Kısayol", mevcutlar)
            if st.button("Kaldır", type="primary"):
                c.execute("DELETE FROM kisayollar WHERE ad=?", (silinecek,))
                conn.commit()
                st.rerun()
