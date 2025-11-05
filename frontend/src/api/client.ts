import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

api.interceptors.request.use((config) => {
  const key = localStorage.getItem("apiKey");
  if (key) config.headers["x-api-key"] = key;
  return config;
});

export default api;
