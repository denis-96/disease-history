import { useEffect, useRef } from "react";

import useRefreshToken from "./useRefreshToken";
import useAuth from "./useAuth";

import { authorizedAxios } from "../api/axios";
import { isTokenExpired } from "../utils/jwt";

const useAuthorizedAxios = () => {
  const refreshToken = useRefreshToken();
  const { auth, setAuth } = useAuth();
  const refreshTokenRequest = useRef(null);

  useEffect(() => {
    const requestInterceptor = authorizedAxios.interceptors.request.use(
      async (config) => {
        let accessToken = auth.accessToken;
        if (!accessToken || isTokenExpired(accessToken)) {
          if (refreshTokenRequest.current === null) {
            refreshTokenRequest.current = refreshToken();
          }
          accessToken = await refreshTokenRequest.current;
          refreshTokenRequest.current = null;
        }

        if (!config.headers["Authorization"]) {
          config.headers["Authorization"] = `Bearer ${accessToken}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    const responseInterceptor = authorizedAxios.interceptors.response.use(
      (response) => response,
      async (error) => {
        const prevRequest = error?.config;
        if (
          (error?.response?.status === 403 ||
            error?.response?.status === 401) &&
          !prevRequest?.sent
        ) {
          setAuth({});
        }
        return Promise.reject(error);
      }
    );

    return () => {
      authorizedAxios.interceptors.request.eject(requestInterceptor);
      authorizedAxios.interceptors.response.eject(responseInterceptor);
    };
    // eslint-disable-next-line
  }, [auth, refreshToken]);

  return authorizedAxios;
};

export default useAuthorizedAxios;
