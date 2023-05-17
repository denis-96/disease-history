import { createContext, useEffect, useState } from "react";

import "./App.scss";

import { isTokenExpired, refreshToken } from "./utils";
import { AUTH } from "./apiEndpoints";

import LoginPage from "./pages/Login/Login";
import MainPage from "./pages/Main/Main";

const tokenContext = createContext(null);

function App() {
  const [token, setToken] = useState(null);
  const [isUserAuthorized, setIsUserAuthorized] = useState(false);

  useEffect(() => {
    if (!token || isTokenExpired(token)) {
      refreshToken(setToken);
      return;
    }

    fetch(AUTH.CHECK, {
      method: "GET",
      credentials: "include",
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => {
        setIsUserAuthorized(response.ok);
        return response.json();
      })
      .then((json) => console.log(json));
  }, [token]);

  return (
    <div className="app">
      <tokenContext.Provider value={{ token, setToken }}>
        {isUserAuthorized ? <MainPage /> : <LoginPage />}
      </tokenContext.Provider>
    </div>
  );
}

export default App;
export { tokenContext };
