import React, { createContext, useContext, useEffect, useState } from "react";
import axiosInstance from "../api/axios";

const AuthContext = createContext({
    token: "",
    user: null,
    login: (token, user) => {},
    logout: () => {}
});

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(() => sessionStorage.getItem("token") || "");
    const [user, setUser] = useState(() => {
        try {
            const u = sessionStorage.getItem("user");
            return u ? JSON.parse(u) : null;
        } catch {
            return null;
        }
    });

    const login = (newToken, newUser) => {
        sessionStorage.setItem("token", newToken);
        sessionStorage.setItem("user", JSON.stringify(newUser));
        setToken(newToken);
        setUser(newUser);
    };

    const logout = () => {
        sessionStorage.removeItem("token");
        sessionStorage.removeItem("user");
        setToken("");
        setUser(null);
    };

    useEffect(() => {
        const interceptor = axiosInstance.interceptors.request.use((config) => {
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });
        return () => axiosInstance.interceptors.request.eject(interceptor);
    }, [token]);

    return (
        <AuthContext.Provider value={{ token, user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);