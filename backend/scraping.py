import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
import json

class CarScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.cars_data = []
        
    def scrape_sahibinden(self, max_pages=50):
        """Sahibinden.com'dan araç verilerini çek"""
        base_url = "https://www.sahibin.com/otomobil?pagingOffset={}"
        
        for page in range(max_pages):
            try:
                url = base_url.format(page * 20)
                response = requests.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    listings = soup.find_all('tr', class_='searchResultsItem')
                    
                    for item in listings:
                        try:
                            car = self._parse_listing(item)
                            if car:
                                self.cars_data.append(car)
                                print(f"Araç verisi eklendi: {car['marka']} {car['model']}")
                        except Exception as e:
                            print(f"İlan ayrıştırma hatası: {str(e)}")
                    
                    # Siteyi yormamak için bekleme
                    time.sleep(random.uniform(2, 4))
                    
            except Exception as e:
                print(f"Sayfa çekme hatası: {str(e)}")
                continue
                
        return self.save_data()
    
    def _parse_listing(self, item):
        """İlan detaylarını ayrıştır"""
        try:
            title = item.find('td', class_='searchResultsTagAttributeValue').text.strip()
            price = item.find('td', class_='searchResultsPriceValue').text.strip()
            details = item.find('td', class_='searchResultsAttributeValue').text.strip()
            
            # Başlığı parçala (örn: "2020 BMW 320i")
            year, brand, model = self._parse_title(title)
            
            # Detayları parçala
            km, gear, fuel = self._parse_details(details)
            
            # Fiyatı temizle
            price = self._clean_price(price)
            
            return {
                'marka': brand,
                'model': model,
                'yil': year,
                'km': km,
                'vites': gear,
                'yakit': fuel,
                'motor': self._extract_engine(model),
                'kasa': self._detect_body_type(model),
                'hasar': 'bilinmiyor',  # Detay sayfasından çekilebilir
                'fiyat': price,
                'tarih': datetime.now().strftime('%Y-%m-%d')
            }
        except Exception as e:
            print(f"Ayrıştırma hatası: {str(e)}")
            return None
    
    def _parse_title(self, title):
        """Başlığı parçala"""
        parts = title.split()
        year = int(parts[0])
        brand = parts[1]
        model = ' '.join(parts[2:])
        return year, brand, model
    
    def _parse_details(self, details):
        """Detayları parçala"""
        parts = details.split('/')
        km = int(parts[0].replace('km', '').replace('.', '').strip())
        gear = parts[1].strip().lower()
        fuel = parts[2].strip().lower()
        return km, gear, fuel
    
    def _clean_price(self, price):
        """Fiyatı temizle"""
        return int(price.replace('TL', '').replace('.', '').strip())
    
    def _extract_engine(self, model):
        """Motor hacmini çıkar"""
        # Örnek: "320i" -> 2.0, "1.6 MultiJet" -> 1.6
        try:
            if '.' in model:
                return float(model.split()[0])
            return 1.6  # Varsayılan değer
        except:
            return 1.6
    
    def _detect_body_type(self, model):
        """Kasa tipini tespit et"""
        model_lower = model.lower()
        if any(x in model_lower for x in ['sedan', 'saloon']):
            return 'sedan'
        elif any(x in model_lower for x in ['hb', 'hatchback']):
            return 'hatchback'
        elif any(x in model_lower for x in ['sw', 'wagon', 'estate']):
            return 'station'
        return 'sedan'  # Varsayılan
    
    def save_data(self):
        """Verileri kaydet"""
        df = pd.DataFrame(self.cars_data)
        
        # CSV olarak kaydet
        df.to_csv('data/car_prices.csv', index=False)
        
        # JSON olarak kaydet
        df.to_json('data/car_prices.json', orient='records', force_ascii=False)
        
        print(f"Toplam {len(df)} araç verisi kaydedildi.")
        return df

if __name__ == "__main__":
    scraper = CarScraper()
    df = scraper.scrape_sahibinden(max_pages=50)
