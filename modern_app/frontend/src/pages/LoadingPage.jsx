import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./LoadingPage.css";

export default function LoadingPage() {
    const { user } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        const timer = setTimeout(() => {
            if (user?.role === "teacher") {
                navigate("/teacher/dashboard", { replace: true });
            } else {
                navigate("/parent/dashboard", { replace: true });
            }
        }, 2200);

        return () => clearTimeout(timer);
    }, [user, navigate]);

    return (
        <div className="loading-page">
            <div className="book-container">
                <div className="book">
                    <div className="book-cover">📖</div>
                    <div className="book-page" />
                    <div className="book-page" />
                    <div className="book-page" />
                </div>
            </div>

            <div className="loading-text">
                <h2>Preparing your dashboard…</h2>
                <p>Analyzing reviews with AI</p>
            </div>

            <div className="loading-bar-container">
                <div className="loading-bar-fill" />
            </div>
        </div>
    );
}
