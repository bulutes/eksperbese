import React from 'react';
import { motion } from 'framer-motion';
import { FaUsers, FaCar, FaChartBar } from 'react-icons/fa';
import './AboutPage.css';

function AboutPage() {
    return (
        <motion.div 
            className="about-container"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
        >
            <motion.section 
                className="about-hero"
                initial={{ y: 50 }}
                animate={{ y: 0 }}
                transition={{ delay: 0.2 }}
            >
                <h1>Hakkımızda</h1>
                <p>EksperTahmin, araç değerleme konusunda Türkiye'nin öncü platformudur.</p>
            </motion.section>

            <section className="about-content">
                <motion.div 
                    className="about-card"
                    initial={{ x: -100, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.4 }}
                >
                    <FaUsers className="about-icon" />
                    <h2>Deneyimli Ekip</h2>
                    <p>Uzman kadromuzla size en doğru değerlemeyi sunuyoruz.</p>
                </motion.div>

                <motion.div 
                    className="about-card"
                    initial={{ x: 0, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.6 }}
                >
                    <FaCar className="about-icon" />
                    <h2>Geniş Veritabanı</h2>
                    <p>Binlerce araç verisiyle en doğru tahminleri yapıyoruz.</p>
                </motion.div>

                <motion.div 
                    className="about-card"
                    initial={{ x: 100, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.8 }}
                >
                    <FaChartBar className="about-icon" />
                    <h2>Güncel Analizler</h2>
                    <p>Piyasa verilerini anlık olarak takip ediyoruz.</p>
                </motion.div>
            </section>

            <motion.section 
                className="mission-section"
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 1 }}
            >
                <h2>Misyonumuz</h2>
                <p>Araç alım-satım süreçlerinde şeffaflığı ve güvenilirliği artırmak için çalışıyoruz.</p>
            </motion.section>
        </motion.div>
    );
}

export default AboutPage;