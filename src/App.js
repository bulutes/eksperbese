import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Navbar from './components/NavBar';
import HomePage from './components/HomePage';
import LoginPage from './components/LoginPage';
import AdminLogin from './components/AdminLogin';
import AdminPanel from './components/AdminPanel';
import ExpertPanel from './components/ExpertPanel';
import ContactPage from './components/ContactPage';
import './App.css';

function App() {
    return (
        <Router>
            <div className="app">
                <ToastContainer
                    position="top-right"
                    autoClose={5000}
                    hideProgressBar={false}
                    newestOnTop={false}
                    closeOnClick
                    rtl={false}
                    pauseOnFocusLoss
                    draggable
                    pauseOnHover
                    theme="light"
                />
                <Navbar />
                <main className="main-content">
                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/login" element={<LoginPage />} />
                        <Route path="/admin-login" element={<AdminLogin />} />
                        <Route path="/admin-panel" element={<AdminPanel />} />
                        <Route path="/expert" element={<ExpertPanel />} />
                        <Route path="/contact" element={<ContactPage />} />
                    </Routes>
                </main>
                <footer className="footer">
                    <p>&copy; 2024 EksperTahmin. Tüm hakları saklıdır.</p>
                </footer>
            </div>
        </Router>
    );
}

export default App;