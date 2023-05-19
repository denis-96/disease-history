import { useEffect } from "react";

import "./App.scss";

import { AUTH_URLS } from "./api/endpoints";
import useAuth from "./hooks/useAuth";
import useAuthorizedAxios from "./hooks/useAuthorizedAxios";
import LoginPage from "./pages/Login";
import MainPage from "./pages/Main";

function App() {
  const { auth } = useAuth();
  const authorizedAxios = useAuthorizedAxios();

  useEffect(() => {
    authorizedAxios.get(AUTH_URLS.CHECK);
    // eslint-disable-next-line
  }, []);

  return <div className="app">{auth?.user ? <MainPage /> : <LoginPage />}</div>;
}

export default App;
