import { createContext } from "react";
import useLocalStorage from "../hooks/useLocalStorage";

const PatientContext = createContext({});

const PatientProvider = ({ children }) => {
  const [patientId, setPatientId] = useLocalStorage("selectedPatientId", null);

  return (
    <PatientContext.Provider value={{ patientId, setPatientId }}>
      {children}
    </PatientContext.Provider>
  );
};

export default PatientContext;
export { PatientProvider };
