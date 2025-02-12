from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import json
import os
import logging
from price_prediction import predict_price
import uvicorn

app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React uygulamanızın adresi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model sınıfları
class CarPredictionRequest(BaseModel):
    marka: str
    model: str
    yil: int
    km: int
    vites: str
    yakit: str
    motor: float
    kasa: str

class AdminLoginRequest(BaseModel):
    password: str

# Yapay zeka modeli ve veri önişleme araçlarını oluştur
def create_sample_model():
    try:
        # Örnek veri seti
        data = pd.DataFrame({
            'marka': ['BMW', 'Mercedes', 'Audi', 'Volkswagen'],
            'model': ['3.20', 'C180', 'A4', 'Passat'],
            'yil': [2020, 2021, 2019, 2022],
            'km': [50000, 30000, 70000, 20000],
            'vites': ['otomatik', 'otomatik', 'manuel', 'otomatik'],
            'yakit': ['dizel', 'benzin', 'dizel', 'benzin'],
            'motor': [2.0, 1.6, 2.0, 1.5],
            'kasa': ['sedan', 'sedan', 'sedan', 'sedan'],
            'fiyat': [1200000, 1500000, 1100000, 1300000]
        })

        # Label Encoder'ları oluştur
        encoders = {}
        categorical_columns = ['marka', 'model', 'vites', 'yakit', 'kasa']
        for column in categorical_columns:
            le = LabelEncoder()
            le.fit(data[column])
            encoders[column] = le

        # Modeli oluştur ve eğit
        X = data.drop('fiyat', axis=1)
        y = data['fiyat']
        
        # Kategorik değişkenleri encode et
        for column in categorical_columns:
            X[column] = encoders[column].transform(X[column])

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        return model, encoders
    except Exception as e:
        logging.error(f"Model oluşturma hatası: {str(e)}")
        return None, None

# Global değişkenler
model, label_encoders = create_sample_model()

# Eksper endpoint'i
@app.post("/login")
async def expert_login(request: Request):
    try:
        data = await request.json()
        password = data.get('password')
        if not password:
            raise HTTPException(status_code=400, detail="Şifre gerekli")

        # Şifreleri yükle
        try:
            with open("passwords.json", "r") as f:
                passwords = json.load(f)
        except FileNotFoundError:
            passwords = {"expert_passwords": []}

        # Şifreyi kontrol et
        if password in passwords.get('expert_passwords', []):
            return {"token": f"expert_{password}"}  # Basit bir token oluştur
        else:
            raise HTTPException(status_code=401, detail="Geçersiz şifre")

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Admin endpoint'leri
@app.post("/admin/login")
async def admin_login(request: AdminLoginRequest):
    if request.password == os.getenv('ADMIN_PASSWORD', 'admin123'):
        return {"token": os.getenv('ADMIN_TOKEN', 'admin_secret_token')}
    raise HTTPException(status_code=401, detail="Geçersiz şifre")

