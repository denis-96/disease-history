import Axios from "axios";
import { BASE_URL } from "./endpoints";

const axios = Axios.create({
  baseURL: BASE_URL,
});

const authorizedAxios = Axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
});

export { axios, authorizedAxios };
