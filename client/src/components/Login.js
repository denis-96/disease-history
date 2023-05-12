import { GoogleLogin } from "@react-oauth/google";

import "./Login.scss";

import { setAuthToken } from "../utils";
import { AUTH_URL } from "../constants";

const authorizeUser = (auth_token, auth_url = AUTH_URL) => {
  fetch(auth_url, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify({
      google_id_token: auth_token,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((json) => {
      json.access_token && setAuthToken(json.access_token);
    });
};

const handelGoogleResponse = (response, onLogin) => {
  if (response.credential) {
    authorizeUser(response.credential);
    onLogin();
  } else {
    alert("Ошибка авторизации");
  }
};

function Login({ onLogin }) {
  return (
    <div className="login">
      <div className="container">
        <div className="login__wrapper">
          <h1>Aвторизация</h1>
          <GoogleLogin
            onSuccess={(response) => handelGoogleResponse(response, onLogin)}
            onError={() => console.log("Login Failed")}
            useOneTap
            shape="rectangular"
            theme="filled_blue"
            size="large"
          />
        </div>
      </div>
    </div>
  );
}

export default Login;
