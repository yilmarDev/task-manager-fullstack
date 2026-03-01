import axios from 'axios';

const url: string = import.meta.env.VITE_API_BASE_URL!;

const securityApi = axios.create({
  baseURL: url,
});

securityApi.interceptors.request.use((config) => {
  const token: string = localStorage.getItem('Authorization')!;
  config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export { securityApi };
