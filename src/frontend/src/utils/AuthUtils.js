import axios from 'axios';


export function isAuthenticated() {
  return localStorage.getItem('access_token') !== null;
}

export function getAccessToken() {
  if (!isAuthenticated()) {
    return false;
  }

  return localStorage.getItem('access_token');
}

export function getAPIKey() {
  if (!isAuthenticated()) {
    return false;
  }

  return localStorage.getItem('api_key');
}

export function storeAccessToken(response) {
  localStorage.setItem('access_token', response.access_token);
  localStorage.setItem('api_key', response.api_key);
  axios.defaults.headers.common['Authorization'] = `Bearer ${response.access_token}`;
}

export function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('api_key');
}
