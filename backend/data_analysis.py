import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class CarDataAnalyzer:
    def __init__(self, data_path='data/car_prices.csv'):
        self.df = pd.read_csv(data_path)
        self.prepare_data()
    
    def prepare_data(self):
        """Veriyi temizle ve hazırla"""
        # Eksik değerleri doldur
        self.df['motor'] = self.df['motor'].fillna(1.6)
        self.df['kasa'] = self.df['kasa'].fillna('sedan')
        self.df['hasar'] = self.df['hasar'].fillna('bilinmiyor')
        
        # Aykırı değerleri temizle
        self.df = self.df[self.df['fiyat'] > 50000]  # Çok düşük fiyatları ele
        self.df = self.df[self.df['fiyat'] < 10000000]  # Çok yüksek fiyatları ele
        
        # Yeni özellikler ekle
        self.df['yas'] = datetime.now().year - self.df['yil']
        self.df['km_yil'] = self.df['km'] / self.df['yas']
    
    def generate_insights(self):
        """Veri analizi yap ve içgörüler üret"""
        insights = {
            'total_cars': len(self.df),
            'avg_price': self.df['fiyat'].mean(),
            'price_by_brand': self.df.groupby('marka')['fiyat'].mean().to_dict(),
            'price_by_year': self.df.groupby('yil')['fiyat'].mean().to_dict(),
            'popular_brands': self.df['marka'].value_counts().head(10).to_dict(),
            'fuel_distribution': self.df['yakit'].value_counts().to_dict(),
            'avg_km': self.df['km'].mean(),
            'price_ranges': {
                'min': self.df['fiyat'].min(),
                'max': self.df['fiyat'].max(),
                'median': self.df['fiyat'].median()
            }
        }
        
        return insights
    
    def plot_insights(self):
        """Görsel analizler oluştur"""
        # Fiyat dağılımı
        plt.figure(figsize=(10, 6))
        sns.histplot(data=self.df, x='fiyat', bins=50)
        plt.title('Araç Fiyatları Dağılımı')
        plt.savefig('reports/price_distribution.png')
        
        # Marka-fiyat ilişkisi
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=self.df, x='marka', y='fiyat')
        plt.xticks(rotation=45)
        plt.title('Markalara Göre Fiyat Dağılımı')
        plt.savefig('reports/brand_prices.png')
        
        # Yıl-fiyat ilişkisi
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=self.df, x='yil', y='fiyat')
        plt.title('Yıl-Fiyat İlişkisi')
        plt.savefig('reports/year_price_correlation.png')
    
    def save_report(self):
        """Analiz raporunu kaydet"""
        insights = self.generate_insights()
        
        report = f"""
        Araç Piyasası Analiz Raporu
        Tarih: {datetime.now().strftime('%Y-%m-%d')}
        
        Genel İstatistikler:
        - Toplam Araç Sayısı: {insights['total_cars']}
        - Ortalama Fiyat: {insights['avg_price']:,.0f} TL
        - Minimum Fiyat: {insights['price_ranges']['min']:,.0f} TL
        - Maksimum Fiyat: {insights['price_ranges']['max']:,.0f} TL
        - Medyan Fiyat: {insights['price_ranges']['median']:,.0f} TL
        
        En Popüler Markalar:
        {'-' * 30}
        """
        
        for brand, count in insights['popular_brands'].items():
            report += f"- {brand}: {count} adet\n"
        
        report += f"\nYakıt Tipi Dağılımı:\n{'-' * 30}\n"
        for fuel, count in insights['fuel_distribution'].items():
            report += f"- {fuel}: {count} adet\n"
        
        with open('reports/market_analysis.txt', 'w', encoding='utf-8') as f:
            f.write(report)

if __name__ == "__main__":
    analyzer = CarDataAnalyzer()
    analyzer.plot_insights()
    analyzer.save_report() 