@app.get("/admin/passwords")
async def get_passwords(request: Request):
    token = request.headers.get('Authorization')
    if token != os.getenv('ADMIN_TOKEN', 'admin_secret_token'):
        raise HTTPException(status_code=401, detail="Yetkisiz erişim")
    
    try:
        with open("passwords.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"expert_passwords": []}

@app.post("/admin/add-password")
async def add_password(request: Request):
    token = request.headers.get('Authorization')
    if token != os.getenv('ADMIN_TOKEN', 'admin_secret_token'):
        raise HTTPException(status_code=401, detail="Yetkisiz erişim")

    data = await request.json()
    new_password = data.get('password')
    if not new_password:
        raise HTTPException(status_code=400, detail="Şifre gerekli")

    try:
        try:
            with open("passwords.json", "r") as f:
                passwords = json.load(f)
        except FileNotFoundError:
            passwords = {"expert_passwords": []}

        if new_password in passwords['expert_passwords']:
            raise HTTPException(status_code=400, detail="Bu şifre zaten mevcut")

        passwords['expert_passwords'].append(new_password)
        
        with open("passwords.json", "w") as f:
            json.dump(passwords, f)

        return {"message": "Şifre başarıyla eklendi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/admin/delete-password")
async def delete_password(request: Request):
    token = request.headers.get('Authorization')
    if token != os.getenv('ADMIN_TOKEN', 'admin_secret_token'):
        raise HTTPException(status_code=401, detail="Yetkisiz erişim")

    data = await request.json()
    password_to_delete = data.get('password')
    if not password_to_delete:
        raise HTTPException(status_code=400, detail="Şifre gerekli")

    try:
        with open("passwords.json", "r") as f:
            passwords = json.load(f)

        if password_to_delete not in passwords['expert_passwords']:
            raise HTTPException(status_code=404, detail="Şifre bulunamadı")

        passwords['expert_passwords'].remove(password_to_delete)
        
        with open("passwords.json", "w") as f:
            json.dump(passwords, f)

        return {"message": "Şifre başarıyla silindi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Tahmin endpoint'i
@app.post("/api/predict/")
async def predict(data: dict):
    try:
        print("Gelen veri:", data)  # Debug için
        result = predict_price(data)
        print("Tahmin sonucu:", result)  # Debug için
        
        if not result:
            raise HTTPException(status_code=400, detail="Tahmin yapılamadı")
            
        return {
            "deger": result["deger"],
            "minDeger": result["minDeger"],
            "maxDeger": result["maxDeger"],
            "guvenOrani": result["guvenOrani"],
            "piyasaYorumu": result["piyasaYorumu"]
        }
    except Exception as e:
        print("Hata:", str(e))  # Debug için
        raise HTTPException(status_code=400, detail=str(e))

# Yardımcı fonksiyonlar
def get_similar_cars(car_data):
    """Benzer araçları getir"""
    # Örnek benzer araç verileri
    return [
        {"price": 1150000, "km": 45000},
        {"price": 1250000, "km": 35000},
        {"price": 1180000, "km": 40000}
    ]

def analyze_value_factors(car_data, predicted_price, similar_cars):
    """Değer faktörlerini analiz et"""
    factors = []
    
    # Kilometre analizi
    avg_km = np.mean([car['km'] for car in similar_cars])
    if int(car_data['km']) < avg_km:
        factors.append({
            "etki": 1,
            "aciklama": "Düşük kilometre değeri olumlu etkiliyor"
        })
    else:
        factors.append({
            "etki": -1,
            "aciklama": "Yüksek kilometre değeri olumsuz etkiliyor"
        })
    
    # Yaş analizi
    current_year = 2024
    car_age = current_year - int(car_data['yil'])
    if car_age < 3:
        factors.append({
            "etki": 1,
            "aciklama": "Araç yaşı olumlu etkiliyor"
        })
    
    return factors

def generate_market_comment(car_data, predicted_price, similar_cars):
    """Piyasa yorumu oluştur"""
    current_year = 2024
    car_age = current_year - int(car_data['yil'])
    avg_market_price = np.mean([car['price'] for car in similar_cars])
    
    comment = f"{car_data['marka']} {car_data['model']} için {car_age} yaşında bir araç olarak "
    
    if predicted_price > avg_market_price:
        comment += "piyasa ortalamasının üzerinde bir değere sahip. "
    else:
        comment += "piyasa ortalamasına yakın bir değere sahip. "
    
    comment += f"Benzer {len(similar_cars)} adet araç incelendiğinde, "
    comment += f"ortalama {round(avg_market_price):,} TL değerinde satışa sunuluyor. "
    
    if int(car_data['km']) < np.mean([car['km'] for car in similar_cars]):
        comment += "Düşük kilometresi değerini olumlu etkiliyor. "
    
    return comment

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)