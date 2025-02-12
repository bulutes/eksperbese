import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Sabit örnek veri seti (gerçek veri olmadığı için)
SAMPLE_DATA = {
    'marka': ['BMW', 'Mercedes', 'Audi', 'Volkswagen', 'Toyota'],
    'model': ['320i', 'C180', 'A4', 'Passat', 'Corolla'],
    'yil': [2020, 2019, 2021, 2018, 2022],
    'km': [50000, 60000, 30000, 80000, 20000],
    'vites': ['otomatik', 'otomatik', 'otomatik', 'manuel', 'otomatik'],
    'yakit': ['benzin', 'benzin', 'dizel', 'dizel', 'hybrid'],
    'motor': [2.0, 1.6, 2.0, 1.6, 1.8],
    'kasa': ['sedan', 'sedan', 'sedan', 'sedan', 'sedan'],
    'hasar': ['yok', 'yok', 'var', 'yok', 'yok'],
    'fiyat': [950000, 900000, 850000, 650000, 750000]
}

def create_sample_dataset():
    """Örnek veri seti oluştur"""
    df = pd.DataFrame(SAMPLE_DATA)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/car_prices.csv', index=False)
    return df

def train_model():
    try:
        # Veri setini yükle
        data = pd.read_csv('data/car_prices.csv')
        
        # Kategorik değişkenleri dönüştür
        encoders = {}
        categorical_columns = ['marka', 'model', 'vites', 'yakit', 'kasa', 'hasar']
        
        for col in categorical_columns:
            encoders[col] = LabelEncoder()
            data[col] = encoders[col].fit_transform(data[col].astype(str))
        
        # Özellikler ve hedef değişken
        X = data[['marka', 'model', 'yil', 'km', 'vites', 'yakit', 'motor', 'kasa', 'hasar']]
        y = data['fiyat']
        
        # Model eğitimi
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        model.fit(X, y)
        
        # Model ve encoder'ları kaydet
        os.makedirs('ml_models', exist_ok=True)
        joblib.dump(model, 'ml_models/car_price_model.joblib')
        joblib.dump(encoders, 'ml_models/encoders.joblib')
        
        return model, encoders
        
    except Exception as e:
        print(f"Model eğitim hatası: {str(e)}")
        return None, None

def calculate_base_price(marka, model, yil):
    """Temel fiyat hesaplama"""
    # Marka bazlı temel fiyatlar
    brand_prices = {
        'BMW': 1500000,
        'Mercedes': 1600000,
        'Audi': 1400000,
        'Volkswagen': 800000,
        'Toyota': 700000,
        'Honda': 650000,
        'Hyundai': 600000,
        'Ford': 700000,
        'Renault': 550000,
        'Fiat': 450000
    }
    
    # Markanın temel fiyatını al veya ortalama bir değer kullan
    base_price = brand_prices.get(marka, 600000)
    
    # Yıl bazlı değer kaybı (her yıl için %8)
    year_depreciation = (2024 - yil) * (base_price * 0.08)
    
    return max(base_price - year_depreciation, 100000)  # Minimum 100,000 TL

