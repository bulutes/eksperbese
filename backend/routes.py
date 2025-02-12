from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Dict
from backend.ml_models.train_model import CarPricePredictor
from report_generator import ReportGenerator
import os
import logging
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from price_prediction import predict_car_price

# Logger yapılandırması
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# JWT ayarları
SECRET_KEY = "your-secret-key-here"  # Güvenli bir secret key kullanın
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Şifreleme için
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Şifre dosyası yolu
PASSWORD_FILE = "password.txt"
ADMIN_PASSWORD = "admin123"  # Admin paneli için şifre

# Router ve predictor tanımlamaları
router = APIRouter()
predictor = CarPricePredictor()
report_generator = ReportGenerator()

# Request modelleri
class PredictionRequest(BaseModel):
    hasar_durumu: str
    arac_bilgileri: Dict[str, str]

class PasswordRequest(BaseModel):
    password: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/verify-password")
async def verify_password(request: PasswordRequest):
    try:
        # Admin şifre kontrolü
        if request.password == ADMIN_PASSWORD:
            token = create_access_token({"sub": "admin"})
            return {"token": token}
            
        # Normal kullanıcı şifre kontrolü
        with open(PASSWORD_FILE, "r") as f:
            stored_password = f.read().strip()
            if pwd_context.verify(request.password, stored_password):
                token = create_access_token({"sub": "user"})
                return {"token": token}
    except FileNotFoundError:
        # İlk kullanımda şifre dosyası yoksa admin şifresini kontrol et
        if request.password == ADMIN_PASSWORD:
            token = create_access_token({"sub": "admin"})
            return {"token": token}
        raise HTTPException(status_code=500, detail="Sistem hatası")
    
    raise HTTPException(status_code=401, detail="Geçersiz şifre")

@router.post("/admin-login")
async def admin_login(request: PasswordRequest):
    if request.password == ADMIN_PASSWORD:
        token = create_access_token({"sub": "admin"})
        return {"token": token}
    raise HTTPException(status_code=401, detail="Geçersiz admin şifresi")

@router.post("/update-password")
async def update_password(request: PasswordRequest, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") != "admin":
            raise HTTPException(status_code=403, detail="Yetkisiz erişim")
        
        hashed_password = pwd_context.hash(request.password)
        with open(PASSWORD_FILE, "w") as f:
            f.write(hashed_password)
        return {"message": "Şifre başarıyla güncellendi"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz token")

# Mevcut endpoint'leri koruma altına alalım
@router.post("/predict")
async def predict_price(request: PredictionRequest, token: str = Depends(oauth2_scheme)):
    try:
        # Token kontrolü
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        logger.debug(f"Gelen istek: {request}")
        result = predictor.predict_price(
            request.hasar_durumu,
            request.arac_bilgileri
        )
        result['arac_bilgileri'] = request.arac_bilgileri
        return result
    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    except Exception as e:
        logger.error(f"Tahmin hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-report")
async def generate_report(data: dict, token: str = Depends(oauth2_scheme)):
    try:
        # Token kontrolü
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        logger.debug(f"Gelen veri: {data}")
        
        reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        filename = f"arac_raporu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(reports_dir, filename)
        
        report_generator.generate_report(data, filepath)
        
        if not os.path.exists(filepath):
            raise Exception("PDF dosyası oluşturulamadı")
            
        return FileResponse(
            filepath,
            media_type='application/pdf',
            filename=filename
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    except Exception as e:
        logger.error(f"Rapor oluşturma hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

main = Blueprint('main', __name__)

@main.route('/api/predict/', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Tahmin işlemi
        prediction = predict_car_price(data)
        
        return jsonify({
            'deger': prediction['price'],
            'minDeger': prediction['min_price'],
            'maxDeger': prediction['max_price'],
            'guvenOrani': prediction['confidence'],
            'piyasaYorumu': prediction['market_analysis']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400