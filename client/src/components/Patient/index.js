import "./index.scss";

import usePatientId from "../../hooks/usePatientId";

import Info from "./Info";
import Treatment from "./Treatment";

function Patient() {
  const { patientId } = usePatientId();

  return patientId ? (
    <>
      <button className="patient__delete-btn"></button>
      <Info />
      <Treatment />
    </>
  ) : (
    <div className="choose-patient">Выберите пациента</div>
  );
}

export default Patient;
