import { useState } from "react";
import { GoogleLogin, GoogleOAuthProvider } from "@react-oauth/google";

import "./Login.scss";

import { AUTH_URLS } from "../api/endpoints";
import { axios } from "../api/axios";
import { decodeTokenPayload } from "../utils/jwt";
import useAuth from "../hooks/useAuth";

function LoginPage() {
  const { setAuth } = useAuth();

  const [errorMsg, setErrorMsg] = useState("");

  const onGoogleLoginSuccess = async (googleResponse) => {
    try {
      const response = await axios.post(
        AUTH_URLS.AUTH,
        JSON.stringify({
          google_id_token: googleResponse.credential,
        }),
        {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true,
        }
      );
      const accessToken = response?.data?.access_token;
      const user = decodeTokenPayload(accessToken).user;
      setAuth({ accessToken, user });
    } catch (error) {
      if (!error?.response) {
        setErrorMsg("No Server Response");
      } else {
        setErrorMsg(error?.response?.data?.detail || "Login Failed");
      }
    }
  };
  const onGoogleLoginError = (error) => {
    setErrorMsg(error);
  };

  return (
    <div className="login">
      {errorMsg && <p className="login__error-msg">{errorMsg}</p>}

      <GoogleOAuthProvider clientId="888133057736-nt82ao6ucu16ubdvsa0t841ivcrlcd62.apps.googleusercontent.com">
        <GoogleLogin
          onSuccess={onGoogleLoginSuccess}
          onError={onGoogleLoginError}
          shape="rectangular"
          theme="filled_blue"
          size="large"
        />
      </GoogleOAuthProvider>
    </div>
  );
}

export default LoginPage;
