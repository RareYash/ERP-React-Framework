/**
 * Auth Context — provides user state and login/logout throughout the app.
 */
import { createContext, useContext, useState, useEffect } from "react";
import { getUser, setAuth, clearAuth } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(() => getUser());

    /** Refresh user from storage (e.g. after page reload). */
    useEffect(() => {
        const stored = getUser();
        if (stored) setUser(stored);
    }, []);

    function handleLogin(data) {
        setAuth(data);
        setUser({
            username: data.username,
            role: data.role,
            student_id: data.student_id,
        });
    }

    function handleLogout() {
        clearAuth();
        setUser(null);
    }

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthenticated: !!user,
                isTeacher: user?.role === "teacher",
                isParent: user?.role === "parent",
                login: handleLogin,
                logout: handleLogout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be used within AuthProvider");
    return ctx;
}
