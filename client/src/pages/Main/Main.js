import { useState } from "react";

import "./Main.scss";
import Nav from "../../components/Nav";
import Patient from "../../components/Patient/Patient";

function MainPage() {
  const [selectedPatient, setSelectedPatient] = useState(null);

  return (
    <>
      <Nav onPatientSelect={(patient) => setSelectedPatient(patient)} />
      <Patient patient={selectedPatient} />
    </>
  );
}

export default MainPage;
