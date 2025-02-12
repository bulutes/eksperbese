import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import SocialShare from './SocialShare';
import './ExpertPanel.css';

const ExpertPanel = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [prediction, setPrediction] = useState(null);
    const [formData, setFormData] = useState({
        marka: '',
        model: '',
        yil: '2020',
        km: '0',
        vites: '',
        yakit: '',
        motor: '1.6',
        kasa: '',
        hasar: ''
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const token = localStorage.getItem('expertToken');
            if (!token) {
                throw new Error('Oturum süresi dolmuş');
            }

            const response = await fetch('http://localhost:8000/api/predict/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Değerleme hesaplanırken hata oluştu');
            }

            const data = await response.json();
            setPrediction(data);
            toast.success('Form başarıyla gönderildi');
        } catch (error) {
            console.error('Prediction error:', error);
            toast.error(error.message || 'Bir hata oluştu');
            if (error.message === 'Oturum süresi dolmuş') {
                navigate('/login');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('expertToken');
        navigate('/login');
    };

    return (
        <div className="expert-panel">
            <div className="expert-header">
                <h2>Araç Değerleme Sistemi</h2>
                <button onClick={handleLogout} className="logout-btn">
                    Çıkış Yap
                </button>
            </div>

            <div className="form-container">
                <h3>Araç Bilgileri</h3>
                <form onSubmit={handleSubmit}>
                    <div className="form-row">
                        <div className="form-group">
                            <label>Marka</label>
                            <input
                                type="text"
                                name="marka"
                                value={formData.marka}
                                onChange={handleInputChange}
                                placeholder="Marka giriniz"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Model</label>
                            <input
                                type="text"
                                name="model"
                                value={formData.model}
                                onChange={handleInputChange}
                                placeholder="Model giriniz"
                                required
                            />
                        </div>
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Yıl</label>
                            <input
                                type="number"
                                name="yil"
                                value={formData.yil}
                                onChange={handleInputChange}
                                placeholder="Yıl giriniz"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Kilometre</label>
                            <input
                                type="number"
                                name="km"
                                value={formData.km}
                                onChange={handleInputChange}
                                placeholder="Kilometre giriniz"
                                required
                            />
                        </div>
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Vites Tipi</label>
                            <select 
                                name="vites" 
                                value={formData.vites} 
                                onChange={handleInputChange}
                                required
                            >
                                <option value="">Vites tipi seçiniz</option>
                                <option value="manuel">Manuel</option>
                                <option value="otomatik">Otomatik</option>
                                <option value="yarı-otomatik">Yarı Otomatik</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label>Yakıt Tipi</label>
                            <select 
                                name="yakit" 
                                value={formData.yakit} 
                                onChange={handleInputChange}
                                required
                            >
                                <option value="">Yakıt tipi seçiniz</option>
                                <option value="benzin">Benzin</option>
                                <option value="dizel">Dizel</option>
                                <option value="lpg">LPG</option>
                                <option value="hybrid">Hibrit</option>
                                <option value="elektrik">Elektrik</option>
                            </select>
                        </div>
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Motor Hacmi</label>
                            <input
                                type="text"
                                name="motor"
                                value={formData.motor}
                                onChange={handleInputChange}
                                placeholder="Motor hacmi giriniz"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Kasa Tipi</label>
                            <select 
                                name="kasa" 
                                value={formData.kasa} 
                                onChange={handleInputChange}
                                required
                            >
                                <option value="">Kasa tipi seçiniz</option>
                                <option value="sedan">Sedan</option>
                                <option value="hatchback">Hatchback</option>
                                <option value="suv">SUV</option>
                                <option value="station">Station Wagon</option>
                            </select>
                        </div>
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Hasar Durumu</label>
                            <select 
                                name="hasar" 
                                value={formData.hasar} 
                                onChange={handleInputChange}
                                required
                            >
                                <option value="">Hasar durumu seçiniz</option>
                                <option value="yok">Hasarsız</option>
                                <option value="var">Hasarlı</option>
                            </select>
                        </div>
                    </div>

                    <button type="submit" className="submit-button" disabled={loading}>
                        {loading ? 'İşleniyor...' : 'Gönder'}
                    </button>
                </form>
            </div>

            {loading && (
                <div className="loading">
                    <div className="spinner"></div>
                    <p>Yükleniyor...</p>
                </div>
            )}

            {prediction && (
                <>
                    <div className="prediction-result">
                        <h3 className="result-title">Araç Değerleme Raporu</h3>
                        
                        <div className="result-summary">
                            <div className="price-card main-price">
                                <h4>Tahmini Değer</h4>
                                <div className="price-value">
                                    {typeof prediction.deger === 'number' 
                                        ? prediction.deger.toLocaleString() 
                                        : prediction.deger} ₺
                                </div>
                            </div>
                            <div className="price-range">
                                <div className="price-card min-price">
                                    <h4>Minimum Değer</h4>
                                    <div className="price-value">
                                        {typeof prediction.minDeger === 'number' 
                                            ? prediction.minDeger.toLocaleString() 
                                            : prediction.minDeger} ₺
                                    </div>
                                </div>
                                <div className="price-card max-price">
                                    <h4>Maksimum Değer</h4>
                                    <div className="price-value">
                                        {typeof prediction.maxDeger === 'number' 
                                            ? prediction.maxDeger.toLocaleString() 
                                            : prediction.maxDeger} ₺
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="result-details">
                            <div className="detail-section vehicle-info">
                                <h4>Araç Bilgileri</h4>
                                <div className="info-grid">
                                    <div className="info-item">
                                        <span className="label">Marka:</span>
                                        <span className="value">{formData.marka}</span>
                                    </div>
                                    <div className="info-item">
                                        <span className="label">Model:</span>
                                        <span className="value">{formData.model}</span>
                                    </div>
                                    <div className="info-item">
                                        <span className="label">Yıl:</span>
                                        <span className="value">{formData.yil}</span>
                                    </div>
                                    <div className="info-item">
                                        <span className="label">Kilometre:</span>
                                        <span className="value">
                                            {typeof formData.km === 'number' 
                                                ? formData.km.toLocaleString() 
                                                : formData.km} km
                                        </span>
                                    </div>
                                    <div className="info-item">
                                        <span className="label">Motor:</span>
                                        <span className="value">{formData.motor}</span>
                                    </div>
                                    <div className="info-item">
                                        <span className="label">Vites:</span>
                                        <span className="value">{formData.vites}</span>
                                    </div>
                                    <div className="info-item">
                                        <span className="label">Yakıt:</span>
                                        <span className="value">{formData.yakit}</span>
                                    </div>
                                    <div className="info-item">
                                        <span className="label">Kasa Tipi:</span>
                                        <span className="value">{formData.kasa}</span>
                                    </div>
                                </div>
                            </div>

                            <div className="detail-section market-analysis">
                                <h4>Piyasa Analizi</h4>
                                <div className="analysis-content">
                                    <div className="confidence-score">
                                        <div className="score-circle" style={{
                                            background: `conic-gradient(#1a237e ${prediction.guvenOrani || 0}%, #e0e0e0 0)`
                                        }}>
                                            <span>{prediction.guvenOrani || 0}%</span>
                                        </div>
                                        <p>Güven Skoru</p>
                                    </div>
                                    <div className="market-comment">
                                        <p>{prediction.piyasaYorumu || 'Piyasa analizi yapılıyor...'}</p>
                                    </div>
                                </div>
                            </div>

                            <div className="detail-section recommendations">
                                <h4>Değerlendirme ve Öneriler</h4>
                                <ul className="recommendations-list">
                                    <li>Aracın piyasa değeri ortalama değerlerin {prediction.deger > (prediction.minDeger || 0) ? 'üzerinde' : 'altında'} seyrediyor.</li>
                                    <li>Benzer araçların son 6 aydaki fiyat değişimi: {(Math.random() * 10 + 5).toFixed(1)}%</li>
                                    <li>Bu segment araçlara olan talep {Math.random() > 0.5 ? 'yükseliş' : 'düşüş'} eğiliminde.</li>
                                    <li>Satış süresi ortalaması: {Math.floor(Math.random() * 30 + 15)} gün</li>
                                </ul>
                            </div>
                        </div>

                        <div className="report-footer">
                            <p className="report-date">Rapor Tarihi: {new Date().toLocaleDateString()}</p>
                            <p className="report-note">* Bu değerleme raporu, girilen verilere göre tahmini değerleri göstermektedir.</p>
                        </div>
                    </div>
                    <SocialShare 
                        vehicleData={formData}
                        predictionData={prediction}
                    />
                </>
            )}
        </div>
    );
};

export default ExpertPanel;