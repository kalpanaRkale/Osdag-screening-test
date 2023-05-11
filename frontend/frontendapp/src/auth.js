// src/api/auth.js
import axios from 'axios';

const BASE_URL = 'http://localhost:8000/api/auth/';

export const login = async (formData) => {
  try {
    const res = await axios.post(`${BASE_URL}login/`, formData);
    localStorage.setItem('token', res.data.access);
  } catch (err) {
    console.log(err);
  }
};

export const signup = async (formData) => {
  try {
    const res = await axios.post(`${BASE_URL}signup/`, formData);
    localStorage.setItem('token', res.data.access);
  } catch (err) {
    console.log(err);
  }
};

export const logout = () => {
  localStorage.removeItem('token');
};
