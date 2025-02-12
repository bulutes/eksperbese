from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            name='TurkishStyle',
            fontName='Helvetica',
            fontSize=12,
            leading=14,
        ))

    def generate_report(self, data: dict, output_path: str) -> str:
        try:
            logger.debug(f"Gelen veri: {data}")
            
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            story = []

            # Logo ekleme
            try:
                logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
                logger.debug(f"Logo yolu: {logo_path}")
                
                if os.path.exists(logo_path):
                    img = Image(logo_path)
                    # Logo boyutunu ayarla (genişlik ve yükseklik)
                    img.drawWidth = 150
                    img.drawHeight = 50
                    story.append(img)
                    story.append(Spacer(1, 20))
                else:
                    logger.warning(f"Logo dosyası bulunamadı: {logo_path}")
            except Exception as e:
                logger.error(f"Logo ekleme hatası: {str(e)}")

            # Başlık
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontName='Helvetica',
                fontSize=24,
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph('EksperTahmin - Araç Deger Raporu', title_style))
            story.append(Spacer(1, 20))

            # Tarih
            date_style = ParagraphStyle(
                'DateStyle',
                parent=self.styles['Normal'],
                fontName='Helvetica',
                fontSize=10,
                alignment=2
            )
            story.append(Paragraph(f'Rapor Tarihi: {datetime.now().strftime("%d.%m.%Y %H:%M")}', date_style))
            story.append(Spacer(1, 20))

            # Araç Bilgileri
            story.append(Paragraph('Araç Bilgileri', self.styles['Heading2']))
            
            # Güvenli veri alımı
            factors = data.get('factors', {})
            arac_bilgileri = data.get('arac_bilgileri', {})
            
            vehicle_data = [
                ['Marka:', str(arac_bilgileri.get('marka', '-'))],
                ['Model:', str(arac_bilgileri.get('model', '-'))],
                ['Yil:', str(factors.get('model_yili', '-'))],
                ['Kilometre:', f"{int(factors.get('kilometre', 0)):,}".replace(',', '.')],
                ['Hasar Durumu:', 'Hasarsiz' if factors.get('hasar_durumu') == 'hasarsiz' else 'Hasarlı'],
                ['Donanim Seviyesi:', str(factors.get('donanim_seviyesi', '-'))]
            ]

            t = Table(vehicle_data, colWidths=[4*cm, 10*cm])
            t.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(t)
            story.append(Spacer(1, 20))

            # Fiyat Bilgileri
            story.append(Paragraph('Fiyat Degerlendirmesi', self.styles['Heading2']))
            price_data = [
                ['Tahmini Deger:', f"{int(data.get('predicted_price', 0)):,} TL".replace(',', '.')],
                ['Minimum Piyasa Degeri:', f"{int(data.get('market_data', {}).get('min_price', 0)):,} TL".replace(',', '.')],
                ['Maksimum Piyasa Degeri:', f"{int(data.get('market_data', {}).get('max_price', 0)):,} TL".replace(',', '.')],
                ['Ortalama Piyasa Degeri:', f"{int(data.get('market_data', {}).get('avg_price', 0)):,} TL".replace(',', '.')]
            ]

            t = Table(price_data, colWidths=[6*cm, 8*cm])
            t.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(t)
            story.append(Spacer(1, 20))

            # Değerlendirme Faktörleri
            story.append(Paragraph('Degerlendirme Faktörleri', self.styles['Heading2']))
            factors_data = [
                ['Hasar Katsayisi:', f"{factors.get('hasar_katsayi', 0)*100:.0f}%"],
                ['Yil Bazli Deger:', f"{factors.get('age_factor', 0)*100:.0f}%"],
                ['Kilometre Etkisi:', f"{factors.get('mileage_factor', 0)*100:.0f}%"],
                ['Donanim Etkisi:', f"{factors.get('equipment_factor', 0)*100:.0f}%"]
            ]

            t = Table(factors_data, colWidths=[6*cm, 8*cm])
            t.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(t)

            doc.build(story)
            return output_path

        except Exception as e:
            logger.error(f"PDF oluşturma hatası: {str(e)}")
            raise Exception(f"PDF oluşturma hatası: {str(e)}")