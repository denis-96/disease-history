import { useEffect, useState } from "react";

import "./App.scss";

import { fetchAuthToken } from "./utils";
import { CHECK_AUTH_URL } from "./constants";

import Nav from "./components/Nav";
import Disease from "./components/Disease/Disease";
import Login from "./components/Login";

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const login = () => {
    setIsLoading(true);
    const token = fetchAuthToken();
    if (token) {
      fetch(CHECK_AUTH_URL, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => response.json())
        .then((json) => {
          json.authenticated && setCurrentUser(json.user);
          setIsLoading(false);
        });
    }
  };

  useEffect(login, []);

  return (
    <div className="app">
      {currentUser ? (
        <>
          <Nav />
          <Disease />
        </>
      ) : isLoading ? (
        <h1>Loading...</h1>
      ) : (
        <Login onLogin={login} />
      )}
    </div>
  );
}

export default App;
