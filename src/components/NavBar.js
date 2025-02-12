import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import './Navbar.css';

function Navbar() {
    const letterVariants = {
        initial: { y: -20, opacity: 0 },
        animate: (i) => ({
            y: 0,
            opacity: 1,
            transition: {
                duration: 0.7,
                delay: i * 0.1,
                type: "spring",
                stiffness: 100
            }
        })
    };

    const logoText = "EksperTahmin";

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/" className="logo-link">
                    <motion.div className="logo-wrapper">
                        <motion.h1 
                            className="logo-text"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                        >
                            {logoText.split("").map((letter, i) => (
                                <motion.span
                                    key={i}
                                    custom={i}
                                    variants={letterVariants}
                                    initial="initial"
                                    animate="animate"
                                    whileHover={{
                                        scale: 1.2,
                                        color: '#26d0ce',
                                        transition: { duration: 0.2 }
                                    }}
                                    className="logo-letter"
                                >
                                    {letter}
                                </motion.span>
                            ))}
                        </motion.h1>
                        <motion.div
                            className="logo-underline"
                            initial={{ width: 0 }}
                            animate={{ width: "100%" }}
                            transition={{ delay: 1, duration: 0.8 }}
                        />
                    </motion.div>
                </Link>

                <motion.div 
                    className="nav-links"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 1.5 }}
                >
                    <Link to="/" className="nav-link">Ana Sayfa</Link>
                    <Link to="/contact" className="nav-link">İletişim</Link>
                    <Link to="/login" className="nav-link">Eksper Girişi</Link>
                    <Link to="/admin-login" className="nav-link">Admin</Link>
                </motion.div>
            </div>
        </nav>
    );
}

export default Navbar;