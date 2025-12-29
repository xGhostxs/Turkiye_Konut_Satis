# Türkiye Konut Satış Analizi (2015-2024)

Streamlit ile yapılan, 2015-2024 yılları arasında Türkiye'deki konut satışlarının detaylı analizini gösteren web uygulaması.

## 📋 Proje Açıklaması

Bu uygulama Excel dosyasından okunan konut satış verilerini kullanarak:
- İl ve ilçe bazında satış analizi
- Satış türü dağılımı (1.El, 2.El, İpotekli, Diğer)
- Yıllık trend analizi
- Machine Learning ile tahmin modeli oluşturma

## 🚀 Başlangıç

### Gereksinimler

- Python 3.7+
- Streamlit
- Pandas
- Plotly
- Scikit-learn

### Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install streamlit pandas plotly scikit-learn openpyxl
```

2. Excel dosyasını hazırlayın:
   - Dosya adı: `ilce_konut.xlsx`
   - Her yıl için ayrı bir sheet (2015, 2016, 2017, ... 2024)
   - Sütun yapısı:
     - 1. Sütun: İl adı
     - 2. Sütun: İlçe adı
     - 3. Sütun: Toplam satış
     - 6. Sütun: İpotekli satışlar
     - 7. Sütun: Diğer satışlar
     - 9. Sütun: 1. El satışlar
     - 10. Sütun: 2. El satışlar

3. Uygulamayı çalıştırın:
```bash
streamlit run app.py
```

## 📊 Özellikler

### 1. **Harita & Veriler Sekmesi**
- **Dinamik Grafik**: 
  - "Tüm İller" seçiliyse → Top 15 İl
  - Bir il seçiliyse → O ilin Top 15 ilçesi
- **İlçe Detayları**: Seçilen dönem için tüm ilçelerin satış bilgileri
- **Özet İstatistikler**: 
  - Toplam satış sayısı
  - Ortalama satış/ilçe
  - En yüksek ve en düşük satış

### 2. **Grafikler Sekmesi**
- **Satış Türü Dağılımı (Daire Grafik)**:
  - 1. El satışlar
  - 2. El satışlar
  - İpotekli satışlar
  - Diğer satışlar
  
- **Top 10 Grafik**:
  - "Tüm İller" seçiliyse → Top 10 İl
  - Bir il seçiliyse → O ilin Top 10 ilçesi

- **Trend Analizi**: 2015-2024 yılları arasında toplam satış trendinin gösterimi

### 3. **Model Sekmesi**
- **Linear Regression Modeli**
- **Model Metrikleri**:
  - R² Skoru
  - RMSE (Root Mean Squared Error)
  - MSE (Mean Squared Error)
  
- **Tahmin vs Gerçek Değerler**: Model performansını gösteren scatter plot
- **Özellik Katsayıları**: Modelde etkili olan özelliklerin sıralaması

## 🎮 Kullanım

### Yan Menü (Sidebar)
1. **Yıl Seçin**: Analiz etmek istediğiniz yılı seçin (2015-2024)
2. **İl Seçin**: 
   - "Tüm İller" → Tüm Türkiye için analiz
   - Spesifik il → Sadece o ilin verilerini göster

Seçimleriniz yapıldıktan sonra tüm grafikler ve tablolar otomatik olarak güncellenir.

## 📈 Veri İşleme

### Veri Yükleme Süreci
1. Excel dosyasından tüm yıllar okunur
2. Veriler temizlenir ve sayısal formata çevrilir
3. IL, ilçe, yıl ve satış kategorileri tasnif edilir
4. Eksik veriler elimine edilir

### Veri Önbellekleme
- `@st.cache_data` dekoratörü kullanarak veri yükleme hızlandırılmıştır
- Veriler sadece bir kez okunur ve saklanır

## 🤖 Machine Learning Modeli

### Kullanılan Algoritma
- **Linear Regression**: Basit ama etkili tahmin modeli

### Giriş Özellikleri (Features)
- Yıl
- İl kodu (Label Encoded)
- İlçe kodu (Label Encoded)
- İpotekli satışlar
- Diğer satışlar
- 1. El satışlar
- 2. El satışlar

### Çıktı
- Toplam konut satış sayısı tahmini

### Model Değerlendirmesi
- **Test/Train Oranı**: 80/20
- Random State: 42 (Tekrar edilebilirlik için)

## 📁 Dosya Yapısı

```
Satış Tahmin/
├── app.py                      # Ana Streamlit uygulaması
├── ilce_konut.xlsx             # Veri kaynağı (Excel)
├── README.md                   # Bu dosya
└── captures/
    └── statistics_20251222_202754.json  # Ek veri dosyası
```

## 🔧 Teknik Detaylar

### Kütüphaneler
- **streamlit**: Web uygulaması framework
- **pandas**: Veri manipülasyonu ve analizi
- **plotly**: İnteraktif grafikler
- **scikit-learn**: Machine Learning modelleri

### Page Config
- Layout: Wide (Geniş sayfa düzeni)
- Title: Tarayıcı sekmesinde gösterilir

## 💡 İpuçları

1. **Büyük Veri**: Çok sayıda il/ilçe varsa, ilk yüklemede biraz zaman alabilir
2. **Filtreleme**: Spesifik bir il seçerek daha detaylı analiz yapabilirsiniz
3. **Model Doğruluğu**: R² skoru 0-1 arasında; 1'e ne kadar yakınsa model o kadar iyidir

## 📝 Yapılabilecek İyileştirmeler

- [ ] Tahmin aralığı ekleme (gelecek yıllar için tahmin)
- [ ] Daha gelişmiş ML modelleri (XGBoost, Random Forest)
- [ ] Harita görselleştirmesi (Coğrafi harita)
- [ ] Veri indirme özelliği (CSV/Excel)
- [ ] İstatistiksel testler

## 👨‍💻 Geliştirici

Oluşturulma Tarihi: Aralık 2025

## 📞 Destek
e.cankat.sumer@gmail.com
Sorular veya sorunlar için lütfen iletişime geçin.

---

**Not**: Excel dosyasının yapısı önemlidir. Sütun sırası değişirse veri doğru yüklenmeyebilir.
