import React, { useState } from 'react';
import { motion } from 'framer-motion';
import './ContactPage.css';

function ContactPage() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // Form gönderme işlemi burada yapılacak
        console.log('Form gönderildi:', { name, email, message });
    };

    const pricingPlans = [
        {
            title: "Temel Plan",
            price: "₺99",
            features: [
                "Temel araç değerleme",
                "3 araç karşılaştırma",
                "Basit rapor"
            ]
        },
        {
            title: "Profesyonel",
            price: "₺199",
            features: [
                "Detaylı araç değerleme",
                "Sınırsız karşılaştırma",
                "Kapsamlı rapor",
                "Piyasa analizi"
            ]
        },
        {
            title: "Kurumsal",
            price: "₺499",
            features: [
                "Tüm Profesyonel özellikleri",
                "API erişimi",
                "Özel destek",
                "Toplu değerleme",
                "Özelleştirilmiş raporlar"
            ]
        }
    ];

    return (
        <div className="contact-container">
            <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="pricing-section"
            >
                <h2>Fiyatlandırma</h2>
                <div className="pricing-cards">
                    {pricingPlans.map((plan, index) => (
                        <motion.div 
                            className="pricing-card"
                            key={index}
                            whileHover={{ scale: 1.05 }}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ 
                                type: "spring", 
                                stiffness: 300,
                                delay: index * 0.2 
                            }}
                        >
                            <h3>{plan.title}</h3>
                            <div className="price">{plan.price}</div>
                            <ul>
                                {plan.features.map((feature, idx) => (
                                    <motion.li 
                                        key={idx}
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: index * 0.1 + idx * 0.1 }}
                                    >
                                        {feature}
                                    </motion.li>
                                ))}
                            </ul>
                            <motion.button
                                whileHover={{ scale: 1.1 }}
                                whileTap={{ scale: 0.9 }}
                            >
                                Planı Seç
                            </motion.button>
                        </motion.div>
                    ))}
                </div>
            </motion.div>

            <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.5 }}
                className="contact-form-section"
            >
                <h2>Bize Ulaşın</h2>
                <form onSubmit={handleSubmit} className="contact-form">
                    <motion.div 
                        className="form-group"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.6 }}
                    >
                        <label>İsim</label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </motion.div>

                    <motion.div 
                        className="form-group"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.7 }}
                    >
                        <label>E-posta</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </motion.div>

                    <motion.div 
                        className="form-group"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.8 }}
                    >
                        <label>Mesaj</label>
                        <textarea
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            required
                        />
                    </motion.div>

                    <motion.button
                        type="submit"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.9 }}
                    >
                        Gönder
                    </motion.button>
                </form>
            </motion.div>
        </div>
    );
}

export default ContactPage;