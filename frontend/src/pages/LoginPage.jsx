import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { login as apiLogin } from "../services/api";
import "./LoginPage.css";

export default function LoginPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    async function handleSubmit(e) {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            const data = await apiLogin(username, password);
            login(data);
            navigate("/loading", { replace: true });
        } catch (err) {
            setError(err.message || "Invalid credentials");
        } finally {
            setLoading(false);
        }
    }

    function fillDemo(user, pass) {
        setUsername(user);
        setPassword(pass);
        setError("");
    }

    return (
        <div className="login-page">
            <div className="login-hero">
                {/* Left — Branding */}
                <div className="login-container">
                    <div className="login-branding animate-fade-in">
                        <div className="login-brand-icon">📚</div>
                        <h1 className="login-title">
                            Your Child&apos;s <span className="text-gradient">Success Story</span> Starts Here
                        </h1>
                        <p className="login-subtitle">
                            AI-powered sentiment analysis of teacher reviews — giving parents
                            clear, actionable insights into their child&apos;s academic journey.
                        </p>

                        <div className="login-features">
                            <div className="login-feature">
                                <div className="login-feature-icon purple">📊</div>
                                <div className="login-feature-text">
                                    <h4>Sentiment Analysis</h4>
                                    <p>NLP-powered review breakdown</p>
                                </div>
                            </div>
                            <div className="login-feature">
                                <div className="login-feature-icon green">✅</div>
                                <div className="login-feature-text">
                                    <h4>Strengths & Growth Areas</h4>
                                    <p>Actionable insights for parents</p>
                                </div>
                            </div>
                            <div className="login-feature">
                                <div className="login-feature-icon amber">📈</div>
                                <div className="login-feature-text">
                                    <h4>Interactive Charts</h4>
                                    <p>Visualize performance trends</p>
                                </div>
                            </div>
                            <div className="login-feature">
                                <div className="login-feature-icon blue">👥</div>
                                <div className="login-feature-text">
                                    <h4>Role-Based Access</h4>
                                    <p>Separate dashboards for parents & teachers</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right — Login Card */}
                    <div className="login-card">
                        <div className="login-card-header">
                            <h2>Welcome Back 👋</h2>
                            <p>Sign in to access your dashboard</p>
                        </div>

                        {error && <div className="login-error">❌ {error}</div>}

                        <form className="login-form" onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label className="form-label" htmlFor="username">
                                    Username
                                </label>
                                <input
                                    id="username"
                                    className="form-input"
                                    type="text"
                                    placeholder="Enter your username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    autoComplete="username"
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label" htmlFor="password">
                                    Password
                                </label>
                                <input
                                    id="password"
                                    className="form-input"
                                    type="password"
                                    placeholder="Enter your password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    autoComplete="current-password"
                                    required
                                />
                            </div>

                            <button
                                type="submit"
                                className="btn btn-primary btn-block btn-lg"
                                disabled={loading}
                            >
                                {loading ? (
                                    <>
                                        <span className="spinner" /> Signing in…
                                    </>
                                ) : (
                                    "🚀 Sign In"
                                )}
                            </button>
                        </form>

                        <div className="login-divider">Demo Accounts</div>

                        <div className="login-demo">
                            <button
                                type="button"
                                className="login-demo-btn"
                                onClick={() => fillDemo("parent1", "pass1234")}
                            >
                                <strong>👨‍👩‍👧 Parent</strong>
                                parent1 / pass1234
                            </button>
                            <button
                                type="button"
                                className="login-demo-btn"
                                onClick={() => fillDemo("teacher", "admin1234")}
                            >
                                <strong>🧑‍🏫 Teacher</strong>
                                teacher / admin1234
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Stats Bar */}
            <div className="login-stats">
                <div className="login-stat">
                    <div className="login-stat-value text-gradient">50+</div>
                    <div className="login-stat-label">Student Profiles</div>
                </div>
                <div className="login-stat">
                    <div className="login-stat-value text-gradient">5</div>
                    <div className="login-stat-label">Analysis Categories</div>
                </div>
                <div className="login-stat">
                    <div className="login-stat-value text-gradient">AI</div>
                    <div className="login-stat-label">Powered Insights</div>
                </div>
                <div className="login-stat">
                    <div className="login-stat-value text-gradient">2</div>
                    <div className="login-stat-label">Role Dashboards</div>
                </div>
            </div>
        </div>
    );
}
