import { Container } from "react-bootstrap";

import "./App.css";

import NavBar from "./components/NavBar";
import MainForm from "./components/MainForm";
import TimeLine from "./components/TimeLine";

function App() {
  return (
    <div className="app">
      <NavBar />
      <Container>
        <MainForm />
        <hr className="mt-5 mb-3" />
        <TimeLine />
        <div style={{ height: 200 }}></div>
      </Container>
    </div>
  );
}

export default App;
