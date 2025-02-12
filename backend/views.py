import joblib
import numpy as np
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from flask import jsonify
from price_prediction import predict_car_price

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict(request):
    try:
        # Model ve yardımcı nesneleri yükle
        model = joblib.load('ml_models/car_price_model.joblib')
        scaler = joblib.load('ml_models/scaler.joblib')
        le_dict = joblib.load('ml_models/label_encoders.joblib')
        
        # Gelen veriyi hazırla
        input_data = {
            'marka': le_dict['marka'].transform([request.data['marka'].lower()])[0],
            'model_yili': int(request.data['yil']),
            'kilometre': int(request.data['km']),
            'yakit': le_dict['yakit'].transform([request.data['yakit'].lower()])[0],
            'vites': le_dict['vites'].transform([request.data['vites'].lower()])[0],
            'motor_hacmi': le_dict['motor_hacmi'].transform([request.data['motor']])[0],
            'hasar': le_dict['hasar'].transform([request.data['hasar']])[0]
        }
        
        # Numpy array'e çevir ve scale et
        input_array = np.array(list(input_data.values())).reshape(1, -1)
        input_scaled = scaler.transform(input_array)
        
        # Tahmin yap
        prediction = model.predict(input_scaled)[0]
        
        # Güven aralığı hesapla
        predictions = []
        for estimator in model.estimators_:
            predictions.append(estimator.predict(input_scaled)[0])
        
        confidence_interval = np.percentile(predictions, [5, 95])
        
        # Market analizi
        market_multipliers = {
            'min': 0.92,
            'max': 1.08,
            'similar_min': 0.88,
            'similar_max': 1.12
        }
        
        response_data = {
            'deger': round(prediction),
            'minDeger': round(prediction * market_multipliers['min']),
            'maxDeger': round(prediction * market_multipliers['max']),
            'ortalamaFiyat': round(prediction * 1.02),
            'benzerMinFiyat': round(prediction * market_multipliers['similar_min']),
            'benzerMaxFiyat': round(prediction * market_multipliers['similar_max']),
            'ilanSayisi': np.random.randint(20, 50),
            'degerFaktorleri': [
                {
                    'etki': 1 if int(request.data['km']) < 100000 else -1,
                    'aciklama': 'Kilometre değeri ortalamanın altında' if int(request.data['km']) < 100000 else 'Kilometre değeri ortalamanın üstünde'
                },
                {
                    'etki': 1 if request.data['hasar'] == 'yok' else -1,
                    'aciklama': 'Hasar kaydı bulunmuyor' if request.data['hasar'] == 'yok' else 'Hasar kaydı mevcut'
                }
            ],
            'piyasaYorumu': generate_market_comment(request.data, prediction),
            'guvenOrani': calculate_confidence_score(predictions)
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

def generate_market_comment(data, prediction):
    current_year = 2024
    vehicle_age = current_year - int(data['yil'])
    
    comment = f"{data['marka']} {data['model']} {data['yil']} model araçlar için "
    
    if vehicle_age < 3:
        comment += "piyasada yüksek talep görülmektedir. "
    elif vehicle_age < 7:
        comment += "piyasada orta düzeyde talep görülmektedir. "
    else:
        comment += "piyasada düşük talep görülmektedir. "
    
    if data['yakit'] in ['elektrik', 'hybrid']:
        comment += f"{data['yakit'].capitalize()} araçlara olan yüksek talep nedeniyle değer artışı gözlemlenmektedir. "
    
    if data['hasar'] == 'yok':
        comment += "Hasar kaydının bulunmaması değeri olumlu etkilemektedir."
    else:
        comment += "Hasar kaydı nedeniyle değer kaybı hesaplamaya dahil edilmiştir."
    
    return comment

def calculate_confidence_score(predictions):
    std = np.std(predictions)
    mean = np.mean(predictions)
    cv = std / mean  # Coefficient of variation
    
    # CV değeri ne kadar düşükse, tahmin o kadar tutarlı
    confidence_score = 100 * (1 - min(cv, 0.5))  # CV'yi 0.5 ile sınırla
    
    return round(max(min(confidence_score, 95), 85))  # 85-95 arası sınırla

def handle_prediction_request(data):
    try:
        prediction = predict_car_price(data)
        return jsonify(prediction), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400