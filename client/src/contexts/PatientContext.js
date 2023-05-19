import { createContext, useState } from "react";

const PatientContext = createContext({});

const PatientProvider = ({ children }) => {
  const [patientId, setPatientId] = useState(
    localStorage.getItem("selectedPatientId")
  );

  return (
    <PatientContext.Provider value={{ patientId, setPatientId }}>
      {children}
    </PatientContext.Provider>
  );
};

export default PatientContext;
export { PatientProvider };
