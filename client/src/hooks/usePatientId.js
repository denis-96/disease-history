import { useContext } from "react";
import PatientContext from "../contexts/PatientContext";

const usePatientId = () => {
  return useContext(PatientContext);
};

export default usePatientId;
