import axios from 'axios';

const url: string = import.meta.env.VITE_API_BASE_URL!;

const apiConn = axios.create({
  baseURL: url,
});

apiConn.interceptors.request.use((config) => {
  const token: string = localStorage.getItem('Authorization')!;
  config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export { apiConn };
