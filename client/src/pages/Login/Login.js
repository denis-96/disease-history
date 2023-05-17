import { GoogleLogin, GoogleOAuthProvider } from "@react-oauth/google";

import "./Login.scss";

import { AUTH } from "../../apiEndpoints";
import { useContext } from "react";
import { tokenContext } from "../../App";

function LoginPage() {
  const { setToken } = useContext(tokenContext);

  const onGoogleLoginSuccess = (response) => {
    if (response.credential) {
      fetch(AUTH.AUTH, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({
          google_id_token: response.credential,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((json) => {
          json.access_token && setToken(json.access_token);
        });
    }
  };
  const onGoogleLoginError = () => {};

  return (
    <GoogleOAuthProvider clientId="888133057736-nt82ao6ucu16ubdvsa0t841ivcrlcd62.apps.googleusercontent.com">
      <div className="login">
        <div className="container">
          <div className="login__wrapper">
            <h1>Aвторизация</h1>
            <GoogleLogin
              onSuccess={onGoogleLoginSuccess}
              onError={onGoogleLoginError}
              shape="rectangular"
              theme="filled_blue"
              size="large"
            />
          </div>
        </div>
      </div>
    </GoogleOAuthProvider>
  );
}

export default LoginPage;
