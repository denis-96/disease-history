import { axios } from "../api/axios";
import { AUTH_URLS } from "../api/endpoints";
import useAuth from "./useAuth";

const useLogout = () => {
  const { setAuth } = useAuth();

  const logout = async () => {
    setAuth({});
    localStorage.clear();
    try {
      await axios(AUTH_URLS.LOGOUT, {
        withCredentials: true,
      });
    } catch (err) {
      console.error(err);
    }
  };

  return logout;
};

export default useLogout;
