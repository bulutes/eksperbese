import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import './LoginPage.css';

function LoginPage() {
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!password.trim()) return;

        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ password })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('expertToken', data.token);
                toast.success('Giriş başarılı!');
                navigate('/expert');
            } else {
                const errorData = await response.json();
                toast.error(errorData.detail || 'Geçersiz şifre');
            }
        } catch (error) {
            console.error('Giriş hatası:', error);
            toast.error('Giriş yapılırken hata oluştu');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="wave-decoration"></div>
            <div className="login-card">
                <h2>Eksper Girişi</h2>
                <form onSubmit={handleSubmit}>
                    <div className="login-input-group">
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Eksper şifresi"
                            disabled={loading}
                        />
                    </div>
                    <button type="submit" disabled={loading}>
                        {loading ? 'Giriş yapılıyor...' : 'Giriş Yap'}
                    </button>
                </form>
            </div>
        </div>
    );
}

export default LoginPage;