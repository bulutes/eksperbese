import pandas as pd
import numpy as np
import os

def create_sample_dataset():
    # Örnek veriler
    brands = ['BMW', 'Mercedes', 'Audi', 'Volkswagen', 'Toyota', 'Honda', 'Hyundai', 'Ford', 'Renault', 'Fiat']
    models = {
        'BMW': ['320i', '520i', 'X5', 'M4', '116i'],
        'Mercedes': ['C180', 'E250', 'A180', 'GLA200', 'CLA200'],
        'Audi': ['A3', 'A4', 'Q5', 'A6', 'Q7'],
        'Volkswagen': ['Passat', 'Golf', 'Tiguan', 'Polo', 'Arteon'],
        'Toyota': ['Corolla', 'Yaris', 'RAV4', 'C-HR', 'Camry'],
        'Honda': ['Civic', 'CR-V', 'Jazz', 'HR-V', 'Accord'],
        'Hyundai': ['i20', 'Tucson', 'i10', 'Kona', 'i30'],
        'Ford': ['Focus', 'Fiesta', 'Kuga', 'Puma', 'Mondeo'],
        'Renault': ['Clio', 'Megane', 'Kadjar', 'Captur', 'Talisman'],
        'Fiat': ['Egea', '500', 'Tipo', 'Panda', '500X']
    }
    
    # Veri listesi
    data = []
    
    # 1000 örnek veri oluştur
    for _ in range(1000):
        brand = np.random.choice(brands)
        model = np.random.choice(models[brand])
        year = np.random.randint(2015, 2024)
        km = np.random.randint(0, 200000)
        
        # Temel fiyat (marka ve modele göre)
        base_price = np.random.randint(300000, 2000000)
        
        # Yıl etkisi
        year_effect = (2024 - year) * 50000
        
        # Kilometre etkisi
        km_effect = km * 0.1
        
        # Final fiyat
        price = base_price - year_effect - km_effect
        
        data.append({
            'marka': brand,
            'model': model,
            'yil': year,
            'km': km,
            'vites': np.random.choice(['otomatik', 'manuel'], p=[0.7, 0.3]),
            'yakit': np.random.choice(['benzin', 'dizel', 'hybrid', 'elektrik'], p=[0.4, 0.4, 0.15, 0.05]),
            'motor': np.random.choice([1.0, 1.3, 1.4, 1.5, 1.6, 2.0]),
            'kasa': np.random.choice(['sedan', 'hatchback', 'suv'], p=[0.5, 0.3, 0.2]),
            'hasar': np.random.choice(['var', 'yok'], p=[0.2, 0.8]),
            'fiyat': max(100000, int(price))  # Minimum 100,000 TL
        })
    
    # DataFrame oluştur
    df = pd.DataFrame(data)
    
    # Klasör oluştur
    os.makedirs('data', exist_ok=True)
    
    # CSV olarak kaydet
    df.to_csv('data/car_prices.csv', index=False)
    print("Örnek veri seti oluşturuldu: data/car_prices.csv")
    print(f"Toplam {len(df)} araç verisi kaydedildi.")
    
    return df

if __name__ == "__main__":
    create_sample_dataset() 