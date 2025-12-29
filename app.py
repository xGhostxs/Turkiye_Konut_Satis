import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import json
import urllib.request

st.set_page_config(page_title="Konut Satış Analizi", layout="wide")

st.title(" Türkiye Konut Satış Analizi (2015-2024)")
st.markdown("Excel dosyasından okunan verileri yıl bazında analiz ve tahmin")

@st.cache_data
def load_data():
    veri = pd.read_excel("ilce_konut.xlsx", sheet_name=None)
    sayfa_ad = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
    
    dfs = []
    for sheet_name in sayfa_ad:
        if sheet_name in veri:
            df = veri[sheet_name]
            
            if len(df) > 0:
                df.columns = df.iloc[0]
                df = df.iloc[1:].reset_index(drop=True)
            
            df.columns = [str(col).lower().strip() for col in df.columns]
            
            if len(df.columns) >= 3:
                new_df = df.iloc[:, 1:3].copy()
                new_df.columns = ['il', 'ilçe']
                new_df['yil'] = int(sheet_name)
                new_df['toplam'] = pd.to_numeric(df.iloc[:, 3], errors='coerce')
                
                # Excel sütun sırası: 6.sütun=ipotekli, 7.sütun=diğer, 9.sütun=ilk_el, 10.sütun=ikinci_el
                if len(df.columns) > 5:
                    new_df['ipotekli'] = pd.to_numeric(df.iloc[:, 5], errors='coerce')
                if len(df.columns) > 6:
                    new_df['diger'] = pd.to_numeric(df.iloc[:, 6], errors='coerce')
                if len(df.columns) > 8:
                    new_df['ilk_el'] = pd.to_numeric(df.iloc[:, 8], errors='coerce')
                if len(df.columns) > 9:
                    new_df['ikinci_el'] = pd.to_numeric(df.iloc[:, 9], errors='coerce')
                
                dfs.append(new_df)
    
    tum_veri = pd.concat(dfs, ignore_index=True)
    tum_veri = tum_veri.dropna(subset=['toplam', 'il', 'ilçe'])
    tum_veri['toplam'] = pd.to_numeric(tum_veri['toplam'], errors='coerce')
    
    return tum_veri

tum_veri = load_data()

st.subheader(" Veri Özeti")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Toplam Satır", len(tum_veri))
with col2:
    st.metric("Yıl Aralığı", f"{tum_veri['yil'].min():.0f} - {tum_veri['yil'].max():.0f}")
with col3:
    st.metric("İl Sayısı", tum_veri['il'].nunique())
with col4:
    st.metric("İlçe Sayısı", tum_veri['ilçe'].nunique())

st.sidebar.title(" Seçenekler")
secili_yil = st.sidebar.selectbox("Yıl Seçin", sorted(tum_veri['yil'].unique()))

il_listesi = sorted(tum_veri['il'].unique())
secili_il = st.sidebar.selectbox("İl Seçin (İsteğe Bağlı)", ["Tüm İller"] + il_listesi)

yil_verisi = tum_veri[tum_veri['yil'] == secili_yil].copy()

if secili_il != "Tüm İller":
    yil_verisi = yil_verisi[yil_verisi['il'] == secili_il]