def predict_price(data):
    try:
        # Gelen veriyi hazırla
        input_data = {
            'marka': str(data.get('marka', '')),
            'model': str(data.get('model', '')),
            'yil': int(data.get('yil', 2020)),
            'km': int(data.get('km', 0)),
            'vites': str(data.get('vites', '')),
            'yakit': str(data.get('yakit', '')),
            'motor': float(data.get('motor', 0)),
            'kasa': str(data.get('kasa', '')),
            'hasar': str(data.get('hasar', ''))
        }
        
        # Temel fiyat hesapla
        base_price = calculate_base_price(input_data['marka'], input_data['model'], input_data['yil'])
        
        # Kilometre etkisi (her 10.000 km için %0.5 değer kaybı)
        km_effect = (input_data['km'] / 10000) * (base_price * 0.005)
        
        # Motor hacmi etkisi
        engine_multiplier = {
            1.0: 0.85,
            1.3: 0.9,
            1.4: 0.95,
            1.5: 1.0,
            1.6: 1.1,
            2.0: 1.3
        }
        engine_effect = base_price * (engine_multiplier.get(input_data['motor'], 1.0) - 1)
        
        # Vites tipi etkisi
        transmission_effect = base_price * 0.05 if input_data['vites'] == 'otomatik' else 0
        
        # Yakıt tipi etkisi
        fuel_multiplier = {
            'benzin': 1.0,
            'dizel': 1.05,
            'hybrid': 1.15,
            'elektrik': 1.25
        }
        fuel_effect = base_price * (fuel_multiplier.get(input_data['yakit'], 1.0) - 1)
        
        # Kasa tipi etkisi
        body_multiplier = {
            'sedan': 1.0,
            'hatchback': 0.95,
            'suv': 1.15
        }
        body_effect = base_price * (body_multiplier.get(input_data['kasa'], 1.0) - 1)
        
        # Hasar etkisi
        damage_effect = -base_price * 0.15 if input_data['hasar'] == 'var' else 0
        
        # Toplam fiyat hesaplama
        predicted_price = (base_price - km_effect + engine_effect + 
                         transmission_effect + fuel_effect + body_effect + damage_effect)
        
        # Rastgele değişkenlik ekle (%5)
        variation = np.random.uniform(-0.05, 0.05)
        predicted_price *= (1 + variation)
        
        # Minimum ve maksimum fiyat aralığı
        min_price = predicted_price * 0.9
        max_price = predicted_price * 1.1
        
        # Piyasa yorumu
        market_analysis = get_market_analysis(predicted_price, input_data)
        
        return {
            'deger': int(predicted_price),
            'minDeger': int(min_price),
            'maxDeger': int(max_price),
            'guvenOrani': round(min(95 - abs(variation * 100), 95), 1),
            'piyasaYorumu': market_analysis
        }

    except Exception as e:
        print(f"Tahmin hatası: {str(e)}")
        return {
            'deger': 0,
            'minDeger': 0,
            'maxDeger': 0,
            'guvenOrani': 0,
            'piyasaYorumu': "Tahmin yapılamadı: " + str(e)
        }

def get_market_analysis(price, data):
    """Detaylı piyasa analizi oluştur"""
    analysis = []
    
    # Fiyat segmenti analizi
    if price > 1500000:
        segment = "lüks"
        trend = "yükselen"
    elif price > 800000:
        segment = "üst"
        trend = "stabil"
    else:
        segment = "orta"
        trend = "yoğun rekabetli"
    
    # Yaş analizi
    car_age = 2024 - data['yil']
    if car_age < 3:
        age_comment = "Araç yeni sayılır ve değer kaybı minimum düzeydedir."
    elif car_age < 7:
        age_comment = "Araç orta yaşta ve makul bir değer kaybına sahiptir."
    else:
        age_comment = "Araç yaşlı, ancak iyi durumda ise değerini koruyabilir."
    
    # Kilometre analizi
    km = data['km']
    if km < 50000:
        km_comment = "Düşük kilometrede ve değerini iyi koruyor."
    elif km < 100000:
        km_comment = "Ortalama kilometrede, bakımları düzenli yapılmışsa değerini korur."
    else:
        km_comment = "Yüksek kilometrede, detaylı bakım geçmişi önemli."
    
    analysis.append(f"Araç {segment} segmentte yer alıyor ve bu segment şu anda {trend} bir piyasaya sahip.")
    analysis.append(age_comment)
    analysis.append(km_comment)
    
    # Yakıt tipi yorumu
    fuel_comments = {
        'benzin': "Benzinli motorlar şehir içi kullanımda avantajlıdır.",
        'dizel': "Dizel motorlar yakıt ekonomisi sunar ve uzun yol kullanımına uygundur.",
        'hybrid': "Hibrit teknolojisi yakıt tasarrufu sağlar ve çevre dostudur.",
        'elektrik': "Elektrikli araçlar düşük işletme maliyeti sunar ve geleceğin teknolojisidir."
    }
    analysis.append(fuel_comments.get(data['yakit'], ""))
    
    return " ".join(analysis)

if __name__ == "__main__":
    # Model eğitimini test et
    model, encoders = train_model()
    if model is not None:
        print("Model başarıyla eğitildi!")
