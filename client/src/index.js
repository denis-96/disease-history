import ReactDOM from "react-dom/client";
import { StrictMode } from "react";
import { GoogleOAuthProvider } from "@react-oauth/google";
import "./index.scss";
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <StrictMode>
    <GoogleOAuthProvider clientId="888133057736-nt82ao6ucu16ubdvsa0t841ivcrlcd62.apps.googleusercontent.com">
      <App />
    </GoogleOAuthProvider>
  </StrictMode>
);
