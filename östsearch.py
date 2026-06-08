import streamlit as st
from googlesearch import search

# Sayfa Ayarları
st.set_page_config(page_title="Östsearch", page_icon="🔍", layout="centered")

# Arama Motoru Tasarımı
st.markdown("""
    <style>
    .search-title { font-size: 50px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    /* Östsearch (9 harf) için renk döngüsü */
    .search-title span:nth-child(1) { color: #4285F4; } /* Ö - Mavi */
    .search-title span:nth-child(2) { color: #EA4335; } /* s - Kırmızı */
    .search-title span:nth-child(3) { color: #FBBC05; } /* t - Sarı */
    .search-title span:nth-child(4) { color: #4285F4; } /* s - Mavi */
    .search-title span:nth-child(5) { color: #34A853; } /* e - Yeşil */
    .search-title span:nth-child(6) { color: #EA4335; } /* a - Kırmızı */
    .search-title span:nth-child(7) { color: #FBBC05; } /* r - Sarı */
    .search-title span:nth-child(8) { color: #34A853; } /* c - Yeşil */
    .search-title span:nth-child(9) { color: #4285F4; } /* h - Mavi */
    
    .result-box { padding: 15px; margin-bottom: 15px; background-color: #1e1e1e; border-radius: 8px; border-left: 4px solid #4285F4; }
    .result-title { font-size: 20px; font-weight: bold; color: #8ab4f8; text-decoration: none; }
    .result-url { font-size: 14px; color: #81c995; margin-bottom: 5px; }
    .result-desc { font-size: 14px; color: #e8eaed; }
    </style>
""", unsafe_allow_html=True)

# Logo
st.markdown("""
    <div class='search-title'>
        <span>Ö</span><span>s</span><span>t</span><span>s</span><span>e</span><span>a</span><span>r</span><span>c</span><span>h</span>
    </div>
""", unsafe_allow_html=True)

# --- CHROME ENTEGRASYONU: URL'den gelen aramayı yakalama ---
if "q" in st.query_params:
    baslangic_aramasi = st.query_params["q"]
else:
    baslangic_aramasi = ""

# Arama Kutusu
arama_kelimesi = st.text_input("Östsearch'te Ara veya URL girin", value=baslangic_aramasi, label_visibility="collapsed")

if arama_kelimesi:
    st.query_params["q"] = arama_kelimesi
    
    st.write("---")
    st.caption(f"🔎 **'{arama_kelimesi}'** için sonuçlar getiriliyor...")
    
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
        st.error("Arama sunucularına bağlanırken bir hata oluştu. Lütfen biraz sonra tekrar dene.")