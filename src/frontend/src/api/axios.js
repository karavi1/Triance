import axios from "axios";
import { useAuth } from "../context/AuthContext";

if (!process.env.REACT_APP_BASE_URL) {
    throw new Error("REACT_APP_BASE_URL is not defined in the environment");
}

const BASE_URL = process.env.REACT_APP_BASE_URL;

const axiosInstance = axios.create({ baseURL: BASE_URL });

export const attachToken = (token) => {
    axiosInstance.interceptors.request.use((config) => {
        if (token) config.headers["Authorization"] = `Bearer ${token}`;
        return config;
    });
};

export default axiosInstance;