tab1, tab2, tab3 = st.tabs([" Harita & Veriler", " Grafikler", " Model"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if secili_il != "Tüm İller":
            st.subheader(f" {secili_il} İli - {secili_yil} Yılı Konut Satışları (İlçe Bazında)")
            
            ilce_ozet = yil_verisi.groupby('ilçe')['toplam'].sum().sort_values(ascending=True).tail(15)
            
            fig = px.bar(
                x=ilce_ozet.values,
                y=ilce_ozet.index,
                title=f"{secili_yil} Yılı En Çok Satış Yapan Top 15 İlçe",
                labels={"x": "Toplam Satış Sayısı", "y": "İlçe"},
                color=ilce_ozet.values,
                color_continuous_scale="Viridis"
            )
        else:
            st.subheader(f" {secili_yil} Yılı Konut Satışları (İl Bazında)")
            
            il_ozet = yil_verisi.groupby('il')['toplam'].sum().sort_values(ascending=True).tail(15)
            
            fig = px.bar(
                x=il_ozet.values,
                y=il_ozet.index,
                title=f"{secili_yil} Yılı En Çok Satış Yapan Top 15 İl",
                labels={"x": "Toplam Satış Sayısı", "y": "İl"},
                color=il_ozet.values,
                color_continuous_scale="Viridis"
            )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("İlçe Detayları")
        tablo = yil_verisi[['il', 'ilçe', 'toplam', 'ipotekli', 'diger', 'ilk_el', 'ikinci_el']].sort_values('toplam', ascending=False)
        tablo.columns = ['İl', 'İlçe', 'Toplam', 'İpotekli', 'Diğer', '1. El', '2. El']
        st.dataframe(tablo, use_container_width=True, height=400)
    
    with col2:
        st.subheader("Özet İstatistikler")
        st.metric("Toplam Satış", f"{yil_verisi['toplam'].sum():,.0f}")
        st.metric("Ortalama Satış/İlçe", f"{yil_verisi['toplam'].mean():,.0f}")
        st.metric("Max Satış", f"{yil_verisi['toplam'].max():,.0f}")
        st.metric("Min Satış", f"{yil_verisi['toplam'].min():,.0f}")
        
        st.markdown("**Top 5 İlçe**")
        top5 = yil_verisi.nlargest(5, 'toplam')[['ilçe', 'toplam']]
        for idx, row in top5.iterrows():
            st.write(f"• {row['ilçe']}: {row['toplam']:,.0f}")

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        satislar = {
            '1. El': yil_verisi['ilk_el'].fillna(0).sum(),
            '2. El': yil_verisi['ikinci_el'].fillna(0).sum(),
            'İpotekli': yil_verisi['ipotekli'].fillna(0).sum(),
            'Diğer': yil_verisi['diger'].fillna(0).sum(),
        }
        
        satislar_filtered = {k: v for k, v in satislar.items() if v > 0}
        
        if satislar_filtered:
            fig_pie = px.pie(
                values=list(satislar_filtered.values()),
                names=list(satislar_filtered.keys()),
                title=f"{secili_yil} Yılı Satış Türü Dağılımı"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Bu dönem için satış türü verisi bulunamadı.")
    
    with col2:
        if secili_il != "Tüm İller":
            ilce_ozet = yil_verisi.groupby('ilçe')['toplam'].sum().sort_values(ascending=False).head(10)
            fig_bar = px.bar(
                x=ilce_ozet.index,
                y=ilce_ozet.values,
                title=f"{secili_il} - Top 10 İlçe {secili_yil} Yılı Toplam Satış",
                labels={"x": "İlçe", "y": "Toplam Satış"}
            )
        else:
            il_ozet = yil_verisi.groupby('il')['toplam'].sum().sort_values(ascending=False).head(10)
            fig_bar = px.bar(
                x=il_ozet.index,
                y=il_ozet.values,
                title=f"Top 10 İl {secili_yil} Yılı Toplam Satış",
                labels={"x": "İl", "y": "Toplam Satış"}
            )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.subheader(" Yıl Bazında Trend")
    yil_trend = tum_veri.groupby('yil')['toplam'].sum().reset_index()
    fig_trend = px.line(
        yil_trend,
        x='yil',
        y='toplam',
        markers=True,
        title="2015-2024 Toplam Konut Satışları Trendi",
        labels={"yil": "Yıl", "toplam": "Toplam Satış"}
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with tab3:
    st.subheader(" İstatistiksel Tahmin Modeli")
    
    from sklearn.preprocessing import StandardScaler
    
    tum_veri_clean = tum_veri.dropna(subset=['toplam'])
    tum_veri_clean['toplam'] = pd.to_numeric(tum_veri_clean['toplam'], errors='coerce')
    
    X = tum_veri_clean[['yil']].copy()
    
    le_il = LabelEncoder()
    le_ilce = LabelEncoder()
    X['il_code'] = le_il.fit_transform(tum_veri_clean['il'].astype(str))
    X['ilce_code'] = le_ilce.fit_transform(tum_veri_clean['ilçe'].astype(str))
    
    satislar_cols = ['ipotekli', 'diger', 'ilk_el', 'ikinci_el']
    for col in satislar_cols:
        if col in tum_veri_clean.columns:
            X[col] = pd.to_numeric(tum_veri_clean[col], errors='coerce').fillna(0)
    
    y = pd.to_numeric(tum_veri_clean['toplam'], errors='coerce')
    
    valid_idx = ~(X.isna().any(axis=1) | y.isna())
    X = X[valid_idx]
    y = y[valid_idx]
    
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("R² Skoru", f"{r2:.4f}")
    with col2:
        st.metric("RMSE", f"{rmse:,.2f}")
    with col3:
        st.metric("MSE", f"{mse:,.2f}")
    
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(
        y=y_test.values, 
        name='Gerçek Değerler',
        mode='markers'
    ))
    fig_pred.add_trace(go.Scatter(
        y=y_pred, 
        name='Tahmin Edilen Değerler',
        mode='markers'
    ))
    fig_pred.update_layout(
        title="Model Tahminleri vs Gerçek Değerler",
        xaxis_title="Veri Seti",
        yaxis_title="Konut Satış Sayısı",
        height=400
    )
    st.plotly_chart(fig_pred, use_container_width=True)
    
    st.subheader(" Özellik Katsayıları")
    feature_importance = pd.DataFrame({
        'Özellik': X.columns,
        'Katsayı': model.coef_
    }).sort_values('Katsayı', ascending=False)
    
    fig_coef = px.bar(
        feature_importance,
        x='Katsayı',
        y='Özellik',
        orientation='h',
        title="Model Katsayıları"
    )
    st.plotly_chart(fig_coef, use_container_width=True)

