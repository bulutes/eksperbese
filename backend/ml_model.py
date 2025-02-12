from typing import Dict, Any, List
import pandas as pd
import numpy as np
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CarPricePredictor:
    def __init__(self):
        self.base_prices = self._load_base_prices()
        self.market_factors = {
            'usd_rate': 31.5,
            'market_condition': 1.1,
            'inflation_rate': 1.15
        }
        self.equipment_levels = {
            'basic': 0.95,
            'medium': 1.0,
            'full': 1.15,
            'premium': 1.25
        }

    def _load_base_prices(self) -> Dict[str, Dict[str, float]]:
        """Güncel araç fiyatlarını yükle"""
        return {
            "toyota": {
                "corolla": 1250000,
                "yaris": 950000,
                "rav4": 2500000,
                "c-hr": 1850000,
                "camry": 2750000
            },
            "volkswagen": {
                "golf": 1450000,
                "passat": 2100000,
                "polo": 950000,
                "tiguan": 2400000,
                "t-roc": 1850000
            },
            "bmw": {
                "3.16": 2500000,
                "3.20": 2800000,
                "5.20": 3500000,
                "x1": 2900000,
                "x3": 3800000,
                "x5": 5500000
            },
            "mercedes": {
                "a180": 2200000,
                "c200": 3100000,
                "e200": 4200000,
                "gla200": 2900000,
                "glc200": 3900000
            },
            "audi": {
                "a3": 1900000,
                "a4": 2800000,
                "a6": 4100000,
                "q3": 2700000,
                "q5": 3800000
            }
        }

    def _calculate_age_factor(self, yil: int) -> float:
        """Yaşa göre değer kaybı hesaplama"""
        current_year = 2024
        age = current_year - yil
        
        if age <= 1:
            return 1.0
        elif age <= 3:
            return 0.85 - (age - 1) * 0.05
        elif age <= 5:
            return 0.75 - (age - 3) * 0.04
        elif age <= 10:
            return 0.65 - (age - 5) * 0.03
        else:
            return max(0.35, 0.50 - (age - 10) * 0.02)

    def _calculate_damage_factor(self, hasar_durumu: str) -> float:
        """Hasar durumuna göre değer kaybı hesaplama"""
        return 1.0 if hasar_durumu == 'hasarsiz' else 0.85

    def _calculate_mileage_factor(self, kilometre: int) -> float:
        """Kilometreye göre değer kaybı hesaplama"""
        try:
            km = float(kilometre)
            if km <= 15000:
                return 1.0
            elif km <= 30000:
                return 0.95
            elif km <= 60000:
                return 0.90
            elif km <= 100000:
                return 0.85
            elif km <= 150000:
                return 0.80
            elif km <= 200000:
                return 0.75
            else:
                return max(0.65, 0.75 - ((km - 200000) / 100000) * 0.05)
        except (ValueError, TypeError):
            return 0.80

    def _calculate_equipment_factor(self, donanim: str) -> float:
        """Donanım seviyesine göre değer faktörü"""
        return self.equipment_levels.get(donanim.lower(), 1.0)

    def _get_base_price(self, marka: str, model: str) -> float:
        """Güncel piyasa değerini belirleme"""
        try:
            marka = marka.lower()
            model = model.lower()
            return self.base_prices.get(marka, {}).get(model, 1000000)
        except Exception as e:
            logger.error(f"Fiyat belirlenirken hata: {str(e)}")
            return 1000000

    def _calculate_market_variation(self, base_price: float) -> float:
        """Piyasa koşullarına göre fiyat varyasyonu"""
        market_effect = (
            base_price * 
            self.market_factors['market_condition'] * 
            self.market_factors['inflation_rate']
        )
        variation = np.random.normal(0, 0.05)
        return market_effect * (1 + variation)

    def _get_equipment_details(self, donanim: str) -> Dict[str, bool]:
        """Donanım seviyesine göre özellikleri belirleme"""
        equipment_details = {
            'basic': {
                'klima': True,
                'abs': True,
                'yol_bilgisayari': True,
                'hiz_sabitleyici': False,
                'geri_gorus_kamerasi': False,
                'navigasyon': False,
                'deri_koltuk': False,
                'sunroof': False
            },
            'medium': {
                'klima': True,
                'abs': True,
                'yol_bilgisayari': True,
                'hiz_sabitleyici': True,
                'geri_gorus_kamerasi': True,
                'navigasyon': False,
                'deri_koltuk': False,
                'sunroof': False
            },
            'full': {
                'klima': True,
                'abs': True,
                'yol_bilgisayari': True,
                'hiz_sabitleyici': True,
                'geri_gorus_kamerasi': True,
                'navigasyon': True,
                'deri_koltuk': True,
                'sunroof': False
            },
            'premium': {
                'klima': True,
                'abs': True,
                'yol_bilgisayari': True,
                'hiz_sabitleyici': True,
                'geri_gorus_kamerasi': True,
                'navigasyon': True,
                'deri_koltuk': True,
                'sunroof': True
            }
        }
        return equipment_details.get(donanim.lower(), equipment_details['medium'])

    def predict_price(self, hasar_durumu: str, arac_bilgileri: Dict[str, Any]) -> Dict[str, Any]:
        """Araç fiyat tahmini"""
        try:
            # Input validasyonu
            required_fields = ['marka', 'model', 'yil', 'kilometre', 'donanim']
            if not all(k in arac_bilgileri for k in required_fields):
                raise ValueError("Eksik araç bilgisi")

            # String değerleri sayıya çevirme
            try:
                yil = int(arac_bilgileri['yil'])
                kilometre = int(arac_bilgileri['kilometre'])
                donanim = str(arac_bilgileri.get('donanim', 'medium')).lower()
            except (ValueError, TypeError):
                raise ValueError("Geçersiz yıl veya kilometre değeri")

            # Değer kontrolleri
            if not (1950 <= yil <= 2024):
                raise ValueError("Geçersiz yıl")
            if kilometre < 0:
                raise ValueError("Geçersiz kilometre")
            if donanim not in self.equipment_levels:
                donanim = 'medium'

            # Temel fiyat hesaplama
            base_price = self._get_base_price(
                arac_bilgileri['marka'],
                arac_bilgileri['model']
            )

            # Faktörleri hesapla
            age_factor = self._calculate_age_factor(yil)
            damage_factor = self._calculate_damage_factor(hasar_durumu)
            mileage_factor = self._calculate_mileage_factor(kilometre)
            equipment_factor = self._calculate_equipment_factor(donanim)

            # Piyasa varyasyonlarını hesapla
            market_prices = [self._calculate_market_variation(base_price) 
                           for _ in range(5)]

            # Son fiyat hesaplama
            final_price = (
                sum(market_prices) / len(market_prices) * 
                age_factor * 
                damage_factor * 
                mileage_factor * 
                equipment_factor
            )

            # Donanım detaylarını al
            equipment_details = self._get_equipment_details(donanim)

            return {
                'predicted_price': round(final_price, 2),
                'market_data': {
                    'min_price': round(min(market_prices), 2),
                    'max_price': round(max(market_prices), 2),
                    'avg_price': round(sum(market_prices) / len(market_prices), 2)
                },
                'factors': {
                    'hasar_durumu': hasar_durumu,
                    'model_yili': yil,
                    'kilometre': kilometre,
                    'donanim_seviyesi': donanim.capitalize(),
                    'hasar_katsayi': damage_factor,
                    'age_factor': age_factor,
                    'mileage_factor': mileage_factor,
                    'equipment_factor': equipment_factor,
                    'base_price': base_price
                },
                'equipment_details': equipment_details
            }

        except Exception as e:
            logger.error(f"Fiyat tahmini sırasında hata: {str(e)}")
            raise ValueError(f"Fiyat tahmin edilemedi: {str(e)}")