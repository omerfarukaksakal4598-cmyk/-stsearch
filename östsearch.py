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
    * {
        color: #e0e0e0;
    }
    
    .stMainBlockContainer {
        background-color: #0a0e27;
    }
    
    [data-testid="stMetric"] {
        background-color: #1a1f3a;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    [data-testid="stMetricValue"] {
        color: #667eea;
    }
    
    .search-result {
        background-color: #1a1f3a;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 5px solid #FF6B35;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    
    .result-title {
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 8px;
    }
    
    .result-url {
        color: #667eea;
        font-size: 12px;
        margin-bottom: 10px;
    }
    
    .result-description {
        color: #b0b0b0;
        font-size: 14px;
        line-height: 1.5;
    }
    
    .filter-box {
        background-color: #1a1f3a;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2a2f4a;
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
    
    .stSidebar {
        background-color: #0f1428;
    }
    
    .stTextInput > div > div > input {
        background-color: #1a1f3a;
        color: #e0e0e0;
        border: 1px solid #2a2f4a;
    }
    
    .stButton > button {
        background-color: #667eea;
        color: white;
        border: none;
    }
    
    .stButton > button:hover {
        background-color: #764ba2;
    }
    
    .stSelectbox, .stRadio, .stSlider {
        color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Örnek veri seti
@st.cache_data
def get_sample_data():
    data = [
        # YouTube İçerikleri
        {
            "title": "YouTube Video Editlemesi Rehberi",
            "url": "https://youtube.com/watch?v=example1",
            "description": "Adobe Premiere Pro ve DaVinci Resolve kullanarak profesyonel video editleme. Renk düzeltme, geçişler ve efektler.",
            "category": "Video",
            "date": "2024-01-20"
        },
        {
            "title": "YouTube Kanalı Başlama 2024",
            "url": "https://youtube.com/watch?v=example2",
            "description": "Sıfırdan YouTube kanalı açma, SEO optimizasyonu, izleyici kazanma stratejileri.",
            "category": "İçerik Oluşturucu",
            "date": "2024-01-18"
        },
        {
            "title": "YouTube Monetizasyon Stratejileri",
            "url": "https://youtube.com/watch?v=example3",
            "description": "YouTube Partner Program, sponsorlu içerik, afiliasyon pazarlaması ve gelir artırma yolları.",
            "category": "İş",
            "date": "2024-01-16"
        },
        
        # Teknoloji
        {
            "title": "Apple iPhone 15 Pro İncelemesi",
            "url": "https://techsite.com/iphone15",
            "description": "iPhone 15 Pro'nun özellikleri, kamera performansı, işlemci hızı ve fiyat-performans değerlendirmesi.",
            "category": "Teknoloji",
            "date": "2024-01-19"
        },
        {
            "title": "ChatGPT 4.0 Neler Suniyor?",
            "url": "https://example.com/chatgpt4",
            "description": "OpenAI'nin yeni ChatGPT 4.0 sürümü, AI uygulamaları ve işletmeler için kullanım alanları.",
            "category": "Yapay Zeka",
            "date": "2024-01-17"
        },
        
        # Programlama
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
            "title": "React 18 Yenilikler",
            "url": "https://example.com/react18",
            "description": "React 18'in yeni özellikleri: Concurrent Rendering, Automatic Batching ve Suspense.",
            "category": "Yazılım",
            "date": "2024-01-14"
        },
        {
            "title": "TypeScript Dersleri İçin Başlangıç",
            "url": "https://example.com/typescript",
            "description": "TypeScript ile statik tipli JavaScript yazın. Interfaces, Generics ve Decorators öğrenin.",
            "category": "Yazılım",
            "date": "2024-01-12"
        },
        
        # Veri Bilimi
        {
            "title": "Veri Analizi Pandas ile",
            "url": "https://example.com/pandas",
            "description": "Pandas kütüphanesi ile veri analizi yapın. Veri temizleme ve dönüştürme teknikleri.",
            "category": "Veri Bilimi",
            "date": "2024-01-08"
        },
        {
            "title": "Machine Learning Başlangıç Kursu",
            "url": "https://example.com/ml-intro",
            "description": "Scikit-learn ile makine öğrenmesi modellerini eğitin ve değerlendirin.",
            "category": "Yapay Zeka",
            "date": "2024-01-05"
        },
        {
            "title": "Python ile Veri Görselleştirme",
            "url": "https://example.com/matplotlib",
            "description": "Matplotlib ve Seaborn kütüphaneleri ile harika grafikler ve şemalar oluşturun.",
            "category": "Veri Bilimi",
            "date": "2024-01-03"
        },
        
        # İş ve Girişimcilik
        {
            "title": "Startup Kurmak için Rehber",
            "url": "https://example.com/startup-guide",
            "description": "İş planı yazma, finansman bulma, pazarlama stratejisi ve büyüme yolları.",
            "category": "İş",
            "date": "2024-01-11"
        },
        {
            "title": "Dijital Pazarlama Stratejileri",
            "url": "https://example.com/digital-marketing",
            "description": "SEO, SEM, sosyal medya pazarlaması ve İçerik Pazarlaması stratejileri.",
            "category": "İş",
            "date": "2024-01-09"
        },
        {
            "title": "Excel İle Veri Analizi",
            "url": "https://example.com/excel-analysis",
            "description": "Excel formülleri, PivotTable'lar ve gelişmiş analiz teknikleri.",
            "category": "İş",
            "date": "2024-01-06"
        },
        
        # Sosyal Medya
        {
            "title": "TikTok Algoritması Nasıl Çalışıyor?",
            "url": "https://example.com/tiktok-algorithm",
            "description": "TikTok'un önerme algoritması, viral olma yolları ve içerik stratejileri.",
            "category": "Sosyal Medya",
            "date": "2024-01-13"
        },
        {
            "title": "Instagram İçerik Planlama",
            "url": "https://example.com/instagram-plan",
            "description": "Instagram stratejisi, Reels, Stories ve Hashag kullanımı.",
            "category": "Sosyal Medya",
            "date": "2024-01-07"
        },
        {
            "title": "LinkedIn Profesyonel Profil Oluşturma",
            "url": "https://example.com/linkedin-profile",
            "description": "LinkedIn profilinizi optimize edin, bağlantı kurun ve iş bulun.",
            "category": "Sosyal Medya",
            "date": "2024-01-04"
        },
        
        # Eğitim
        {
            "title": "İngilizce Öğrenme İpuçları",
            "url": "https://example.com/english-tips",
            "description": "Konuşma, yazı, dinleme ve okuma becerilerini geliştirme yöntemleri.",
            "category": "Eğitim",
            "date": "2024-01-02"
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

# İstatistikler göster (sidebar üstü)
st.sidebar.write("---")
st.sidebar.write("**📊 Veritabanı İstatistikleri**")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Toplam Sonuç", len(data))
with col2:
    st.metric("Kategoriler", len(categories))
st.sidebar.write("---")

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
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    topics = [
        {"emoji": "📺", "name": "YouTube"},
        {"emoji": "🐍", "name": "Python"},
        {"emoji": "🤖", "name": "AI"},
        {"emoji": "📱", "name": "TikTok"},
        {"emoji": "💼", "name": "İş"}
    ]
    
    for col, topic in zip([col1, col2, col3, col4, col5], topics):
        with col:
            if st.button(f"{topic['emoji']}\n{topic['name']}", use_container_width=True):
                search_query = topic['name']
                st.rerun()

# Alt bilgi
st.divider()
st.markdown("""
<div style="text-align: center; color: #999; font-size: 12px; padding: 20px;">
    <p>östsearch © 2024 | Akıllı Arama Teknolojisi</p>
</div>
""", unsafe_allow_html=True)
