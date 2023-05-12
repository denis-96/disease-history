const generateId = () => Math.random().toString(36).substring(2, 12);

const setAuthToken = (token) => localStorage.setItem("token", token);

const fetchAuthToken = () => localStorage.getItem("token");

export { generateId, setAuthToken, fetchAuthToken };
