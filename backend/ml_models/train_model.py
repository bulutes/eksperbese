import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib

# Örnek veri seti oluşturma (gerçek verilerinizle değiştirin)
def create_sample_data():
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'marka': np.random.choice(['toyota', 'volkswagen', 'ford', 'renault', 'bmw', 'mercedes', 'audi'], n_samples),
        'model_yili': np.random.randint(2010, 2024, n_samples),
        'kilometre': np.random.randint(0, 300000, n_samples),
        'yakit': np.random.choice(['benzin', 'dizel', 'lpg', 'hybrid', 'elektrik'], n_samples),
        'vites': np.random.choice(['manuel', 'otomatik', 'yarı-otomatik'], n_samples),
        'motor_hacmi': np.random.choice(['1.0', '1.4', '1.6', '2.0'], n_samples),
        'hasar': np.random.choice(['var', 'yok'], n_samples),
    }
    
    # Fiyat hesaplama (basit bir formül)
    base_prices = {
        'toyota': 400000, 'volkswagen': 450000, 'ford': 380000, 'renault': 350000,
        'bmw': 800000, 'mercedes': 850000, 'audi': 750000
    }
    
    prices = []
    for i in range(n_samples):
        base = base_prices[data['marka'][i]]
        year_factor = (2024 - data['model_yili'][i]) * 30000
        km_factor = data['kilometre'][i] * 0.1
        
        price = base - year_factor - km_factor
        
        # Yakıt tipi etkisi
        if data['yakit'][i] == 'elektrik':
            price *= 1.2
        elif data['yakit'][i] == 'hybrid':
            price *= 1.1
            
        # Vites tipi etkisi
        if data['vites'][i] == 'otomatik':
            price *= 1.1
            
        # Hasar durumu etkisi
        if data['hasar'][i] == 'var':
            price *= 0.85
            
        # Rastgele varyasyon ekle
        price *= np.random.uniform(0.9, 1.1)
        
        prices.append(max(price, 100000))  # Minimum fiyat sınırı
    
    data['fiyat'] = prices
    return pd.DataFrame(data)

def train_model():
    # Veri setini oluştur
    df = create_sample_data()
    
    # Label Encoding
    le_dict = {}
    categorical_columns = ['marka', 'yakit', 'vites', 'motor_hacmi', 'hasar']
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le
    
    # Feature'ları ve target'ı ayır
    X = df.drop('fiyat', axis=1)
    y = df['fiyat']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Model eğitimi
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Model ve yardımcı nesneleri kaydet
    joblib.dump(model, 'ml_models/car_price_model.joblib')
    joblib.dump(scaler, 'ml_models/scaler.joblib')
    joblib.dump(le_dict, 'ml_models/label_encoders.joblib')
    
    # Model performansını değerlendir
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    print(f"Train R2 Score: {train_score:.4f}")
    print(f"Test R2 Score: {test_score:.4f}")

if __name__ == "__main__":
    train_model()