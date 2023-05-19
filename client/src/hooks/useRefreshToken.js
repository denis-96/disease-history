import { AUTH_URLS } from "../api/endpoints";
import { axios } from "../api/axios";
import useAuth from "./useAuth";
import { decodeTokenPayload } from "../utils/jwt";

const useRefreshToken = () => {
  const { setAuth } = useAuth();

  const refresh = async () => {
    const response = await axios.get(AUTH_URLS.REFRESH, {
      withCredentials: true,
    });
    if (!response.data?.access_token) {
      setAuth({});
      return;
    }
    const accessToken = response.data.access_token;
    setAuth({
      user: decodeTokenPayload(accessToken).user,
      accessToken: accessToken,
    });
    return accessToken;
  };
  return refresh;
};

export default useRefreshToken;
