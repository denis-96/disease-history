import { AUTH } from "./apiEndpoints";

const generateId = () => Math.random().toString(36).substring(2, 12);

const isTokenExpired = () => false;
const refreshToken = (onSuccess) => {
  fetch(AUTH.REFRESH, { method: "GET", credentials: "include" })
    .then((response) => response.json())
    .then((json) => json.access_token && onSuccess(json.access_token));
};

export { generateId, isTokenExpired, refreshToken };
