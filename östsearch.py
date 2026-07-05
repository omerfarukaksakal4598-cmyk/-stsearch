import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Sayfa yapılandırması
st.set_page_config(
    page_title="östsearch",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stMetric"] {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    
    .search-result {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 5px solid #FF6B35;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .result-title {
        font-size: 18px;
        font-weight: bold;
        color: #1f1f1f;
        margin-bottom: 8px;
    }
    
    .result-url {
        color: #0066cc;
        font-size: 12px;
        margin-bottom: 10px;
    }
    
    .result-description {
        color: #555;
        font-size: 14px;
        line-height: 1.5;
    }
    
    .filter-box {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    
    .header-container {
        text-align: center;
        padding: 30px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
    }
    
    .header-title {
        font-size: 48px;
        font-weight: bold;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .header-subtitle {
        font-size: 16px;
        margin-top: 10px;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Örnek veri seti
@st.cache_data
def get_sample_data():
    data = [
        {
            "title": "Python Programlama Rehberi",
            "url": "https://example.com/python-guide",
            "description": "Python programlamasının temellerini öğrenin. Değişkenler, döngüler, fonksiyonlar ve daha fazlası.",
            "category": "Eğitim",
            "date": "2024-01-15"
        },
        {
            "title": "Web Geliştirme ile Django",
            "url": "https://example.com/django",
            "description": "Django framework kullanarak modern web uygulamaları geliştirin. REST API'lar oluşturun.",
            "category": "Yazılım",
            "date": "2024-01-10"
        },
        {
            "title": "Veri Analizi Pandas ile",
            "url": "https://example.com/pandas",
            "description": "Pandas kütüphanesi ile veri analizi yapın. Veri temizleme ve dönüştürme teknikleri.",
            "category": "Veri Bilimi",
            "date": "2024-01-08"
        },
        {
            "title": "Makine Öğrenmesi Başlangıcı",
            "url": "https://example.com/ml-intro",
            "description": "Scikit-learn ile makine öğrenmesi modellerini eğitin ve değerlendirin.",
            "category": "Yapay Zeka",
            "date": "2024-01-05"
        },
        {
            "title": "API Tasarımı Best Practices",
            "url": "https://example.com/api-design",
            "description": "RESTful API'ları tasarlama ve geliştirme için en iyi uygulamalar.",
            "category": "Yazılım",
            "date": "2024-01-01"
        },
        {
            "title": "Streamlit ile Hızlı Uygulamalar",
            "url": "https://example.com/streamlit",
            "description": "Python ile etkileşimli web uygulamaları oluşturun. Streamlit framework'ünü öğrenin.",
            "category": "Yazılım",
            "date": "2023-12-28"
        }
    ]
    return data

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🔍 östsearch</h1>
    <p class="header-subtitle">Akıllı Arama Motoru</p>
</div>
""", unsafe_allow_html=True)

# Ana arama kutusu
col1, col2 = st.columns([4, 1])
with col1:
    search_query = st.text_input(
        "Ara",
        placeholder="Aranacak kelime veya konuyu girin...",
        label_visibility="collapsed"
    )
with col2:
    search_button = st.button("🔍 Ara", use_container_width=True)

st.divider()

# Kenar çubuğu - Filtreler
st.sidebar.title("⚙️ Filtreler")

# Veri yükle
data = get_sample_data()
categories = sorted(list(set([item["category"] for item in data])))

# Kategori filtresi
selected_category = st.sidebar.selectbox(
    "Kategori",
    ["Tümü"] + categories,
    index=0
)

# Tarih aralığı filtresi
st.sidebar.write("**Tarih Aralığı**")
date_filter = st.sidebar.slider(
    "Son kaç gün içinde",
    0, 60, 60,
    label_visibility="collapsed"
)

# Sıralama seçeneği
sort_option = st.sidebar.radio(
    "Sırala",
    ["En Yeni", "İlişkili", "En Popüler"],
    index=1
)

st.sidebar.divider()

# İstatistikler
st.sidebar.write("**İstatistikler**")
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.metric("Toplam Sonuç", len(data))
with col2:
    st.metric("Kategoriler", len(categories))
with col3:
    st.metric("Sürüm", "1.0")

# Arama ve filtreleme işlevi
def filter_data(data, query, category, days):
    filtered = data
    
    # Kategori filtresi
    if category != "Tümü":
        filtered = [item for item in filtered if item["category"] == category]
    
    # Tarih filtresi
    if days < 60:
        cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=days)
        filtered = [
            item for item in filtered 
            if pd.Timestamp(item["date"]) >= cutoff_date
        ]
    
    # Arama sorgusu filtresi
    if query:
        query_lower = query.lower()
        filtered = [
            item for item in filtered
            if query_lower in item["title"].lower() or 
               query_lower in item["description"].lower()
        ]
    
    return filtered

# Sonuçları göster
if search_button or search_query:
    results = filter_data(data, search_query, selected_category, date_filter)
    
    # Başlık ve sayı
    st.subheader(f"📊 Sonuçlar: {len(results)} bulundu")
    
    if results:
        for result in results:
            st.markdown(f"""
            <div class="search-result">
                <div class="result-title">{result['title']}</div>
                <div class="result-url">🔗 {result['url']}</div>
                <div class="result-description">{result['description']}</div>
                <div style="margin-top: 10px; font-size: 12px; color: #888;">
                    📁 {result['category']} · 📅 {result['date']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("😔 Arama kriterlerine uygun sonuç bulunamadı. Lütfen farklı arama terimlerini deneyin.")

else:
    # Başlık sayfası
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px;">
        <h2 style="color: #667eea;">Hoş Geldiniz!</h2>
        <p style="font-size: 16px; color: #666;">
            Yukarıdaki arama kutusunu kullanarak istediğiniz konuyu arayın.
        </p>
        <p style="font-size: 14px; color: #999;">
            Filtreler bölümünden kategori ve tarih aralığını belirtebilirsiniz.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Popüler konular
    st.divider()
    st.write("**🔥 Popüler Konular**")
    
    col1, col2, col3 = st.columns(3)
    
    topics = [
        {"emoji": "🐍", "name": "Python", "count": "12 sonuç"},
        {"emoji": "🌐", "name": "Web Dev", "count": "8 sonuç"},
        {"emoji": "📊", "name": "Veri Bilimi", "count": "6 sonuç"}
    ]
    
    for col, topic in zip([col1, col2, col3], topics):
        with col:
            if st.button(f"{topic['emoji']} {topic['name']}", use_container_width=True):
                st.session_state.search_query = topic['name']
                st.rerun()

# Alt bilgi
st.divider()
st.markdown("""
<div style="text-align: center; color: #999; font-size: 12px; padding: 20px;">
    <p>östsearch © 2024 | Akıllı Arama Teknolojisi</p>
</div>
""", unsafe_allow_html=True)
