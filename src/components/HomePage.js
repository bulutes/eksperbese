import React from 'react';
import { motion } from 'framer-motion';
import { FaCar, FaChartLine, FaShieldAlt } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
    const navigate = useNavigate();

    return (
        <div className="home-container">
            <section className="hero-section">
                <motion.div 
                    className="hero-content"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <h1>EksperTahmin ile Araç Değerleme</h1>
                    <p>Profesyonel ve güvenilir araç değerleme hizmeti</p>
                    <motion.button 
                        className="cta-button"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => navigate('/login')}
                    >
                        Hemen Başla
                    </motion.button>
                </motion.div>
            </section>

            <section className="features-section">
                <h2>Neden EksperTahmin?</h2>
                <div className="features-grid">
                    <motion.div 
                        className="feature-card"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                    >
                        <FaCar className="feature-icon" />
                        <h3>Hassas Değerleme</h3>
                        <p>Güncel piyasa verilerine dayalı doğru değerleme</p>
                    </motion.div>

                    <motion.div 
                        className="feature-card"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.4 }}
                    >
                        <FaChartLine className="feature-icon" />
                        <h3>Piyasa Analizi</h3>
                        <p>Detaylı piyasa karşılaştırması ve trend analizi</p>
                    </motion.div>

                    <motion.div 
                        className="feature-card"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.6 }}
                    >
                        <FaShieldAlt className="feature-icon" />
                        <h3>Güvenilir Sonuçlar</h3>
                        <p>Uzman eksperler tarafından onaylı değerleme</p>
                    </motion.div>
                </div>
            </section>

            <section className="stats-section">
                <div className="stats-grid">
                    <div className="stat-item">
                        <h4>10K+</h4>
                        <p>Değerleme</p>
                    </div>
                    <div className="stat-item">
                        <h4>95%</h4>
                        <p>Doğruluk</p>
                    </div>
                    <div className="stat-item">
                        <h4>1000+</h4>
                        <p>Mutlu Müşteri</p>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default HomePage;