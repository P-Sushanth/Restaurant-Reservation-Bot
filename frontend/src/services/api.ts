import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
});

export const getMenu = async (compressed = false) => {
    const endpoint = compressed ? '/menu/compressed' : '/menu';
    const response = await api.get(endpoint);
    return response.data;
};

export const checkAvailability = async (date: string, guests: number, time?: string) => {
    const params: any = { check_date: date, guests };
    if (time) {
        params.check_time = time;
    }
    const response = await api.get('/availability', { params });
    return response.data;
};

export const makeReservation = async (data: { name: string; phone: string; guests: number; date: string; time: string }) => {
    const response = await api.post('/reserve', data);
    return response.data;
};

export const cancelReservation = async (id: number) => {
    const response = await api.delete(`/cancel/${id}`);
    return response.data;
};

export const chatWithBot = async (message: string) => {
    const response = await api.post('/chat', { message });
    return response.data;
};

export default api;
