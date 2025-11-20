import { type AxiosInstance } from "axios";
import axios from "axios";

// axios instance \\
export const axiosInstance: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL as string,
  withCredentials: true,
});

// auth token \\
axiosInstance.interceptors.request.use(
  (config) => {
    const authData = localStorage.getItem("auth-storage");
    if (authData) {
      try {
        const { state } = JSON.parse(authData);
        if (state?.accessToken) {
          config.headers.Authorization = `Bearer ${state.accessToken}`;
        }
      } catch (error) {
        console.error("Error parsing auth data:", error);
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Response to handle token refresh \\
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const authData = localStorage.getItem("auth-storage");
      if (authData) {
        try {
          const { state } = JSON.parse(authData);
          if (state?.refreshToken) {
            // refresh token \\
            const refreshResponse = await axios.post(
              `${import.meta.env.VITE_API_URL}/users/refresh`,
              { refresh_token: state.refreshToken },
            );

            const { access_token, refresh_token } = refreshResponse.data;

            const updatedState = {
              ...state,
              accessToken: access_token,
              refreshToken: refresh_token || state.refreshToken,
            };

            localStorage.setItem(
              "auth-storage",
              JSON.stringify({ state: updatedState }),
            );

            originalRequest.headers.Authorization = `Bearer ${access_token}`;
            return axiosInstance(originalRequest);
          }
        } catch (refreshError) {
          console.error("Token refresh failed:", refreshError);
          localStorage.removeItem("auth-storage");
          window.location.href = "/login";
        }
      }
    }

    return Promise.reject(error);
  },
);