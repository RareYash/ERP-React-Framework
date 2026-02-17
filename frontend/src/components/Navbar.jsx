import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Navbar.css";

export default function Navbar() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    function handleLogout() {
        logout();
        navigate("/", { replace: true });
    }

    if (!user) return null;

    const initials = user.username.slice(0, 2).toUpperCase();

    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <span className="navbar-brand-icon">📚</span>
                <span>Student Review System</span>
            </div>

            <div className="navbar-right">
                <div className="navbar-user">
                    <div className="navbar-user-avatar">{initials}</div>
                    <span>{user.username}</span>
                    <span className={`navbar-role navbar-role-${user.role}`}>
                        {user.role}
                    </span>
                </div>
                <button className="btn-logout" onClick={handleLogout}>
                    🚪 Logout
                </button>
            </div>
        </nav>
    );
}
