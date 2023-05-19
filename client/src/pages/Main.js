import "./Main.scss";

import { PatientProvider } from "../contexts/PatientContext";
import Nav from "../components/Nav/Nav";
import Patient from "../components/Patient";

function MainPage() {
  return (
    <PatientProvider>
      <Nav />
      <Patient />
    </PatientProvider>
  );
}

export default MainPage;
