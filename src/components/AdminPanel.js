import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import './AdminPanel.css';

function AdminPanel() {
    const [newPassword, setNewPassword] = useState('');
    const [passwords, setPasswords] = useState([]);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('adminToken');
        if (!token) {
            navigate('/admin-login');
            return;
        }
        fetchPasswords();
    }, [navigate]);

    const fetchPasswords = async () => {
        try {
            const token = localStorage.getItem('adminToken');
            const response = await fetch('http://localhost:8000/admin/passwords', {
                headers: {
                    'Authorization': token
                }
            });
            if (response.ok) {
                const data = await response.json();
                setPasswords(data.expert_passwords);
            }
        } catch (error) {
            console.error('Şifre listesi alınamadı:', error);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('adminToken');
        navigate('/admin-login');
    };

    const handleAddPassword = async (e) => {
        e.preventDefault();
        if (!newPassword.trim()) return;

        setLoading(true);
        try {
            const token = localStorage.getItem('adminToken');
            const response = await fetch('http://localhost:8000/admin/add-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token
                },
                body: JSON.stringify({ password: newPassword })
            });

            if (response.ok) {
                toast.success('Şifre başarıyla eklendi');
                setNewPassword('');
                fetchPasswords();
            }
        } catch (error) {
            toast.error('Şifre eklenirken hata oluştu');
        } finally {
            setLoading(false);
        }
    };

    const handleDeletePassword = async (password) => {
        try {
            const token = localStorage.getItem('adminToken');
            const response = await fetch('http://localhost:8000/admin/delete-password', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token
                },
                body: JSON.stringify({ password })
            });

            if (response.ok) {
                toast.success('Şifre başarıyla silindi');
                fetchPasswords();
            }
        } catch (error) {
            toast.error('Şifre silinirken hata oluştu');
        }
    };

    return (
        <div className="admin-panel-container">
            <div className="admin-panel-header">
                <h1 className="admin-panel-title">Admin Paneli</h1>
                <button onClick={handleLogout} className="admin-logout">
                    Çıkış Yap
                </button>
            </div>

            <div className="admin-content">
                <div className="admin-card">
                    <h3>Yeni Eksper Şifresi Ekle</h3>
                    <form onSubmit={handleAddPassword} className="admin-form">
                        <div className="admin-input-group">
                            <input
                                type="text"
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                placeholder="Yeni şifre"
                                className="admin-input"
                                disabled={loading}
                            />
                        </div>
                        <button type="submit" className="admin-button" disabled={loading}>
                            {loading ? 'Ekleniyor...' : 'Ekle'}
                        </button>
                    </form>
                </div>

                <div className="admin-card">
                    <h3>Mevcut Şifreler</h3>
                    <div className="admin-list">
                        {passwords.map((password, index) => (
                            <div key={index} className="admin-list-item">
                                <span>{password}</span>
                                <button
                                    onClick={() => handleDeletePassword(password)}
                                    className="admin-button delete"
                                >
                                    Sil
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {loading && (
                <div className="loading">
                    <div className="spinner"></div>
                </div>
            )}

            <footer className="admin-footer">
                <p>© 2024 EksperTahmin. Tüm hakları saklıdır.</p>
            </footer>
        </div>
    );
}

export default AdminPanel;